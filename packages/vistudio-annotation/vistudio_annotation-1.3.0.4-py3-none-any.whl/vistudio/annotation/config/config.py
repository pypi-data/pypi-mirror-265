# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
"""
Vistudio Spec
"""
import re
import logit
from pydantic import BaseModel
from windmillcomputev1.client.compute_client import ComputeClient

logit.base_logger.setup_logger({})


image_extensions = ('.jpeg', '.jpg', '.png', '.bmp')
job_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/jobs/(?P<job_name>[^/]+)$"
annotationset_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/annotationsets/" \
                             r"(?P<annotationset_local_name>[^/]+)$"

fs_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/filesystems/(?P<filesystems_name>[^/]+)$"


class Config(BaseModel):
    """
    定义基础变量
    """
    s3_host: str = ""
    s3_endpoint: str = ""
    s3_ak: str = ""
    s3_sk: str = ""
    disableSSL: bool = True
    filesystem_name: str = ""

    mongodb_host: str = ""
    mongodb_port: int = 8717
    mongodb_user: str = ""
    mongodb_password: str = ""
    mongodb_database: str = ""
    mongodb_collection: str = ""

    windmill_endpoint: str = ""
    windmill_ak: str = ""
    windmill_sk: str = ""

    vistudio_endpoint: str = ""
    job_name: str = ""


def parse_args(args) -> Config:
    """
    获取环境变量
    """

    config = Config()

    # 获取job_name
    config.job_name = args.job_name

    # annotation
    config.vistudio_endpoint = args.vistudio_endpoint

    # mongodb
    config.mongodb_host = args.mongo_host
    config.mongodb_port = int(args.mongo_port)
    config.mongodb_user = args.mongo_user
    config.mongodb_password = args.mongo_password
    config.mongodb_database = args.mongo_database
    config.mongodb_collection = args.mongo_collection
    config.filesystem_name = args.filesystem_name
    filesystem_localname = args.filesystem_name.split("/")[-1]

    # windmill
    config.windmill_endpoint = args.windmill_endpoint
    config.windmill_ak = args.windmill_ak
    config.windmill_sk = args.windmill_sk

    # s3信息
    try:
        compute_client = ComputeClient(endpoint=config.windmill_endpoint,
                                       ak=config.windmill_ak,
                                       sk=config.windmill_sk)

        match = re.match(fs_name_pattern, config.filesystem_name)
        fs_name_dict = match.groupdict()
        fs_workspace_id = fs_name_dict.get("workspace_id")
        fs_local_name = fs_name_dict.get("filesystems_name")

        fs_res = compute_client.get_filesystem_credential(fs_workspace_id,
                                                          fs_local_name)
    except Exception as e:
        logit.error("get windmill fs info is None.workspace_id:{},filesystem_localname:{}"
                     .format(config.workspace_id, filesystem_localname), e)
        raise Exception("Get windmill fs info exception.workspace_id:{},filesystem_localname:{}"
                        .format(config.workspace_id, filesystem_localname))

    config.s3_host = fs_res.host
    config.s3_endpoint = fs_res.endpoint
    config.s3_ak = fs_res.credential.get("accessKey")
    config.s3_sk = fs_res.credential.get("secretKey")
    if fs_res.config.get("disableSSL") == "true":
        config.disableSSL = True
    else:
        config.disableSSL = False

    logit.info("Config: {}".format(config))
    return config



