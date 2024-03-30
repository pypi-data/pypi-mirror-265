#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
export_pipeline.py
"""
import sys
import os
__work_dir__ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, __work_dir__)

from vistudio.annotation.pipeline.base_import_pipeline import BaseImportPipline
from vistudio.annotation.processor.importer.image.image_formatter import ImageUriFormatter
from vistudio.annotation.processor.importer.annoation.vistudio_formatter import VistudioFormatter
from vistudio.annotation.reader.reader import VistudioReader
import ray
import argparse
import logit

image_extensions = ('.jpeg', '.jpg', '.png', '.bmp')
job_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/jobs/(?P<job_name>[^/]+)$"
annotationset_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/annotationsets/" \
                             r"(?P<annotationset_local_name>[^/]+)$"

fs_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/filesystems/(?P<filesystems_name>[^/]+)$"


class ImportVistudioPipeline(BaseImportPipline):
    """
        标注格式转换类
        :param param_dict: 公共的字段
        :param annotation_file_path: 标注文件本地路径
        :param image_uri: 图像s3地址
        :param image_path: 图像本地路径
        :param annotation_format: 标注格式
        """

    def __init__(self,
                 args,
                 ):
        super().__init__(args)

    def _import_annoation(self):
        """
        导入标注文件
        :return:
        """

        # 读取json 文件
        vistudio_reader = VistudioReader(config=self.config)
        file_uris = vistudio_reader.get_file_uris(data_uri=self.data_uri, data_types=self.data_types)
        ds = vistudio_reader.read_json(file_uris)
        logit.info("import annotation from vistudio.dataset count = {}".format(ds.count()))

        if len(self.data_types) == 2 and "image" in self.data_types and "annotation" in self.data_types:
            image_uri_prefix = os.path.join(self.data_uri, "images")
        else:
            image_uri_prefix = self.data_uri
        # 处理 ds
        vistudio_formater = VistudioFormatter(config=self.config,
                                              labels=self.labels,
                                              user_id=self.user_id,
                                              annotation_set_id=self.annotation_set_id,
                                              annotation_set_name=self.annotation_set_name,
                                             )
        final_ds = vistudio_formater.fit(ds).stats_
        logit.info("format dataset.dataset count = {}".format(final_ds.count()))
        # 数据入库
        final_ds.write_mongo(uri=self.mongo_uri,
                             database=self.config.mongodb_database,
                             collection=self.config.mongodb_collection)

    def _import_image(self):
        """
        导入图片
        :return:
        """
        vistudio_reader = VistudioReader(config=self.config,annotation_set_id=self.annotation_set_id)
        file_uris = vistudio_reader.get_file_uris(data_uri=self.data_uri, data_types=self.data_types)

        ds = ray.data.from_items(file_uris)
        logit.info("import vistudio image from json.dataset count = {}".format(ds.count()))

        image_formater = ImageUriFormatter(config=self.config,
                                           annotation_set_id=self.annotation_set_id,
                                           user_id=self.user_id,
                                           annotation_set_name=self.annotation_set_name)
        final_ds = image_formater.fit(ds).stats_
        logit.info("format dataset.dataset count = {}".format(final_ds.count()))
        # 写入数据
        final_ds.write_mongo(uri=self.mongo_uri,
                                   database=self.config.mongodb_database,
                                   collection=self.config.mongodb_collection)

    def run(self):
        """
        run this piepline
        :return:
        """
        if len(self.data_types) == 1 and self.data_types[0] == "annotation":
            self._import_annoation()

        elif len(self.data_types) == 1 and self.data_types[0] == "image":
            self._import_image()

        elif len(self.data_types) == 2 and "image" in self.data_types and "annotation" in self.data_types:
            self._import_annoation()
        else:
            raise Exception("The data_types: '{}' is not support.".format(self.data_types))


def main(args):
    pipeline = ImportVistudioPipeline(args)
    pipeline.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-uri",
        dest="data_uri",
        required=True,
        default="",
        help="Only Image、Only Annotation、Image + Annotation",
    )
    parser.add_argument(
        "--annotation-format",
        dest="annotation_format",
        required=False,
        default="",
        help="Annotation format. Example: Coco",
    )
    parser.add_argument(
        "--data-types",
        dest="data_types",
        required=True,
        default="",
        help="Data type. Example: image,annotation",
    )

    parser.add_argument(
        "--annotation-set-name",
        dest="annotation_set_name",
        required=True,
        default="",
        help="Annotation set id, example: as01",
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
        default="",
        help="vistudio annotation endpoint",
    )


    args = parser.parse_args()
    main(args)