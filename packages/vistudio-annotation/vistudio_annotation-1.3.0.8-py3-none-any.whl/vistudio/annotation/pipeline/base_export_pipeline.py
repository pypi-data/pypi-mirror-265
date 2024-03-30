#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   base_pipeline.py
"""
import re
import json
from windmilltrainingv1.client.training_client import TrainingClient
from vistudio.annotation.client.annotation_client import AnnotationClient
from vistudio.annotation.config import config
from vistudio.annotation.util import annotation_util
import logit

job_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/jobs/(?P<job_name>[^/]+)$"
annotationset_name_pattern = r"workspaces/(?P<workspace_id>[^/]+)/projects/(?P<project_name>[^/]+)/annotationsets/" \
                             r"(?P<annotationset_local_name>[^/]+)$"


class BaseExportPipeline(object):
    def __init__(self, args):
        self.args = args
        self.config = config.parse_args(args)
        self.dataset = json.loads(annotation_util.decode_from_base64(args.dataset))
        self.mongo_pipeline = self._get_mongo_pipeline()
        self.merge_labels = self._get_merge_labels()
        self.mongo_uri = self._get_mongo_uri()
        self._get_project_workspace()
        self._get_labels()
        self._get_auth_info()
        self.annotation_format = args.annotation_format.lower()

    def _get_mongo_uri(self):
        """
        get mongo uri
        :return:
        """
        uri = "mongodb://{}:{}@{}:{}".format(self.config.mongodb_user,
                                             self.config.mongodb_password,
                                             self.config.mongodb_host,
                                             self.config.mongodb_port)
        return uri

    def _get_merge_labels(self):
        """
        get merge labels
        :return:
        """
        if self.args.merge_labels is not None and self.args.merge_labels != '':
            merge_labels = json.loads(annotation_util.decode_from_base64(self.args.merge_labels))
        else:
            merge_labels = None

        print("merge_labels,",merge_labels)
        return merge_labels

    def _get_mongo_pipeline(self):
        """
        get mongo pipeline
        :return:
        """
        if self.args.q is not None and self.args.q != '':
            mongo_pipeline = json.loads(annotation_util.decode_from_base64(self.args.q))
        else:
            mongo_pipeline = None
        return mongo_pipeline

    def _get_project_workspace(self):
        """
        get project workspace
        :return:
        """
        match = re.match(job_name_pattern, self.args.job_name)
        job_name_dict = match.groupdict()
        self.workspace_id = job_name_dict.get("workspace_id")
        self.project_name = job_name_dict.get("project_name")
        self.job_local_name = job_name_dict.get("job_name")

    def _get_labels(self):
        """
        get labels
        :return:
        """
        annotation_set_name = self.args.annotation_set_name
        self.annotation_set_name = annotation_set_name
        try:
            annotation_client = AnnotationClient(endpoint=self.config.vistudio_endpoint,
                                                 ak=self.config.windmill_ak,
                                                 sk=self.config.windmill_sk)
            match = re.match(annotationset_name_pattern, self.annotation_set_name)
            annotationset_name_dict = match.groupdict()
            annotationset_workspace_id = annotationset_name_dict.get("workspace_id")
            annotationset_project_name = annotationset_name_dict.get("project_name")
            annotationset_local_name = annotationset_name_dict.get("annotationset_local_name")
            anno_res = annotation_client.get_annotation_set(workspace_id=annotationset_workspace_id,
                                                            project_name=annotationset_project_name,
                                                            local_name=annotationset_local_name)
        except Exception as e:
            logit.error("get annotation info exception.annotation_name:{}"
                         .format(annotation_set_name), e)
            raise Exception("Get annotation set info exception.annotation_set_name:{}".format(annotation_set_name))

        self.annotation_set_id = anno_res.id
        if anno_res.id is None:
            self.annotation_set_id = "test-annotation-set-id"  # todo 待删除
        annotation_labels = anno_res.labels
        labels = {}
        for label_elem in annotation_labels:
            label_local_name = label_elem.local_name
            label_display_name = label_elem.display_name
            labels[label_local_name] = label_display_name

        self.labels = labels

    def _get_auth_info(self):
        """
        get auth info
        :return:
        """
        try:
            train_client = TrainingClient(endpoint=self.config.windmill_endpoint,
                                          ak=self.config.windmill_ak,
                                          sk=self.config.windmill_sk)
            job_res = train_client.get_job(workspace_id=self.workspace_id,
                                           project_name=self.project_name,
                                           local_name=self.job_local_name)
        except Exception as e:
            logit.error("get job info exception.job name:{}"
                         .format(self.config.job_name), e)
            raise Exception("Get job info exception.job_name:{}".format(self.config.job_name))

        self.org_id = job_res.orgID
        self.user_id = job_res.userID


