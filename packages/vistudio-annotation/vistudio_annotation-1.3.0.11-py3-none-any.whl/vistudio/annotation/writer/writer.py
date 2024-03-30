#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   writer.py
"""
from typing import Dict, Any, Optional
from pyarrow._s3fs import S3FileSystem
from ray.data.datasource import FilenameProvider
import ray.data
from ray.data.block import Block
from windmilltrainingv1.client.training_client import TrainingClient
from windmillartifactv1.client.artifact_client import ArtifactClient
from vistudio.annotation.config.config import Config
from logit.base_logger import setup_logger
setup_logger({})
import logit

ANNOTATION_FORMAT_COCO = 'COCO'
ANNOTATION_FORMAT_IMAGENET = 'ImageNet'
ANNOTATION_FORMAT_CITYSCAPES = 'Cityscapes'

class Writer(object):
    """
    Write annotation file
    """
    def __init__(self,
                 config: Config
                 ):
        self.config = config
        s3_config_dict = {
            "ak": self.config.s3_ak,
            "sk": self.config.s3_sk,
            "region": "bj",
            "host": self.config.s3_host,
            "disableSSL": self.config.disableSSL
        }
        self.s3_bucket = self.config.s3_endpoint.split("/")[0]
        self.artifact_client = ArtifactClient(
            endpoint=self.config.windmill_endpoint,
            ak=self.config.windmill_ak,
            sk=self.config.windmill_sk
        )
        self.train_client = TrainingClient(
            endpoint=self.config.windmill_endpoint,
            ak=self.config.windmill_ak,
            sk=self.config.windmill_sk
        )

        if not self.config.s3_host.startswith("http"):
            if self.config.disableSSL:
                self.pyarrow_fs_endpoint_url = "http://" + self.config.s3_host
            else:
                self.pyarrow_fs_endpoint_url = "https://" + self.config.s3_host

        self.fs = S3FileSystem(
            access_key=self.config.s3_ak,
            secret_key=self.config.s3_sk,
            endpoint_override=self.pyarrow_fs_endpoint_url)

    def write_json(self,
                   ds: ray.data.dataset,
                   path: str,
                   partition_num: int = None,
                   filename_provider: Optional[FilenameProvider] = None,
                   ):
        """
        Write json file
        """
        if partition_num is None:
            ds.write_json(path=path, filesystem=self.fs, filename_provider=filename_provider)
        else:
            ds.repartition(partition_num).write_json(path=path, filesystem=self.fs, filename_provider=filename_provider)

    def write_csv_without_header(self,
                   ds: ray.data.dataset,
                   path: str,
                   partition_num: int = None,
                   filename_provider: Optional[FilenameProvider] = None,
                   ):
        """
        Write csv file
        """
        from pyarrow import csv
        if partition_num is None:
            ds.write_csv(path, filesystem=self.fs,
                         filename_provider=filename_provider,
                         arrow_csv_args_fn=lambda: {
                                "write_options": csv.WriteOptions(
                                    include_header=False,
                                )})
        else:
            ds.repartition(partition_num).write_csv(path=path,
                                                     filesystem=self.fs,
                                                     filename_provider=filename_provider,
                                                     arrow_csv_args_fn=lambda: {
                                                         "write_options": csv.WriteOptions(
                                                             include_header=False,
                                                         )}
                                                     )

    def create_location(self, object_name: str):
        """
        create location
        :param object_name:
        :return:
        """
        # 创建位置
        location_resp = self.artifact_client.create_location(
            object_name=object_name
        )
        return location_resp

    def create_dataset(self, location,
                       annotation_format,
                       dataset,
                       workspace_id,
                       project_name):
        """
        create dataset
        :param location:
        :param annotation_format:
        :param dataset:
        :param workspace_id:
        :param project_name:
        :return:
        """
        # 创建数据集
        artifact = dataset.get('artifact', {})
        if annotation_format == 'coco':
            annotation_format = ANNOTATION_FORMAT_COCO
        elif annotation_format == 'cityscapes':
            annotation_format = ANNOTATION_FORMAT_CITYSCAPES
        elif annotation_format == 'imagenet':
            annotation_format = ANNOTATION_FORMAT_IMAGENET
        dataset_resp = self.train_client.create_dataset(
            workspace_id=dataset.get("workspaceID"),
            project_name=dataset.get("projectName"),
            category=dataset.get("category", "Image/ObjectDetecton"),
            local_name=dataset.get("localName"),
            artifact_uri=location,
            description=dataset.get('description', ''),
            display_name=dataset.get('displayName', ''),
            data_type=dataset.get('dataType', 'Image'),
            annotation_format=annotation_format,
            artifact_description=artifact.get('description', ''),
            artifact_alias=artifact.get('alias', []),
            artifact_tags=artifact.get('tags', []),
            artifact_metadata={'paths': [location + "/"]},
        )
        logit.info("create dataset resp is {}".format(dataset_resp))


class ImageFilenameProvider(FilenameProvider):
    """
    ImageFilenameProvider,Generates filenames when you write a :class:`~ray.data.Dataset
    """

    def get_filename_for_row(self, row: Dict[str, Any], task_index: int, block_index: int, row_index: int) -> str:
        """
        get_filename_for_row
        :param row:
        :param task_index:
        :param block_index:
        :param row_index:
        :return:
        """
        if self.file_name is None:
            return (
                f"{task_index:06}_{block_index:06}"
                f"_{row_index:06}.{self.file_format}"
            )
        else:
            if self.is_full_file_name:
                return self.file_name
            return (
                f"{task_index:06}_{block_index:06}"
                f"_{row_index:06}_{self.file_name}"
            )

    def __init__(self, file_format: str=None, file_name: str=None, is_full_file_name: bool=False):
        self.file_format = file_format
        self.file_name = file_name
        self.is_full_file_name = is_full_file_name

    def get_filename_for_block(
            self, block: Block, task_index: int, block_index: int
    ) -> str:
        """
        get_filename_for_block
        :param block:
        :param task_index:
        :param block_index:
        :return:
        """
        if self.file_name is None:
            return (
                f"{task_index:06}_{block_index:06}"
                f".{self.file_format}"
            )
        else:
            if self.is_full_file_name:
                return self.file_name
            return (
                f"{task_index:06}_{block_index:06}"
                f"_{self.file_name}"
            )



