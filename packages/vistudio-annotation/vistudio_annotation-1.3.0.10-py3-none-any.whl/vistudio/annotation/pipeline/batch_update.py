# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
"""
batch_delete.py
Authors: xujian(xujian16@baidu.com)
Date:    2024/3/18 3:55 下午
"""

import argparse
import base64
import json
import random
import string
import pymongo

from pydantic import BaseModel
from vistudio.annotation.config.config import Config
from .query_pipeline import query_mongo
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from vistudio.annotation.client.annotation_client import AnnotationClient
from windmilltrainingv1.client.training_client import TrainingClient



DATA_TYPE_IMAGE = "Image"
DATA_TYPE_ANNOTATION = "Annotation"

mongo_client = None
collection = None
vistudio_client = None
train_client = None


class UpdateConfig(BaseModel):
    """
    定义更新任务的配置
    """
    job_name: str = ""
    query_pipeline: list = []
    annotation_set_name: str = ""
    object_type: str = ""
    updates: dict = {}


def generate_random_string(length):
    """
    生成随机字符串
    :param length:
    :return:
    """
    # 定义字符集合
    characters = string.ascii_letters + string.digits

    # 生成随机字符串
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def parse_annotation_set_name(annotation_set_name):
    """
    解析 annotation_set_name
    :param annotation_set_name:
    :return:
    """
    workspace_id, project_name, local_name = annotation_set_name.split("/")[1], annotation_set_name.split("/")[3], \
                                            annotation_set_name.split("/")[-1]
    return workspace_id, project_name, local_name


def parse_job_name(job_name):
    """
    解析 job_name
    :param job_name:
    :return:
    """
    # 获取 workspace_id, project_name, local_name
    workspace_id, project_name, local_name = job_name.split("/")[1], job_name.split("/")[3], \
                                            job_name.split("/")[-1]
    return workspace_id, project_name, local_name


def batch_update(update_conf: UpdateConfig):
    """
    批量更新
    :param update_conf:
    :return:
    """
    # 获取 annotation_set_id
    workspace_id, project_name, local_name = parse_annotation_set_name(update_conf.annotation_set_name)
    annotation_set = vistudio_client.get_annotation_set(workspace_id, project_name, local_name)
    print("annotation_set: {}".format(annotation_set))
    annotation_set_id = annotation_set.id
    print("annotation_set_id: {}".format(annotation_set_id))

    # 获取 job 对应的 user_id
    workspace_id, project_name, local_name = parse_job_name(update_conf.job_name)
    job = train_client.get_job(workspace_id, project_name, local_name)
    print("job: {}".format(job))
    user_id = job.userID

    # 获取需要更新的 image_id
    results = query_mongo(update_conf.query_pipeline, collection)
    update_image_ids = results.get("image_ids", [])
    print(f"update_image_ids: {update_image_ids}")

    # 更新
    if update_config.object_type == "Image":
        update_image_tag(annotation_set_id, update_image_ids, update_conf.updates)
    elif update_config.object_type == "Annotation":
        update_annotation_label(annotation_set_id, update_image_ids, update_conf.updates, user_id)


def update_image_tag(annotation_set_id, image_ids, updates):
    """
    更新 image 的 tag
    :param annotation_set_id:
    :param image_ids:
    :param updates:
    :return:
    """
    update_tags = updates["tags"]
    update_field = dict()
    for key, value in update_tags.items():
        update_field[f"tags.{key}"] = value
    update = {"$set": update_field}
    with mongo_client.start_session() as session:
        try:
            session.start_transaction()
            collection.update_many(
                filter={
                    "image_id": {"$in": image_ids},
                    "annotation_set_id": annotation_set_id,
                    "data_type": DATA_TYPE_IMAGE
                },
                update=update,
                session=session)
            session.commit_transaction()
        except Exception as e:
            session.abort_transaction()
            raise e


def update_annotation_label(annotation_set_id, image_ids, updates, user_id=""):
    """
    更新 annotation 的 label
    :param annotation_set_id:
    :param image_ids:
    :param updates:
    :param user_id:
    :return:
    """
    update_label_ids = updates["labels"]
    # 目前版本，只支持一个 label
    assert len(update_label_ids) == 1
    update_labels = [{"id": id} for id in update_label_ids]

    anno_filter = {
        "image_id": {"$in": image_ids},
        "annotation_set_id": annotation_set_id,
        "data_type": DATA_TYPE_ANNOTATION,
        "artifact_name": ""
    }
    image_filter = {
        "image_id": {"$in": image_ids},
        "annotation_set_id": annotation_set_id,
        "data_type": DATA_TYPE_IMAGE,
    }

    # 计算需要新插入的 annotation
    insert_annotations = []
    for image_id in image_ids:
        annotation = {
            "image_id": image_id,
            "annotation_set_id": annotation_set_id,
            "artifact_name": "",
            "task_kind": "Manual",
            "data_type": DATA_TYPE_ANNOTATION,
            "annotations": [{"id": "anno-" + generate_random_string(8), "labels": update_labels}],
            "user_id": user_id,
        }
        insert_annotations.append(annotation)

    # 执行 mongo 更新
    image_update = {"$set": {"annotation_state": "Annotated"}}
    with mongo_client.start_session() as session:
        try:
            session.start_transaction()
            # 先删除，后插入新的标注
            collection.delete_many(anno_filter, session=session)
            collection.insert_many(insert_annotations, session=session)

            # 更新图片的标注状态
            collection.update_many(image_filter, image_update)
            session.commit_transaction()
        except Exception as e:
            session.abort_transaction()
            raise e


def split_string_list(s):
    """
    将字符串转换为 list
    :param s:
    :return:
    """
    return s.strip("'").split(",")


def parse_args():
    """
    解析参数
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--q",
        dest="q",
        required=True,
        default='',
        help="Mongo query sql",
    )

    parser.add_argument(
        "--object-type",
        dest="object_type",
        required=True,
        default=[],
        help="Exclude image ids",
    )

    parser.add_argument(
        "--updates",
        dest="updates",
        required=True,
        default='',
        help="Updates content",
    )

    parser.add_argument(
        "--annotation-set-name",
        dest="annotation_set_name",
        required=True,
        default="",
        help="Annotation set name, example: as01",
    )

    parser.add_argument(
        "--job-name",
        dest="job_name",
        required=True,
        default='',
        help="Job name",
    )

    parser.add_argument(
        "--filesystem-name",
        dest="filesystem_name",
        required=True,
        default='',
        help="Filesystem name",
    )

    parser.add_argument(
        "--mongo-host",
        dest="mongo_host",
        required=True,
        default="10.27.240.45",
        help="mongo host",
    )

    parser.add_argument(
        "--mongo-port",
        dest="mongo_port",
        required=True,
        default="8718",
        help="mongo port",
    )

    parser.add_argument(
        "--mongo-user",
        dest="mongo_user",
        required=True,
        default="root",
        help="mongo user",
    )

    parser.add_argument(
        "--mongo-password",
        dest="mongo_password",
        required=True,
        default="",
        help="mongo password",
    )

    parser.add_argument(
        "--mongo-db",
        dest="mongo_database",
        required=True,
        default="",
        help="mongo database",
    )

    parser.add_argument(
        "--mongo-collection",
        dest="mongo_collection",
        required=True,
        default="",
        help="mongo collection",
    )

    parser.add_argument(
        "--vistudio-endpoint",
        dest="vistudio_endpoint",
        required=True,
        default="",
        help="windmill host",
    )

    parser.add_argument(
        "--windmill-endpoint",
        dest="windmill_endpoint",
        required=True,
        default="",
        help="windmill host",
    )

    parser.add_argument(
        "--windmill-ak",
        dest="windmill_ak",
        required=True,
        default="",
        help="windmill ak",
    )

    parser.add_argument(
        "--windmill-sk",
        dest="windmill_sk",
        required=True,
        default="",
        help="windmill sk",
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    print("start batch update")
    args = parse_args()
    q = args.q
    q = base64.b64decode(q)
    print(f"query: {q}")
    q = json.loads(q)

    updates = args.updates
    updates = base64.b64decode(updates)
    print(f"updates: {updates}")
    updates = json.loads(updates)

    base_conf = Config(
        mongodb_host=args.mongo_host,
        mongodb_port=args.mongo_port,
        mongodb_user=args.mongo_user,
        mongodb_password=args.mongo_password,
        mongodb_database=args.mongo_database,
        mongodb_collection=args.mongo_collection,
        vistudio_endpoint=args.vistudio_endpoint,
        windmill_endpoint=args.windmill_endpoint,
        windmill_ak=args.windmill_ak,
        windmill_sk=args.windmill_sk,
    )
    update_config = UpdateConfig(
        job_name=args.job_name,
        annotation_set_name=args.annotation_set_name,
        query_pipeline=q,
        object_type=args.object_type,
        updates=updates,
    )

    # init mongo client
    mongo_uri = f"mongodb://{base_conf.mongodb_user}:{base_conf.mongodb_password}@{base_conf.mongodb_host}:" \
                f"{base_conf.mongodb_port}"
    mongo_client = pymongo.MongoClient(mongo_uri)
    db = mongo_client[base_conf.mongodb_database]
    collection = db[base_conf.mongodb_collection]

    # init vistudio client
    vistudio_client = AnnotationClient(
        BceClientConfiguration(credentials=BceCredentials(base_conf.windmill_ak, base_conf.windmill_sk),
                               endpoint=base_conf.vistudio_endpoint))

    # init train client
    train_client = TrainingClient(
        BceClientConfiguration(credentials=BceCredentials(base_conf.windmill_ak, base_conf.windmill_sk),
                               endpoint=base_conf.windmill_endpoint))

    # batch update
    batch_update(update_config)
