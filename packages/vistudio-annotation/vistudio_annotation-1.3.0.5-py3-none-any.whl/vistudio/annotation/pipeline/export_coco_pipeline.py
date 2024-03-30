#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   export_pipeline.py
"""
import ray
from ray.data.read_api import read_datasource
from ray.data.datasource.datasource import Datasource
import sys
import os
__work_dir__ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, __work_dir__)

from vistudio.annotation.datasource import query_pipeline
from base_export_pipeline import BaseExportPipeline
from vistudio.annotation.datasource.sharded_mongo_datasource import ShardedMongoDatasource
from vistudio.annotation.processor.exporter.coco.coco_formatter import CocoFormatter
from vistudio.annotation.processor.exporter.coco.coco_merger import CocoMerger
from vistudio.annotation.writer.writer import Writer, ImageFilenameProvider
import argparse
import logit

job_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/jobs/(?P<job_name>[^/]+)$"
annotationset_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/annotationsets/" \
                             r"(?P<annotationset_local_name>[^/]+)$"


class ExportCocoPipeline(BaseExportPipeline):
    """
    exporter coco pipeline
    """

    def __init__(self,
                 args,
                 ):
        super().__init__(args)

    def _get_mongo_datasource(self) -> Datasource:
        """
        get mongo datasource
        :param config:
        :param params:
        :return: Datasource
        """
        uri = "mongodb://{}:{}@{}:{}".format(self.config.mongodb_user,
                                             self.config.mongodb_password,
                                             self.config.mongodb_host,
                                             self.config.mongodb_port)
        func = query_pipeline.get_pipeline_func(self.mongo_pipeline)
        db_name = self.config.mongodb_database
        collection_name = self.config.mongodb_collection

        source = ShardedMongoDatasource(
            uri=uri,
            database=db_name,
            collection=collection_name,
            pipeline_func=func
        )
        return source

    def run(self, parallelism: int = 10):
        """
        pipeline_coco
        :return:
        """
        # step 1: datasource
        # todo 暂时注释 测试需要
        datasource = self._get_mongo_datasource()
        ds = read_datasource(datasource, parallelism=parallelism)
        logit.info("read data from mongo.dataset count = {}".format(ds.count()))
        if ds.count() <= 0:
            return

        coco_formater = CocoFormatter(labels=self.labels, merge_labels=self.merge_labels)
        merger = CocoMerger()
        format_ds = coco_formater.transform(ds)
        logit.info("format dataset.dataset count = {}".format(format_ds.count()))
        merge_ds = merger.fit(format_ds).stats_
        logit.info("merge dataset.dataset count = {}".format(merge_ds.count()))

        # setp 3: writer
        object_name = "workspaces/{}/projects/{}/datasets/{}".format(
            self.dataset.get('workspaceID'),
            self.dataset.get('projectName'),
            self.dataset.get('localName')
        )
        writer = Writer(config=self.config)
        location_resp = writer.create_location(object_name=object_name)
        location = location_resp.location[len("s3://"):].strip("/")
        logit.info("create windmill location. location= {}".format(location))

        annotation_filename_provider = ImageFilenameProvider(file_name="annotation.json")
        #filename_provider = ImageFilenameProvider(".json")
        writer.write_json(
            ds=merge_ds,
            path=location,
            partition_num=None,
            filename_provider=annotation_filename_provider)
        # create dataset
        writer.create_dataset(location=location_resp.location,
                              annotation_format=self.annotation_format,
                              dataset=self.dataset,
                              workspace_id=self.workspace_id,
                              project_name=self.project_name)

    def _test_get_ds(self):
        test_data = []
        import pandas as pd
        ds = ray.data.from_pandas(pd.DataFrame(test_data))
        return ds


def main(args):
    pipeline = ExportCocoPipeline(args)
    pipeline.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--q",
        dest="q",
        required=True,
        default="",
        help="Mongo query sql",
    )

    parser.add_argument(
        "--annotation-format",
        dest="annotation_format",
        required=True,
        default="",
        help="Annotation format. Example: Unannotated, Coco",
    )

    parser.add_argument(
        "--annotation-set-name",
        dest="annotation_set_name",
        required=True,
        default="",
        help="Annotation set name, example: as01",
    )
    parser.add_argument(
        "--export-to",
        dest="export_to",
        required=True,
        default="dataset",
        help="dataset or filesystem",
    )
    parser.add_argument(
        "--dataset",
        dest="dataset",
        required=False,
        default="",
        help="create dataset request",
    )

    parser.add_argument(
        "--merge-labels",
        dest="merge_labels",
        required=False,
        default="",
        help="need merge label,key is dest label, value is need merge labels",
    )

    parser.add_argument(
        "--mongo-host",
        dest="mongo_host",
        required=True,
        default="10.27.240.45",
        help="mongo host",
    )

    parser.add_argument(
        "--mongo-port",
        dest="mongo_port",
        required=True,
        default="8718",
        help="mongo port",
    )

    parser.add_argument(
        "--mongo-user",
        dest="mongo_user",
        required=True,
        default="root",
        help="mongo user",
    )

    parser.add_argument(
        "--mongo-password",
        dest="mongo_password",
        required=True,
        default="",
        help="mongo password",
    )

    parser.add_argument(
        "--mongo-db",
        dest="mongo_database",
        required=True,
        default="",
        help="mongo database",
    )

    parser.add_argument(
        "--mongo-collection",
        dest="mongo_collection",
        required=True,
        default="",
        help="mongo collection",
    )

    parser.add_argument(
        "--windmill-endpoint",
        dest="windmill_endpoint",
        required=True,
        default="",
        help="windmill endpoint",
    )

    parser.add_argument(
        "--windmill-ak",
        dest="windmill_ak",
        required=True,
        default="",
        help="windmill ak",
    )

    parser.add_argument(
        "--windmill-sk",
        dest="windmill_sk",
        required=True,
        default="",
        help="windmill sk",
    )

    parser.add_argument(
        "--filesystem-name",
        dest="filesystem_name",
        required=True,
        default="",
        help="filesystem name",
    )

    parser.add_argument(
        "--job-name",
        dest="job_name",
        required=True,
        default="",
        help="windmill job name",
    )

    parser.add_argument(
        "--vistudio-endpoint",
        dest="vistudio_endpoint",
        required=True,
        default="http://10.27.240.49:8322",
        help="vistudio annotation endpoint",
    )


    args = parser.parse_args()
    main(args)