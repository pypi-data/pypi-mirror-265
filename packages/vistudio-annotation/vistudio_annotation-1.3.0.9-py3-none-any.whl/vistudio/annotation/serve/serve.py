# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
"""

"""
import threading
import time
import os
from ray import serve

from vistudio.annotation.config.config import Config
from vistudio.annotation.pipeline.image_processing import ImageProcessingPipeline
from vistudio.annotation.pipeline.update_annotation_state import UpdateAnnotationStatePipeline
from vistudio.annotation.pipeline.update_image_created_time import UpdateImageCreatedTimePipeline


@serve.deployment(
    num_replicas=1,
    ray_actor_options={
        "num_cpus": 1,
        "num_gpus": 0,
    },
)
class ResidentTasks:
    """
    Resident Tasks
    """
    def __init__(self):
        self.sleep_unit = 5
        self.wait_count = 1
        self.config = parse_args()

        self.image_processing_signal = []
        self.update_annotation_state_signal = []
        self.update_image_created_time_signal = []

        self.image_processing_ppl = ImageProcessingPipeline(config=self.config, parallelism=10)
        self.update_annotation_state_ppl = UpdateAnnotationStatePipeline(config=self.config, parallelism=10)
        self.update_image_created_time_ppl = UpdateImageCreatedTimePipeline(config=self.config, parallelism=10)

        threading.Thread(target=self.image_processing).start()
        threading.Thread(target=self.update_annotation_state).start()
        threading.Thread(target=self.update_image_created_time).start()

    def __call__(self):
        self.image_processing_signal.append(1)
        self.update_annotation_state_signal.append(1)
        self.update_image_created_time_signal.append(1)

    def image_processing(self):
        """
        图像处理
        """
        while True:
            self.image_processing_signal.clear()
            res = self.image_processing_ppl.run()
            if res:
                self.wait_count = 1
            else:
                self.wait_count = min(360, 2 * self.wait_count)

            for _ in range(self.wait_count):
                if len(self.image_processing_signal) > 0:
                    self.wait_count = 1
                    break
                time.sleep(self.sleep_unit)

    def update_annotation_state(self):
        """
        更新状态
        """
        while True:
            self.update_annotation_state_signal.clear()
            res = self.update_annotation_state_ppl.run()
            if res:
                self.wait_count = 1
            else:
                self.wait_count = min(360, 2 * self.wait_count)

            for _ in range(self.wait_count):
                if len(self.update_annotation_state_signal) > 0:
                    self.wait_count = 1
                    break
                time.sleep(self.sleep_unit)

    def update_image_created_time(self):
        """
        更新时间
        """
        while True:
            self.update_image_created_time_signal.clear()
            res = self.update_image_created_time_ppl.run()
            if res:
                self.wait_count = 1
            else:
                self.wait_count = min(360, 2 * self.wait_count)

            for _ in range(self.wait_count):
                if len(self.update_image_created_time_signal) > 0:
                    self.wait_count = 1
                    break
                time.sleep(self.sleep_unit)


def parse_args() -> Config:
    """
    获取环境变量
    """
    config = Config()

    # mongodb
    config.mongodb_host = os.environ.get('MONGO_HOST', '10.27.240.45')
    config.mongodb_port = int(os.environ.get('MONGO_PORT', 8719))
    config.mongodb_user = os.environ.get('MONGO_USER', 'root')
    config.mongodb_password = os.environ.get('MONGO_PASSWORD', 'mongo123#')
    config.mongodb_database = os.environ.get('MONGO_DB', 'annotation_dev_tiny')
    config.mongodb_collection = os.environ.get('MONGO_COLLECTION', 'annotation')

    # windmill
    config.windmill_endpoint = os.environ.get('WINDMILL_ENDPOINT', "http://10.27.240.45:8340")
    config.windmill_ak = os.environ.get('WINDMILL_AK', "1cb1860b8bc848298050edffa2ef9e16")
    config.windmill_sk = os.environ.get('WINDMILL_SK', "51a7a74c9ef14063a6892d08dd19ffbf")

    return config


app = ResidentTasks.bind()
serve.run(app,
          route_prefix="/imageaggregation" ,
          name="imageaggregation_app",
          host="0.0.0.0",
          port=8000)

