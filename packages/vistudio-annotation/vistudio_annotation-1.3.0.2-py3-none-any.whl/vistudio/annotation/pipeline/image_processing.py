#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
image_aggregation.py
"""
import os
import logit
import pyarrow as pa
from pymongoarrow.api import Schema
from ray.data.datasource.datasource import Datasource
from ray.data.read_api import read_datasource

from vistudio.annotation.datasource.sharded_mongo_datasource import ShardedMongoDatasource
from vistudio.annotation.processor.generator.thumbnail_generator import ThumbnailGenerator
from vistudio.annotation.processor.generator.webp_generator import WebpGenerator
from vistudio.annotation.config.config import Config

logit.base_logger.setup_logger({})


class ImageProcessingPipeline(object):
    """
    process image
    """

    def __init__(self, config, parallelism):
        self.config = config
        self.parallelism = parallelism

    def run(self):
        """
        run this piepline
        """
        # 第一步 查找Init的图像
        mongo_param = {
            "pipeline": [
                {"$match": {
                    "data_type": "Image",
                    "image_state": "Init",
                }},
                { "$sort": { "created_at": -1 } },
                { "$limit": 10000 }
            ],
            "schema": Schema({"image_id": pa.string(),
                              "annotation_set_id": pa.string(),
                              "annotation_set_name": pa.string(),
                              "file_uri": pa.string()})
        }
        datasource = self._get_mongo_datasource(config=self.config, params=mongo_param)
        ds = read_datasource(datasource, parallelism=self.parallelism)
        if ds.count() <= 0:
            return False

        # 第二步 转换图像
        thumb_generator = ThumbnailGenerator(self.config)
        jpeg_ds = thumb_generator.transform(ds)

        webp_generator = WebpGenerator(self.config)
        webp_ds = webp_generator.transform(ds)

        process_ds = jpeg_ds.union(webp_ds)
        print(process_ds.take_all())

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

    # windmill
    config.windmill_endpoint = os.environ.get('WINDMILL_ENDPOINT', "http://10.27.240.45:8340")
    config.windmill_ak = os.environ.get('WINDMILL_AK', "1cb1860b8bc848298050edffa2ef9e16")
    config.windmill_sk = os.environ.get('WINDMILL_SK', "51a7a74c9ef14063a6892d08dd19ffbf")

    pipeline = ImageProcessingPipeline(config=config, parallelism=10)
    result = pipeline.run()
    print('result:', result)

if __name__ == '__main__':
    main()

