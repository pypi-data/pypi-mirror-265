#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File :   formater.py
"""
import pyarrow as pa
import  pandas as pd
import os
import logit
import re
import ray
import time
from typing import Union, Dict, Any, List
from windmilltrainingv1.client.training_client import TrainingClient
from ray.data.preprocessor import Preprocessor
from ray.data import Dataset
from vistudio.annotation.util import annotation_util
from vistudio.annotation.config.config import Config
import logit


image_extensions = ('.jpeg', '.jpg', '.png', '.bmp')
job_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/jobs/(?P<job_name>[^/]+)$"
time_pattern = "%Y-%m-%dT%H:%M:%SZ"


class VistudioFormatter(Preprocessor):
    """
    use this Preprocessor to handle dataset
    """
    def __init__(self,
                 config: Config,
                 labels: Union[Dict] = dict,
                 user_id: str = None,
                 annotation_set_id: str = None,
                 annotation_set_name: str = None,
                ):
        self.config = config
        self._is_fittable = True
        self.labels = {v: int(k) for k, v in labels.items()}
        self.user_id = user_id
        self.annotation_set_id = annotation_set_id
        self.annotation_set_name = annotation_set_name

        # 初始化train client
        self.train_client = TrainingClient(endpoint=config.windmill_endpoint,
                                           ak=config.windmill_ak,
                                           sk=config.windmill_sk)



        self.exist_image_names = self._get_exist_filenames()  # 已经存在的图片，用于过滤
        self.exist_annotations = self._get_exist_annoation()  # 已经存在的标注，用于过滤

    @staticmethod
    def _mongodb_collection(host='localhost', port=8717, username='root', password='',
                           database='vistudio', collection='annotationitems'):
        """
        初始化mongodb连接
        """
        from pymongo import MongoClient
        mongo_client = MongoClient(host=host, port=port, username=username, password=password)
        mongo_db = mongo_client[database][collection]
        return mongo_db

    def _get_exist_filenames(self):
        """
        获取当前标注集已有的图像名称 file_name
        :return:
        """
        mongodb = self._mongodb_collection(host=self.config.mongodb_host,
                                                port=self.config.mongodb_port,
                                                username=self.config.mongodb_user,
                                                password=self.config.mongodb_password,
                                                database=self.config.mongodb_database,
                                                collection=self.config.mongodb_collection)

        exist_images_set = set()
        query = {
            "annotation_set_id": self.annotation_set_id,
            "data_type": "Image"
        }
        exist_images = mongodb.find(query, ["image_name"])
        for image in exist_images:
            exist_images_set.add(image["image_name"])

        return exist_images_set

    def _get_exist_annoation(self):
        """
        获取当前标注集已有的标注信息
        :return:
        """
        mongodb = self._mongodb_collection(host=self.config.mongodb_host,
                                           port=self.config.mongodb_port,
                                           username=self.config.mongodb_user,
                                           password=self.config.mongodb_password,
                                           database=self.config.mongodb_database,
                                           collection=self.config.mongodb_collection)
        exist_annoation_set = set()
        query = {
            "annotation_set_id": self.annotation_set_id,
            "data_type": "Annotation"
        }
        exist_anno = mongodb.find(query, ["image_id"])
        for anno in exist_anno:
            exist_annoation_set.add(anno["image_id"])
        return exist_annoation_set


    @staticmethod
    def _flat(row: Dict[str, Any], col: str) -> List[Dict[str, Any]]:
        """
         Expand the col column
        :param col:
        :return: List
        """
        #ray.util.pdb.set_trace()
        return row[col]

    @staticmethod
    def _filter_exist_images(row: Dict[str, Any], exist_fileuris: set()):
        """
        if row['filename'] in exist_fileuris, drop this row
        :param row:
        :param exist_fileuris:
        :return:
        """
        return os.path.basename(row["file_name"])not in exist_fileuris

    @staticmethod
    def _filter_exist_annoation(row: Dict[str, Any], exist_image_ids: list()):
        """
        if row['image_id'] not in exist_image_ids, drop this row
        :param row:
        :param exist_image_ids:
        :return:
        """
        return row["image_id"] in exist_image_ids

    @staticmethod
    def _filter_exist_labels(row: Dict[str, Any], labels: Union[Dict] = dict):
        """
        if row['name'] in labels, drop this row
        :param row:
        :param labels:
        :return:
        """
        return row["name"] not in labels.values()

    def _fit(self, ds: "Dataset") -> "Preprocessor":
        """
        fit coco dataset
        :param ds:
        :return: Preprocessor
        """
        final_anno_ds = self._fit_vistudio(ds)
        self.stats_ = final_anno_ds
        return self

    def _fill_image_info_vistudio(self, row: Dict[str, Any]):
        """
        fill vistudio image info
        :param row:
        :return:
        """
        row['annotation_set_id'] = self.annotation_set_id
        row['user_id'] = self.user_id
        row['created_at'] = time.time_ns()
        row['data_type'] = 'Image'
        row['annotation_state'] = 'Init'
        row['image_state'] = 'Init'
        row['annotation_set_name'] = self.annotation_set_name
        row['file_uri'] = row['file_uri']

        return row

    def _update_annotation_job(self, err_msg):
        """
        更新标注任务状态
        """
        job_name = self.config.job_name
        logit.info("update job name is {}".format(job_name))
        match = re.match(job_name_pattern, job_name)
        job_name_dict = match.groupdict()
        update_job_resp = self.train_client.update_job(
            workspace_id=job_name_dict["workspace_id"],
            project_name=job_name_dict["project_name"],
            local_name=job_name_dict["job_name"],
            tags={"errMsg": err_msg},
        )
        logit.info("update job resp is {}".format(update_job_resp))

    @staticmethod
    def _parse_vistudio_anno_topyarrow(row: Dict[str, Any]) -> Dict[str, Any]:
        if row['type'] == 'annotation':
            df = pd.DataFrame(row["annotations"])

            # 将 Pandas DataFrame 转换为 PyArrow 表
            arrow_table = pa.Table.from_pandas(df)
            row["annotations"] = arrow_table
            return row
        else:
            return row

    def _fit_vistudio(self,  ds: "Dataset") -> Dataset:
        """
        _fit
        :param ds:
        :return: Preprocessor
        """
        df = ds.to_pandas()
        image_ds = ds.filter(lambda row: row["data_type"] == 'Image')
        logit.info("import vistudio flat image.image_ds count={}".format(image_ds.count()))
        final_image_ds = None
        if image_ds.count() > 0:
            added_image_ds = image_ds\
                .add_column("image_id", lambda df: annotation_util.generate_md5(df['image_name'][0]))
            final_image_ds = added_image_ds.map(lambda row: self._fill_image_info_vistudio(row=row))

        anno_filtered_df = df[df['data_type'] == 'Annotation']
        anno_ds = ray.data.from_pandas(anno_filtered_df)
        logit.info("import vistudio flat image.anno_ds count={}".format(anno_ds.count()))
        final_annotation_ds = None
        if anno_ds.count() > 0:
            anno_schema_names = anno_ds.schema().names
            if "width" in anno_schema_names and "height" in anno_schema_names and "file_uri" in anno_schema_names:
                droped_anno_ds = anno_ds.drop_columns(cols=['width', 'height', 'file_uri'])
            else:
                droped_anno_ds = anno_ds

            now = time.time_ns()

            final_annotation_ds = droped_anno_ds\
                .add_column("annotation_set_id", lambda df: self.annotation_set_id)\
                .add_column("user_id", lambda df: self.user_id) \
                .add_column("image_id", lambda df: annotation_util.generate_md5(df['image_name'][0])) \
                .add_column("created_at", lambda df: now)

        if final_annotation_ds is not None and final_image_ds is not None:
            final_ds = final_annotation_ds.union(final_image_ds)
        elif final_annotation_ds is not None:
            final_ds = final_annotation_ds
        elif final_image_ds is not None:
            final_ds = final_image_ds

        return final_ds


def test_fit_vistudio(config):
    """
    测试 fit_vistudio
    :param param_dict:
    :param train_client:
    :param labels:
    :param exist_image_names:
    :param exist_annotations:
    :return:
    """
    paths = list()
    paths.append("/Users/chujianfei/Downloads/shell/temp/vistudio_v3.json")
    import ray
    ds = ray.data.read_json(paths=paths)
    print("origin_ds", ds.take_all())

    anno_formatter = VistudioFormatter(config=config)
    final_ds = anno_formatter.fit(ds).stats_
    print("final_ds", final_ds.take_all())


if __name__ == "__main__":

    windmill_host = "http://10.27.240.49:8340"
    windmill_ak = "904fd1fa009447559d5ee5a6ad128526"
    windmill_sk = "a2b08c8dbc7a478393c5d57855b5c892"
    train_client = TrainingClient(
                   endpoint=windmill_host,
                   ak=windmill_ak,
                   sk=windmill_sk)

    mongodb_host = "10.27.240.45"
    mongodb_port = 8719
    mongodb_user = "root"
    mongodb_password = "mongo123#"
    mongodb_database = "annotation_dev"


    def mongodb_collection(host='localhost', port=8717, username='root', password='',
                           database='vistudio', collection='annotationitems'):
        """
        初始化mongodb连接
        """
        from pymongo import MongoClient
        mongo_client = MongoClient(host=host, port=port, username=username, password=password)
        mongo_db = mongo_client[database]
        return mongo_db

    mongodb = mongodb_collection(
        host=mongodb_host,
        port=mongodb_port,
        username=mongodb_user,
        password=mongodb_password,
        database=mongodb_database,
        collection=mongodb_collection)

    param_dict = {
        "annotation_set_id" : "annotation_set_1",
        "annotation_format": "coco",
        "user_id": "user_123"
    }
    labels = {"1": "piaofu", "2": "head", "3": "toukui", "4": "floater", "5": "heichou", "6": "lanzao"}
    config = Config()
    test_fit_vistudio(config)




