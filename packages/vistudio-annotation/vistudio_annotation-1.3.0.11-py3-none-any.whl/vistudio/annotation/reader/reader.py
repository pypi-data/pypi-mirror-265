#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
reader.py
"""
import os
import ray
from typing import List, Union, Dict
from pyarrow.fs import S3FileSystem
from pymongo import MongoClient
from ray.data.dataset import Dataset
from windmillcomputev1.filesystem import S3BlobStore
from vistudio.annotation.config.config import Config

image_extensions = ('.jpeg', '.jpg', '.png', '.bmp')


class CocoReader(object):
    """
    CocoReader ,use this reader to read json file
    """
    def __init__(self,
                 config: Config,
                 annotation_set_id: str = None,
                 ):
        self.config = config
        self.annotation_set_id = annotation_set_id

        self.s3_bucket = config.s3_endpoint.split("/")[0]

        # 初始化blobstore
        s3_config_dict = {
            "ak": config.s3_ak,
            "sk": config.s3_sk,
            "region": "bj",
            "host": config.s3_host,
            "disableSSL": config.disableSSL
        }
        self.bs = S3BlobStore(endpoint=self.s3_bucket, config=s3_config_dict)

        if not config.s3_host.startswith("http"):
            if config.disableSSL:
                pyarrow_fs_endpoint_url = "http://" + config.s3_host
            else:
                pyarrow_fs_endpoint_url = "https://" + config.s3_host
        self.fs = S3FileSystem(access_key=config.s3_ak,
                               secret_key=config.s3_sk,
                               endpoint_override=pyarrow_fs_endpoint_url,
                               region="bj")

        # 初始化数据库
        self.mongodb = self._mongodb_collection(host=config.mongodb_host,
                                                port=config.mongodb_port,
                                                username=config.mongodb_user,
                                                password=config.mongodb_password,
                                                database=config.mongodb_database,
                                                collection=config.mongodb_collection)

    @staticmethod
    def _mongodb_collection(host='localhost', port=8717, username='root', password='',
                            database='vistudio', collection='annotation'):
        """
        初始化mongodb连接
        """
        mongo_client = MongoClient(host=host, port=port, username=username, password=password)
        mongo_db = mongo_client[database][collection]
        return mongo_db

    def _get_filenames(self, file_uri, layer):
        """
        :param file_uri: s3地址
        :param layer: 遍历的层数
        :return: 文件filename列表
        """
        filenames = []
        dest_path = file_uri.split(self.s3_bucket + '/')[1]
        if not dest_path.endswith("/"):
            dest_path += "/"
        dest_parts = dest_path.split('/')[:-1]

        file_list = self.bs.list_meta(dest_path)
        for file in file_list:
            f_path = file.url_path.split(self.s3_bucket + '/')[1]
            f_parts = f_path.split('/')[:-1]
            # 此处表示取文件夹3层内的数据
            if len(f_parts) - len(dest_parts) > layer:
                continue
            filename = "s3://" + os.path.join(self.s3_bucket, f_path)
            filenames.append(filename)

        return filenames

    def get_annoation_fileuris(self, data_uri) -> list():
        """
        get annoation file uris by data_uri
        :param data_uri:
        :return: list
        """
        annotation_file_uri = data_uri
        # 获取全部要处理的标注文件
        ext = os.path.splitext(annotation_file_uri)[1].lower()
        if ext == "":
            filenames = self._get_filenames(annotation_file_uri, 0)
        else:
            filenames = [annotation_file_uri]

        file_uris = list()
        for filename in filenames:
            if not filename.lower().endswith('.json'):
                continue
            file_uris.append(filename)

        return file_uris

    def _get_exist_fileuris(self):
        """
        获取当前标注集已有的图像名称 file_name
        :return:
        """
        exist_images_set = set()
        query = {
            "annotation_set_id": self.annotation_set_id,
            "data_type": "Image"
        }
        exist_images = self.mongodb.find(query, ["image_name"])
        for image in exist_images:
            if "image_name" in image:
                exist_images_set.add(image["image_name"])
        return exist_images_set

    def get_image_fileuris(self, data_uri) -> list():
        """
        get image file uris by data_uri
        :param data_uri:
        :return:
        """
        image_uri = data_uri

        ext = os.path.splitext(image_uri)[1].lower()
        if ext == "":
            filenames = self._get_filenames(image_uri, 2)
        else:
            filenames = [image_uri]

        # 获取该标注集已有的图像名称
        exist_images_set = self._get_exist_fileuris()

        # 插入图像
        file_uris = list()
        for filename in filenames:
            if not filename.lower().endswith(image_extensions):
                continue

            _, file_name = os.path.split(filename)
            if file_name in exist_images_set:
                continue
            file_uris.append(filename)

        return file_uris

    def get_file_uris(self, data_uri: str, data_types: list()) -> list():
        """
        get file uris by data uri
        :param data_uri:
        :param data_types:
        :return:
        """
        if len(data_types) == 1 and data_types[0] == "annotation":
            file_uris = self.get_annoation_fileuris(data_uri)

        elif len(data_types) == 1 and data_types[0] == "image":
            file_uris = self.get_image_fileuris(data_uri)

        elif len(data_types) == 2 and "image" in data_types and "annotation" in data_types:
            anno_uri = os.path.join(data_uri, "annotations")

            # 获取所有的图片 和文件 uri
            file_uris = self.get_annoation_fileuris(data_uri=anno_uri)

        return file_uris

    def read_json(self, file_uris: List[str]) -> Dataset:
        """
        read json
        :param file_uris:
        :return: Dataset
        """
        ds = ray.data.read_json(paths=file_uris, filesystem=self.fs)
        return ds


class VistudioReader(object):
    """
       VistudioReader ,use this reader to read json file
       """

    def __init__(self,
                 config: Config,
                 annotation_set_id: str = None,
                 ):
        self.config = config
        self.annotation_set_id = annotation_set_id

        self.s3_bucket = config.s3_endpoint.split("/")[0]

        # 初始化blobstore
        s3_config_dict = {
            "ak": config.s3_ak,
            "sk": config.s3_sk,
            "region": "bj",
            "host": config.s3_host,
            "disableSSL": config.disableSSL
        }
        self.bs = S3BlobStore(endpoint=self.s3_bucket, config=s3_config_dict)

        if not config.s3_host.startswith("http"):
            if config.disableSSL:
                pyarrow_fs_endpoint_url = "http://" + config.s3_host
            else:
                pyarrow_fs_endpoint_url = "https://" + config.s3_host
        self.fs = S3FileSystem(access_key=config.s3_ak,
                               secret_key=config.s3_sk,
                               endpoint_override=pyarrow_fs_endpoint_url,
                               region="bj")

        # 初始化数据库
        self.mongodb = self._mongodb_collection(host=config.mongodb_host,
                                                port=config.mongodb_port,
                                                username=config.mongodb_user,
                                                password=config.mongodb_password,
                                                database=config.mongodb_database,
                                                collection=config.mongodb_collection)

    def _get_filenames(self, file_uri, layer):
        """
        :param file_uri: s3地址
        :param layer: 遍历的层数
        :return: 文件filename列表
        """
        filenames = []
        dest_path = file_uri.split(self.s3_bucket + '/')[1]
        if not dest_path.endswith("/"):
            dest_path += "/"
        dest_parts = dest_path.split('/')[:-1]

        file_list = self.bs.list_meta(dest_path)
        for file in file_list:
            f_path = file.url_path.split(self.s3_bucket + '/')[1]
            f_parts = f_path.split('/')[:-1]
            # 此处表示取文件夹3层内的数据
            if len(f_parts) - len(dest_parts) > layer:
                continue
            filename = "s3://" + os.path.join(self.s3_bucket, f_path)
            filenames.append(filename)

        return filenames

    @staticmethod
    def _mongodb_collection(host='localhost', port=8717, username='root', password='',
                            database='vistudio', collection='annotation'):
        """
        初始化mongodb连接
        """
        mongo_client = MongoClient(host=host, port=port, username=username, password=password)
        mongo_db = mongo_client[database][collection]
        return mongo_db

    def get_annoation_fileuris(self, data_uri) -> list():
        """
        get annoation file uris by data_uri
        :param data_uri:
        :return: list
        """
        annotation_file_uri = data_uri
        # 获取全部要处理的标注文件
        ext = os.path.splitext(annotation_file_uri)[1].lower()
        if ext == "":
            filenames = self._get_filenames(annotation_file_uri, 0)
        else:
            filenames = [annotation_file_uri]

        file_uris = list()
        for filename in filenames:
            if not filename.lower().endswith('.json') and not filename.lower().endswith('.jsonl'):
                continue
            file_uris.append(filename)

        return file_uris

    def _get_exist_fileuris(self):
        """
        获取当前标注集已有的图像名称 file_name
        :return:
        """
        exist_images_set = set()
        query = {
            "annotation_set_id": self.annotation_set_id,
            "data_type": "Image"

        }
        exist_images = self.mongodb.find(query, ["file_uri"])
        for image in exist_images:
            exist_images_set.add(image["file_uri"])
        return exist_images_set

    def get_image_fileuris(self, data_uri) -> list():
        """
        get image file uris by data_uri
        :param data_uri:
        :return:
        """
        image_uri = data_uri

        ext = os.path.splitext(image_uri)[1].lower()
        if ext == "":
            filenames = self._get_filenames(image_uri, 2)
        else:
            filenames = [image_uri]

        # 获取该标注集已有的图像名称
        exist_images_set = self._get_exist_fileuris()

        # 插入图像
        file_uris = list()
        for filename in filenames:
            if not filename.lower().endswith(image_extensions):
                continue

            _, file_name = os.path.split(filename)
            if file_name in exist_images_set:
                continue
            file_uris.append(filename)

        return file_uris

    def get_file_uris(self, data_uri: str, data_types: list()) -> list():
        """
        get file uris by data uri
        :param data_uri:
        :param data_types:
        :return:
        """
        if len(data_types) == 1 and data_types[0] == "annotation":
            file_uris = self.get_annoation_fileuris(data_uri)

        elif len(data_types) == 1 and data_types[0] == "image":
            file_uris = self.get_image_fileuris(data_uri)

        elif len(data_types) == 2 and "image" in data_types and "annotation" in data_types:
            anno_uri = os.path.join(data_uri, "jsonl")

            # 获取所有的图片 和文件 uri
            file_uris = self.get_annoation_fileuris(data_uri=anno_uri)

        return file_uris

    def read_json(self, file_uris: List[str]) -> Dataset:
        """
        read json
        :param file_uris:
        :return: Dataset
        """
        ds = ray.data.read_json(paths=file_uris, filesystem=self.fs)
        return ds