#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
@File    :   thumbnail_generator.py
@Time    :   2024/03/13 16:49:57
@Author  :   <dongling01@baidu.com>
"""
import os
import time
import pandas as pd
import re
import io
import logit
from PIL import Image
from typing import Union, Dict, Any
from ray.data.preprocessor import Preprocessor
from windmillcomputev1.client.compute_client import ComputeClient
from windmillcomputev1.filesystem import blobstore
from pymongo import MongoClient

logit.base_logger.setup_logger({})


THUMBNAIL_WIDTH = 158
THUMBNAIL_HEIGHT = 118

as_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/" \
                  r"annotationsets/(?P<annotation_set_name>[^/]+)$"


class ThumbnailGenerator(Preprocessor):
    """
    generate thumbnail
    """

    def __init__(self, config):
        self._is_fittable = True
        self._fitted = True

        self.config = config
        self.compute_client = ComputeClient(endpoint=config.windmill_endpoint,
                                            ak=config.windmill_ak,
                                            sk=config.windmill_sk)
        self.bs_dict = {}

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
        return self._generate_thumbnail(rows)

    def _generate_thumbnail(self, rows: list):
        """
        generate thumbnail
        """
        mongo_client = MongoClient(host=self.config.mongodb_host, port=self.config.mongodb_port,
                                   username=self.config.mongodb_user, password=self.config.mongodb_password)
        mongo = mongo_client[self.config.mongodb_database][self.config.mongodb_collection]

        for row in rows:
            try:
                pj_name = self._get_bs(row['annotation_set_name'])
                bs = self.bs_dict[pj_name]

                file_uri = row['file_uri']
                file_dir, file_name = os.path.split(file_uri)
                thumb_dir = file_dir + "-thumbnail"
                thumb_uri = os.path.join(thumb_dir, file_name)
                ext = os.path.splitext(file_uri)[1][1:]
                ext = ext.lower()

                # read image
                image_bytes = bs.read_raw(path=file_uri)
                image_bytes_io = io.BytesIO(image_bytes)
                img = Image.open(image_bytes_io)
                width, height = img.size

                # resize image
                resized_img = img.resize((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))

                # write thumbnail to s3
                byte_arr = io.BytesIO()
                if ext == 'jpg':
                    resized_img.save(byte_arr, format='jpeg')
                else:
                    resized_img.save(byte_arr, format=ext)
                resize_img_bytes = byte_arr.getvalue()
                bs.write_raw(path=thumb_uri, content_type=f'image/{ext}', data=resize_img_bytes)

                # update mongo
                query = {
                    "image_id": row['image_id'],
                    "annotation_set_id": row['annotation_set_id'],
                    "data_type": "Image"
                }
                update = {
                    "$set": {
                        "image_state": "Completed",
                        "width": width,
                        "height": height,
                        "updated_at": time.time_ns(),
                    }
                }
                c = mongo.update_one(query, update)
                logit.info(f"update count: {c.modified_count}")
                logit.info("generate thumbnail success")

            except Exception as e:
                # update mongo
                query = {
                    "image_id": row['image_id'],
                    "annotation_set_id": row['annotation_set_id'],
                    "data_type": "Image"
                }
                update = {
                    "$set": {
                        "image_state": "Error",
                        "updated_at": time.time_ns(),
                    }
                }
                c = mongo.update_one(query, update)
                logit.info(f"update count: {c.modified_count}")
                logit.error(f"generate thumbnail error: {e}")

        return pd.DataFrame(rows)

    def _get_bs(self, annotation_set_name: str):
        """
        get blob store
        :param annotation_set_name:
        :return:
        """
        match = re.match(as_name_pattern, annotation_set_name)
        as_name = match.groupdict()
        workspace_id = as_name['workspace_id']
        project_name = as_name['project_name']
        pj_name = f"workspaces/{workspace_id}/projects/{project_name}"

        if pj_name not in self.bs_dict:
            fs = self.compute_client.suggest_first_filesystem(workspace_id=workspace_id, guest_name=pj_name)
            self.bs_dict[pj_name] = blobstore(filesystem=fs)
        return pj_name


