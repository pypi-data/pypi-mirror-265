#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File :   ImageUriFormatter.py
"""
import time
import os
from ray.data.preprocessor import Preprocessor
from ray.data import Dataset
from vistudio.annotation.util import annotation_util
from vistudio.annotation.config.config import Config

time_pattern = "%Y-%m-%dT%H:%M:%SZ"


class ImageUriFormatter(Preprocessor):
    """
    ImageUriFormater , use this Preprocessor to add column
    """
    def __init__(self,
                 config: Config,
                 annotation_set_id: str,
                 user_id: str,
                 annotation_set_name: str,):
        self._is_fittable = True
        self.config = config
        self.annotation_set_id = annotation_set_id
        self.user_id = user_id
        self.annotation_set_name = annotation_set_name

    def _fit(self, ds: "Dataset") -> "Preprocessor":
        """
        _fit
        :param ds:
        :return: Preprocessor
        """
        added_ds = ds.add_column("annotation_set_id", lambda df: self.annotation_set_id)\
            .add_column("user_id", lambda df: self.user_id)\
            .add_column("image_state", lambda df: "Init")\
            .add_column("data_type", lambda df: "Image")\
            .add_column("file_uri", lambda df: df['item'])\
            .add_column("width", lambda df: 0)\
            .add_column("height", lambda df: 0)\
            .add_column("image_name", lambda df: os.path.basename(df['item'][0]))\
            .add_column("image_id", lambda df: annotation_util.generate_md5(os.path.basename(df['item'][0])))\
            .add_column("created_at", lambda df: time.time_ns())\
            .add_column("annotation_set_name", lambda df: self.annotation_set_name) \
            .add_column("annotation_state", lambda df: "Init")
        final_ds = added_ds.drop_columns(cols=['item'])
        self.stats_ = final_ds
        return self





