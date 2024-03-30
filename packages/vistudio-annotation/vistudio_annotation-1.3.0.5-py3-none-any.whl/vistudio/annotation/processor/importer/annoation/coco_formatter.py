#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File :   formater.py
"""
import time
import pandas as pd
import os
import re
import ray
from typing import Union, Dict, Any, List
from ray.data.preprocessor import Preprocessor
from ray.data import Dataset
from windmilltrainingv1.client.training_client import TrainingClient
from vistudio.annotation.util import annotation_util
from vistudio.annotation.config.config import Config
import logit

image_extensions = ('.jpeg', '.jpg', '.png', '.bmp')
job_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/jobs/(?P<job_name>[^/]+)$"
time_pattern = "%Y-%m-%dT%H:%M:%SZ"


class CocoFormatter(Preprocessor):
    """
    use this Preprocessor to handle dataset
    """
    def __init__(self,
                 config: Config,
                 labels: Union[Dict] = dict,
                 user_id: str = None,
                 annotation_set_id: str = None,
                 annotation_set_name: str = None,
                 data_uri: str = None,
                 data_types: list() = None

                 ):
        self._is_fittable = True
        self.config = config
        self.labels = {v: int(k) for k, v in labels.items()}
        self.user_id = user_id
        self.annotation_set_id = annotation_set_id
        self.annotation_set_name = annotation_set_name
        self.data_uri = data_uri,
        self.data_types = data_types
        if len(self.data_types) == 2 and "image" in self.data_types and "annotation" in self.data_types:
            self.image_uri_prefix = os.path.join(data_uri, "images")
        else:
            self.image_uri_prefix = ''
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
        return row["name"] not in labels

    def _group_by_image_id(self, group: pd.DataFrame) -> pd.DataFrame:
        """
        group bu image_id
        :param group:
        :return:
        """
        image_id = group["image_id"][0]
        ids = group["id"].tolist()
        annoations = list()
        for i in range(len(ids)):
            id = ids[i]
            bbox = group["bbox"].tolist()[i]
            segmentation = group["segmentation"].tolist()[i]
            area = group["area"].tolist()[i]
            cate = group["category_id"].tolist()[i]
            iscrowd = group["iscrowd"].tolist()[i]
            anno = {
                "id": str(id),
                "bbox": bbox,
                "segmentation": segmentation,
                "area": area,
                "labels": [{
                    "id": str(cate),
                    "confidence": 1
                }],
                "iscrowd": iscrowd
            }
            annoations.append(anno)

        annoation_res = {"image_id": image_id,
                         "user_id": self.user_id,
                         "created_at": time.time_ns(),
                         "annotations": [annoations],
                         "data_type": "Annotation",
                         "annotation_set_id": self.annotation_set_id,
                         "task_kind": "Manual",
                         "artifact_name": ""}

        return pd.DataFrame(annoation_res)

    @staticmethod
    def _filter_exist_anno_bymd5(row: Dict[str, Any], exist_anno: set()):
        """
        if md5(row['name'] )in exist_anno, drop this row
        :param row:
        :param exist_fileuris:
        :return:
        """
        return annotation_util.generate_md5(row['name']) not in exist_anno


    @staticmethod
    def _update_image_id_byMD5(df: pd.DataFrame) -> "pandas.Series":
        """
        update image_id = MD5(row(file_name))
        :param row:
        :return:
        """
        df['image_id'] = df['file_name'].apply(lambda x : annotation_util.generate_md5(x))
        image_id_series = df['image_id'].rename("image_id")
        return image_id_series

    @staticmethod
    def _update_bbox(row: Dict[str, Any]):
        """
        update image_id = MD5(row(file_name))
        :param row:
        :return:
        """
        return pd.DataFrame([row]).to_dict()

    def _fit(self, ds: "Dataset") -> "Preprocessor":
        """
        fit coco dataset
        :param ds:
        :return: Preprocessor
        """
        final_anno_ds = self._fit_coco(ds)
        self.stats_ = final_anno_ds
        return self

    def _fill_image_info_coco(self, row: Dict[str, Any]):
        """
        fill coco image info
        :param row:
        :param image_ids:
        :return:
        """
        row['image_id'] = annotation_util.generate_md5(row['file_name'])
        row['image_name'] = os.path.basename(row['file_name'])
        row['annotation_set_id'] = self.annotation_set_id
        row['annotation_set_name'] = self.annotation_set_name
        row['user_id'] = self.user_id
        row['created_at'] = time.time_ns()
        row['data_type'] = 'Image'
        row['annotation_state'] = 'Init'
        row['image_state'] = 'Init'
        row['file_uri'] = os.path.join(self.image_uri_prefix, row['file_name'])
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

    def _fit_coco(self, ds: "Dataset") -> "Dataset":
        """
        _fit_coco
        :param ds: Dataset
        :return: Dataset
        """
        # 这里首先强校验标签，如果标注文件的标签 不在控制面的标签中，直接中断后续操作
        cate_ds = ds.flat_map(lambda row: self._flat(row=row, col="categories"))
        filter_label_ds = cate_ds.filter(lambda row: self._filter_exist_labels(row, self.labels)).select_columns(
            cols=["name"])

        if filter_label_ds.count() > 0:
            not_exist_label_list = filter_label_ds.to_pandas()['name'].tolist()
            if len(not_exist_label_list) > 0:
                err_msg = "标签 '{}' 不存在，请在平台添加.".format(not_exist_label_list)
                self._update_annotation_job( err_msg)
                raise Exception("The current labels does not match the existing labels." + err_msg)

        # 展开 images
        image_ds = ds.flat_map(lambda row: self._flat(row=row, col="images"))
        logit.info("import coco flat image.image_ds count={}".format(image_ds.count()))

        # 展开 annoations
        annoation_ds = ds.flat_map(lambda row: self._flat(row=row, col="annotations"))
        logit.info("import coco flat annotation.annoation_ds count={}".format(annoation_ds.count()))

        # merge image_ds and annoation_ds on annoation_ds.image_id = image_ds.id
        drop_id_annotaion_ds = annoation_ds.drop_columns(cols=['id'])
        image_df = image_ds.to_pandas()
        annotation_df = drop_id_annotaion_ds.to_pandas()
        annotation_image_is = annotation_df['image_id'].tolist()
        merged_df = pd.merge(annotation_df, image_df, left_on='image_id', right_on='id')
        #
        bboxs = merged_df['bbox'].tolist()
        segmentation = merged_df['segmentation'].tolist()
        normal_bbox_list = [arr.tolist() for arr in bboxs]
        normal_segmentation_list = [arr.tolist() for arr in segmentation]
        merged_df['bbox'] = normal_bbox_list
        merged_df['segmentation'] = normal_segmentation_list
        merged_annotaion_ds = ray.data.from_pandas(merged_df).drop_columns(cols=['image_id'])

        # # update image_id to md5(file_name)
        updated_annoation_ds = merged_annotaion_ds.add_column("image_id", lambda df: self._update_image_id_byMD5(df))
        droped_annoation_ds = updated_annoation_ds.drop_columns(cols=['file_name', 'height', 'width'])
        # groupby and map_groups
        group_data = droped_annoation_ds.groupby("image_id")
        group_anno_ds = group_data.map_groups(lambda g: self._group_by_image_id(g))

        fill_image_ds = image_ds.map(lambda row: self._fill_image_info_coco(row=row))\
            .drop_columns(cols=['id', 'file_name'])
        if len(self.data_types) == 1 and self.data_types[0] == "annotation":
            # only annotation
            final_ds = group_anno_ds
        elif len(self.data_types) == 2 and "image" in self.data_types and "annotation" in self.data_types:
            # image and annotation
            final_ds = group_anno_ds.union(fill_image_ds)

        return final_ds



def test_fit_coco(config):
    """
    测试 fit_coco
    :param param_dict:
    :param train_client:
    :param labels:
    :param exist_image_names:
    :param exist_annotations:
    :return:
    """
    paths = list()
    paths.append("/Users/chujianfei/Downloads/shell/temp/val_zbh.json")
    import ray
    ds = ray.data.read_json(paths=paths)
    print("origin_ds", ds.take_all())

    anno_formatter = CocoFormatter(config=config)
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

    config = Config()
    labels = {"1": "piaofu", "2": "head", "3": "toukui", "4": "floater", "5": "heichou", "6": "lanzao"}

    test_fit_coco(config=config)




