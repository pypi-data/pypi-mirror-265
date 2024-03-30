# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
"""
statistic.py
Authors: xujian(xujian16@baidu.com)
Date:    2024/3/23 2:37 下午
"""

import argparse
import base64
import json
import os
import random

import pymongo
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from vistudio.annotation.client.annotation_client import AnnotationClient
from gaea_operator.metric import Metric, EvalMetricCalculator, LabelStatisticMetricCalculator
from windmillcomputev1.client.compute_client import ComputeClient
from windmillcomputev1.filesystem.s3 import S3BlobStore
from windmillcomputev1.filesystem.blobstore import CONFIG_HOST, CONFIG_AK, CONFIG_SK, CONFIG_REGION, CONFIG_DISABLE_SSL

from vistudio.annotation.config.config import Config
from query_pipeline import query_mongo


def parse_annotation_set_name(annotation_set_name):
    """
    解析 annotation_set_name
    :param annotation_set_name:
    :return:
    """
    workspace_id, project_name, local_name = annotation_set_name.split("/")[1], annotation_set_name.split("/")[3], \
                                            annotation_set_name.split("/")[-1]
    return workspace_id, project_name, local_name


def parse_filesystem_name(filesystem_name):
    """
    解析 filesystem_name
    :param filesystem_name:
    :return:
    """
    workspace_id, local_name = filesystem_name.split("/")[1], filesystem_name.split("/")[-1]
    return workspace_id, local_name


def generate_output_json_path(name=None):
    """
    生成输出文件路径
    :return:
    """
    output_dir = "batch_act/output"
    if name is None:
        name = str(random.randint(0, 2 ** 16))
    output_json = output_dir + "/" + name + ".json"
    return output_json


def statistic(base_conf: Config, annotation_set_name, query_pipeline):
    """
    指标统计分析
    :param base_conf:
    :param annotation_set_name:
    :param query_pipeline:
    :return:
    """
    # 获取 s3 配置
    compute_client = ComputeClient(endpoint=base_conf.windmill_endpoint, ak=base_conf.windmill_ak,
                                   sk=base_conf.windmill_sk)
    workspace_id, local_name = parse_filesystem_name(base_conf.filesystem_name)
    filesystem = compute_client.get_filesystem(workspace_id, local_name)
    s3_host, s3_endpoint = filesystem.host, filesystem.endpoint
    s3_bucket = s3_endpoint.split("/")[0]
    credential = compute_client.get_filesystem_credential(workspace_id, local_name)
    credential = credential.credential
    s3_ak, s3_sk = credential['accessKey'], credential['secretKey']
    s3_conf = {CONFIG_HOST: s3_host, CONFIG_AK: s3_ak, CONFIG_SK: s3_sk, CONFIG_REGION: 'bj', CONFIG_DISABLE_SSL: True}
    blobstore = S3BlobStore(s3_endpoint, s3_conf)
    location = "s3://" + s3_endpoint + "/" + base_conf.job_name
    print(f"upload location: {location}")

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
    annotation_set_category = annotation_set.category.get("category", "Image/ObjectDetection")
    print("annotation_set_category: {}".format(annotation_set_category))

    labels = annotation_set.labels
    for label in labels:
        label["name"] = label["displayName"]
        label["id"] = label["localName"]
    print("labels: {}".format(labels))

    # 获取需要统计的图片及标注
    results = query_mongo(query_pipeline, collection)
    images = results.get("images", [])
    annotations = results.get("annotations", [])

    if len(images) == 0:
        print("No images to statistic")
        return

    # 分组不同的模型结果
    annotation_map = {}
    for annotation in annotations:
        artifact_name = annotation.get("artifact_name", "")
        if artifact_name not in annotation_map:
            annotation_map[artifact_name] = []
        annotation_map[artifact_name].append(annotation)

    # 统计不同模型的指标
    eval_metric = EvalMetricCalculator(category=annotation_set_category, labels=labels, images=images)
    label_statistics = LabelStatisticMetricCalculator(labels=labels)
    metric = Metric(metric=[eval_metric, label_statistics], annotation_set_name=annotation_set_name)
    for artifact_name, annotations in annotation_map.items():
        if artifact_name == "":
            manual_json = generate_output_json_path()
            metric(references=annotations, output_uri=manual_json, task_kind="Manual")
            blobstore.upload_file(manual_json, location + "/metric-manual.json")
            os.remove(manual_json)
            continue

        artifact_file_name = "metric-" + artifact_name.replace("/", "-") + ".json"
        output_url = generate_output_json_path()
        manual_annotations = annotation_map.get("", None)
        metric(predictions=annotations, references=manual_annotations, output_uri=output_url,
               task_kind="Model", artifact_name=artifact_name)
        blobstore.upload_file(output_url, location + "/" + artifact_file_name)
        os.remove(output_url)

    return
    # 保存labels
    labels_json = generate_output_json_path("labels.json")
    with open(labels_json, "w") as f:
        json.dump(labels, f)
    # 保存人工和模型标注结果
    for artifact_name, annotations in annotation_map.items():
        for anno in annotations:
            anno.pop("_id")
        annotation_json = generate_output_json_path("metric-" + artifact_name.replace("/", "-") + ".json")
        with open(annotation_json, "w") as f:
            json.dump(annotations, f)


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
    print("start statistic")
    args = parse_args()
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
        job_name=args.job_name,
        filesystem_name=args.filesystem_name,
    )

    statistic(base_config, args.annotation_set_name, q)
