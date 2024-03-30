#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
@File    :   thumbnail_generator.py
@Time    :   2024/03/13 16:49:57
@Author  :   <dongling01@baidu.com>
"""

import time
import pandas as pd
from typing import Union, Dict, Any
from ray.data.preprocessor import Preprocessor
from pymongo import MongoClient


class ImageCreatedTimeUpdater(Preprocessor):
    """
    ImageCreatedTimeUpdater
    """

    def __init__(self, config):
        self._is_fittable = True
        self._fitted = True

        self.config = config

    def _get_transform_config(self) -> Dict[str, Any]:
        """Returns kwargs to be passed to :meth:`ray.data.Dataset.map_batches`.

        This can be implemented by subclassing preprocessors.
        """
        return {"batch_size": 1024}

    def _transform_pandas(self, df: "pd.DataFrame") -> "pd.DataFrame":
        """
        _transform_pandas
        :param df:
        :return:
        """
        rows = df.to_dict(orient='records')
        return self._update_annotation_status(rows)

    def _update_annotation_status(self, rows: list):
        """
        get annotation status
        """
        mongo_client = MongoClient(host=self.config.mongodb_host, port=self.config.mongodb_port,
                                   username=self.config.mongodb_user, password=self.config.mongodb_password)
        mongo = mongo_client[self.config.mongodb_database][self.config.mongodb_collection]

        for row in rows:
            query = {
                "image_id": row['image_id'],
                "annotation_set_id": row['annotation_set_id'],
                "data_type": 'Image'
            }
            item = mongo.find_one(query)
            if item is None:
                continue

            update = {
                "$set": {
                    "image_created_at": item.get('created_at'),
                    "updated_at": time.time_ns(),
                }
            }
            query = {
                "image_id": row['image_id'],
                "annotation_set_id": row['annotation_set_id'],
                "data_type": 'Annotation',
            }
            mongo.update_many(query, update)

        return pd.DataFrame(rows)







