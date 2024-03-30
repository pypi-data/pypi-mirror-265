#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
formater.py
"""

from typing import Union, Dict, Any

import pandas as pd
import ray.data
from ray.data.preprocessor import Preprocessor
import numpy as np
import os
from windmillcomputev1.filesystem.s3 import S3BlobStore
from windmillartifactv1.client.artifact_client import ArtifactClient
from pyarrow.fs import S3FileSystem

from vistudio.annotation.writer.writer import ImageFilenameProvider
from vistudio.annotation.config.config import Config
from vistudio.annotation.util import annotation_util, image_util
import logit

logit.base_logger.setup_logger({})

ANNOTATION_FORMAT_COCO = 'Coco'
ANNOTATION_FORMAT_IMAGENET = 'ImageNet'
ANNOTATION_FORMAT_CITYSCAPES = 'Cityscapes'

ANNOTATION_TYPE_POLYGON = 'polygon'
ANNOTATION_TYPE_RLE = 'rle'


class CityscapeFormatter(Preprocessor):
    """
    use this Preprocessor to convert vistudio_v1 to cityscape
    """

    def __init__(self, config: Config,
                 labels: Union[Dict] = dict,
                 location: str = None,
                 merge_labels: Union[Dict] = dict):
        self.config = config
        self.label_id_dict = dict()
        self._is_fittable = True
        self._fitted = True
        self.labels = labels
        self.location = location
        self.merge_labels = merge_labels

        for label_id, label_name in self.labels.items():
            label_index = len(self.label_id_dict) + 1
            self.label_id_dict[label_id] = label_index

        if not self.config.s3_host.startswith("http"):
            if self.config.disableSSL:
                self.pyarrow_fs_endpoint_url = "http://" + self.config.s3_host
            else:
                self.pyarrow_fs_endpoint_url = "https://" + self.config.s3_host

        self.fs = S3FileSystem(
            access_key=self.config.s3_ak,
            secret_key=self.config.s3_sk,
            endpoint_override=self.pyarrow_fs_endpoint_url)

    def _transform_pandas(self, df: "pd.DataFrame") -> "pd.DataFrame":
        """
        _transform_pandas
        :param df:
        :return:
        """
        rows = df.to_dict(orient='records')
        return self._cityscape_from_vistudio_v1(rows)

    def _cityscape_from_vistudio_v1(self, rows: list):
        """
        cityscape_from_vistudio_v1
        :param elem:
        :return:
        """
        item_list = []
        for elem in rows:
            file_uri = elem['file_uri']
            annotations_total = elem.get('annotations')
            if annotations_total is None or len(annotations_total) == 0:
                continue
            for image_annotation in annotations_total:
                task_kind = image_annotation['task_kind']
                if task_kind != "Manual":
                    continue

                annotations = image_annotation['annotations']
                if annotations is None  or len(annotations) == 0:
                    continue

                is_masked = False
                mask = np.zeros(shape=(elem['height'], elem['width']), dtype=np.int32)
                item = dict()
                for annotation in annotations:
                    points = annotation.get('segmentation', [])

                    labels = annotation['labels']
                    for label in labels:
                        label_id = label['id']
                        if self.merge_labels is not None and label_id in self.merge_labels:
                            label_id = self.merge_labels[label_id]
                        label_index = self.label_id_dict.get(str(label_id))
                        if label_index is None:
                            logit.warning("label_id: {} not found".format(label_id))
                            print("label_id: {} not found".format(label_id))
                            continue
                        rle = annotation.get('rle')
                        if rle is not None:
                            rle_counts = annotation['rle']['count']
                            if rle_counts is not None and isinstance(rle_counts, list) and len(rle_counts) > 0:
                                annotation_type = ANNOTATION_TYPE_RLE
                            else:
                                annotation_type = ANNOTATION_TYPE_POLYGON

                            if annotation_type == ANNOTATION_TYPE_RLE:
                                annotation_util.fill_mask_with_rle(mask, rle=points, label_id=label_index)
                            elif annotation_type == ANNOTATION_TYPE_POLYGON:
                                annotation_util.fill_mask_with_polygon(mask, points=points, label_id=label_index)
                            else:
                                raise ValueError("exporter to cityscape error:  {}".format(elem))

                    if not is_masked:
                        is_masked = True

                if is_masked:
                    file_name = os.path.basename(file_uri)
                    file_dir = os.path.dirname(file_uri).replace('s3://', '')
                    png_file = image_util.convert_ext_with_png(file_name)
                    # png_path = os.path.join(self.mask_dir, file_dir)
                    # png_full_path = os.path.join(self.mask_dir, file_dir, png_file)
                    # if not os.path.exists(png_path):
                    #     os.makedirs(png_path)
                    #cv2.imwrite(png_full_path, mask)
                    image_data = [{"image": mask}]
                    ds = ray.data.from_pandas(pd.DataFrame(image_data))

                    upload_path = self.location + "/labels/" + png_file
                    filename_provider = ImageFilenameProvider(file_name=png_file, is_full_file_name=True)
                    logit.info("cityscape formatter.upload mask.file_uri:{} png_file:{} upload_path:{}"
                               .format(file_uri, png_file, upload_path))
                    ds.repartition(1).write_images(path=self.location + "/labels/",
                                    filesystem=self.fs,
                                    column="image",
                                    filename_provider=filename_provider)
                    item_value = '{} {}'.format(file_name, self.location + "/labels/" + png_file)
                    item = {"item": item_value}
                    item_list.append(item)

        return pd.DataFrame(item_list)

    def _get_transform_config(self) -> Dict[str, Any]:
        """Returns kwargs to be passed to :meth:`ray.data.Dataset.map_batches`.

        This can be implemented by subclassing preprocessors.
        """
        return {"batch_size": 1024}


if __name__ == "__main__":
    test_data = []
    import pandas as pd
    ds = ray.data.from_pandas(pd.DataFrame(test_data))
    ds.write_images
    labels = {"1": "aa", "2": "bb"}
    s3_bucket = "windmill"
    s3_host = "http://s3.bj.bcebos.com:80"
    s3_ak = "de0472630db3405fbab8c469aa03f05e"
    s3_sk = "1f416c9741b743feb072a7590f57dbb9"

    windmill_host = "http://10.27.240.49:8340"
    windmill_ak = "904fd1fa009447559d5ee5a6ad128526"
    windmill_sk = "a2b08c8dbc7a478393c5d57855b5c892"
    artifact_client = ArtifactClient(
        endpoint=windmill_host,
        ak=windmill_ak,
        sk=windmill_sk
    )
    object_name = "workspaces/{}/projects/{}/datasets/{}".format(
        "public",
        "default",
        "ds-o6lxw5JV"
    )
    location_resp = artifact_client.create_location(object_name=object_name)
    location = location_resp.location[len("s3://"):].strip("/")

    s3_access_key = "de0472630db3405fbab8c469aa03f05e"
    s3_secret_key = "1f416c9741b743feb072a7590f57dbb9"
    s3_endpoint_override = "http://s3.bj.bcebos.com:80"
    s3_region = "bj"

    bos = S3FileSystem(access_key=s3_access_key,
                       region=s3_region,
                       secret_key=s3_secret_key,
                       endpoint_override=s3_endpoint_override)
    config = Config()
    cityscape_formater = CityscapeFormatter(config=config, labels=labels, location=location)
    final_ds = cityscape_formater.transform(ds)
    print("final_ds", final_ds.take_all())