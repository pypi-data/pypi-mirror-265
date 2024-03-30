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
import pymongo

from query_pipeline import query_mongo
from vistudio.annotation.config.config import Config
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from vistudio_annotation.client.annotation_client import AnnotationClient


def parse_annotation_set_name(annotation_set_name):
    """
    解析 annotation_set_name
    :param annotation_set_name:
    :return:
    """
    workspace_id, project_name, local_name = annotation_set_name.split("/")[1], annotation_set_name.split("/")[3], \
                                            annotation_set_name.split("/")[-1]
    return workspace_id, project_name, local_name


def batch_delete(base_conf: Config, annotation_set_name, query_pipeline):
    """
    批量删除
    :param base_conf:
    :param annotation_set_name:
    :param query_pipeline
    :return:
    """
    # 连接Mongo
    mongo_uri = f"mongodb://{base_conf.mongodb_user}:{base_conf.mongodb_password}@{base_conf.mongodb_host}:" \
                f"{base_conf.mongodb_port}"
    client = pymongo.MongoClient(mongo_uri)
    db = client[base_conf.mongodb_database]
    collection = db[base_conf.mongodb_collection]

    # 获取 annotation_set_id
    windmill = AnnotationClient(
        BceClientConfiguration(credentials=BceCredentials(base_conf.windmill_ak, base_conf.windmill_sk),
                               endpoint=base_conf.vistudio_endpoint))

    workspace_id, project_name, local_name = parse_annotation_set_name(annotation_set_name)
    annotation_set = windmill.get_annotation_set(workspace_id, project_name, local_name)
    print("annotation_set: {}".format(annotation_set))
    annotation_set_id = annotation_set.id
    print("annotation_set_id: {}".format(annotation_set_id))

    # 获取需要更新的 image_id
    results = query_mongo(query_pipeline, collection)
    delete_image_ids = results.get("image_ids", [])
    print("delete_image_ids: {}".format(delete_image_ids))

    # 通过 mongo 删除
    with client.start_session() as session:
        try:
            session.start_transaction()
            collection.delete_many({
                "image_id": {"$in": delete_image_ids},
                "annotation_set_id": annotation_set_id}, session=session)
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
    print("start batch delete")
    args = parse_args()
    print(f"args: {args}")
    q = args.q
    q = base64.b64decode(q)
    print(f"query: {q}")
    q = json.loads(q)
    base_config = Config(
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

    batch_delete(base_config, args.annotation_set_name, q)
