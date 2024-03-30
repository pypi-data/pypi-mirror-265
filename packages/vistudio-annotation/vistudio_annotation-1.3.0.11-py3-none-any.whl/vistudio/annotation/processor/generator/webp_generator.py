#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
@File    :   webp_generator.py
@Time    :   2024/03/13 16:49:57
@Author  :   <dongling01@baidu.com>
"""
import os
import pandas as pd
import re
from typing import Union, Dict, Any
from ray.data.preprocessor import Preprocessor
from windmillcomputev1.client.compute_client import ComputeClient
from windmillcomputev1.filesystem import blobstore
import logit


as_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/" \
                  r"annotationsets/(?P<annotation_set_name>[^/]+)$"
Boundary_Size = 2 * 1024 * 1024


class WebpGenerator(Preprocessor):
    """
    generate webp
    """

    def __init__(self, config):
        self._is_fittable = True
        self._fitted = True
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
        return self._generate_webp(rows)

    def _generate_webp(self, rows: list):
        """
        generate webp
        """
        for row in rows:
            try:
                pj_name = self._get_bs(row['annotation_set_name'])
                bs = self.bs_dict[pj_name]

                file_uri = row['file_uri']
                file_dir, file_name = os.path.split(file_uri)
                ext = os.path.splitext(file_uri)[1]
                webp_dir = file_dir + "-webp"
                webp_filename = file_name.replace(ext, '.webp')
                webp_uri = os.path.join(webp_dir, webp_filename)

                # read image
                image_bytes = bs.read_raw(path=file_uri)

                # write webp to s3
                size = len(image_bytes)
                if size > Boundary_Size:
                    bs.write_raw(path=webp_uri, content_type='image/webp', data=image_bytes)

            except Exception as e:
                logit.error(f"generate webp error: {e}")

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




