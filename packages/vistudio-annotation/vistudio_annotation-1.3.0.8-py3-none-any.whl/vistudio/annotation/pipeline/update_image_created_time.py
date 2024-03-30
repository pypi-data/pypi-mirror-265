#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""

"""
import os
import pyarrow as pa
from ray.data.datasource.datasource import Datasource
from ray.data.read_api import read_datasource
from pymongoarrow.api import Schema
from vistudio.annotation.datasource.sharded_mongo_datasource import ShardedMongoDatasource
from vistudio.annotation.processor.updater.image_created_time_updater import ImageCreatedTimeUpdater
from vistudio.annotation.config.config import Config


class UpdateImageCreatedTimePipeline(object):
    """
    update image created time
    """

    def __init__(self, config, parallelism):
        self.config = config
        self.parallelism = parallelism

    def run(self):
        """
        run this piepline
        """
        # 第1步 拿到image_created_at为0的数据
        mongo_param = {
            "pipeline": [
                { "$match": {
                    "data_type": "Annotation",
                    "image_created_at": 0,
                } },
                { "$sort": { "created_at": -1 } },
                {"$limit": 10000}
            ],
            "schema": Schema({"image_id": pa.string(), "annotation_set_id": pa.string()})
        }
        datasource = self._get_mongo_datasource(config=self.config, params=mongo_param)
        ds = read_datasource(datasource, parallelism=self.parallelism)
        if ds.count() <= 0:
            return False

        # 第2步 找到image的created_at，更新annotation的image_created_at
        update_anno_status = ImageCreatedTimeUpdater(config=self.config)
        u_ds = update_anno_status.transform(ds)
        print(u_ds.take_all())

        return True

    @staticmethod
    def _get_mongo_datasource(config: Config, params: dict) -> Datasource:
        """
        get mongo datasource
        :param config:
        :param params:
        :return: Datasource
        """
        uri = "mongodb://{}:{}@{}:{}".format(config.mongodb_user,
                                             config.mongodb_password,
                                             config.mongodb_host,
                                             config.mongodb_port)
        db_name = config.mongodb_database
        collection_name = config.mongodb_collection

        source = ShardedMongoDatasource(
            uri=uri,
            database=db_name,
            collection=collection_name,
            pipeline=params['pipeline'],
            schema=params['schema'],
        )
        return source


def main():
    """
    main function
    :return:
    """
    config = Config()
    # mongodb
    config.mongodb_host = os.environ.get('MONGO_HOST', '10.27.240.45')
    config.mongodb_port = int(os.environ.get('MONGO_PORT', 8718))
    config.mongodb_user = os.environ.get('MONGO_USER', 'root')
    config.mongodb_password = os.environ.get('MONGO_PASSWORD', 'mongo123#')
    config.mongodb_database = os.environ.get('MONGO_DB', 'annotation')
    config.mongodb_collection = os.environ.get('MONGO_COLLECTION', 'annotationitems')
    pipeline = UpdateImageCreatedTimePipeline(config=config, parallelism=10)
    result = pipeline.run()
    print('result:', result)

if __name__ == '__main__':
    main()






