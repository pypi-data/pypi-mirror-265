#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
formater.py
"""

from typing import Union, Dict, Any

import pandas as pd
import ray.data
from ray.data.preprocessor import Preprocessor

from vistudio.annotation.util import annotation_util

ANNOTATION_FORMAT_COCO = 'Coco'
ANNOTATION_FORMAT_IMAGENET = 'ImageNet'
ANNOTATION_FORMAT_CITYSCAPES = 'Cityscapes'

ANNOTATION_TYPE_POLYGON = 'polygon'
ANNOTATION_TYPE_RLE = 'rle'


class CocoFormatter(Preprocessor):
    """
    use this Preprocessor to convert vistudio_v1 to coco
    """

    def __init__(self,
                 labels: Union[Dict] = dict,
                 merge_labels: Union[Dict] = dict):
        self._is_fittable = True
        self._fitted = True
        # labels = {"1", "diaosi"}
        self.labels = labels
        self.merge_labels = merge_labels

    def _transform_pandas(self, df: "pd.DataFrame") -> "pd.DataFrame":
        """
        _transform_pandas
        :param df:
        :return:
        """

        rows = df.to_dict(orient='records')
        return self._coco_from_vistudio_v1(rows)

    def _coco_from_vistudio_v1(self, rows: list):
        """
        coco_from_vistudio_v1
        :param elem:
        :return:
        """
        images_list = list()
        annotations_list = list()
        categories_list = list()
        all_file_name = list()
        label_id_dict = dict()
        for elem in rows:
            file_name = elem['file_uri']
            image_height = elem['height']
            image_width = elem['width']
            all_file_name.append(file_name)

            image_id = int(elem['image_id'], 16)
            images_list.append({
                "file_name": file_name,
                "height": image_height,
                "width": image_width,
                "id": image_id
            })

            annotations_total = elem.get('annotations')
            if annotations_total is None or len(annotations_total) == 0:
                continue
            for image_annotation in annotations_total:
                task_kind = image_annotation['task_kind']
                if task_kind != "Manual":
                    continue

                annotations = image_annotation['annotations']
                if annotations is None or len(annotations) == 0:
                    continue

                for annotation in annotations:
                    bbox = annotation.get('bbox', [])
                    area = annotation.get('area', [])
                    seg = annotation.get('segmentation', [])

                    labels = annotation['labels']
                    if labels is None or len(labels) == 0:
                        continue

                    label_id = str(labels[0]['id'])
                    if self.merge_labels is not None and label_id in self.merge_labels:
                        label_id = self.merge_labels[label_id]
                    if label_id not in label_id_dict:
                        label_id_dict[label_id] = len(label_id_dict) + 1
                        label_name = self.labels.get(str(label_id), "not_found")
                        categories_list.append({
                            "id": label_id,
                            "name": label_name,
                            "supercategory": label_name
                        })

                    annotations_list.append({
                        "id": annotation_util.generate_random_digits(6),
                        "image_id": image_id,
                        "bbox": bbox,
                        "area": area,
                        "iscrowd": 0,
                        "category_id": label_id,
                        "segmentation": seg,
                    })
        anno = [{
            "images": images_list,
            "annotations": annotations_list,
            "categories": categories_list
        }]
        return pd.DataFrame(anno)

    def _get_transform_config(self) -> Dict[str, Any]:
        """Returns kwargs to be passed to :meth:`ray.data.Dataset.map_batches`.

        This can be implemented by subclassing preprocessors.
        """
        return {"batch_size": 1024}


if __name__ == "__main__":
    test_data = []
    import pandas as pd
    ds = ray.data.from_pandas(pd.DataFrame(test_data))
    labels = {"1": "aa", "2": "bb"}
    coco_formater = CocoFormatter(labels=labels)
    final_ds = coco_formater.transform(ds)
    print("final_ds", final_ds.take_all())
