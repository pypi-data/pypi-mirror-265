#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
formater.py
"""

from typing import Union, Dict, Any
import pandas as pd
import ray.data
from ray.data.preprocessor import Preprocessor


class ImageNetFormatter(Preprocessor):
    """
    use this Preprocessor to convert  vistudio to imagenet
    """
    def __init__(self,
                 labels: Union[Dict] = dict,
                 merge_labels: Union[Dict] = dict
                 ):
        self._is_fittable = True
        self._fitted = True
        self.label_id_dict = dict()
        self.labels = labels
        self.merge_labels = merge_labels
        for label_id, label_name in self.labels.items():
            self.label_id_dict[label_id] = len(self.label_id_dict)

    def _transform_pandas(self, df: "pd.DataFrame") -> "pd.DataFrame":
        """
        _transform_pandas
        :param df:
        :return:
        """
        rows = df.to_dict(orient='records')
        return self._imagenet_from_vistudio_v1(rows)

    def _imagenet_from_vistudio_v1(self, rows: list):
        """
        imagenet_from_vistudio_v1
        :param elem:
        :return:
        """
        annotation_list = list()
        for elem in rows:
            annotations_total = elem.get('annotations')
            if annotations_total is None  or len(annotations_total) == 0:
                continue
            file_name = elem['file_uri']
            for image_annotation in annotations_total:
                task_kind = image_annotation['task_kind']
                if task_kind != "Manual":
                    continue
                annotations = image_annotation['annotations']
                if annotations is None  or len(annotations) == 0:
                    continue
                for annotation in annotations:
                    labels = annotation['labels']
                    for label in labels:
                        label_id = label['id']
                        if self.merge_labels is not None and label_id in self.merge_labels:
                            label_id = self.merge_labels[label_id]
                        if self.label_id_dict.get(str(label_id)) is not None:
                            annotation_list.append(("{} {}").format(file_name, self.label_id_dict.get(str(label_id))))

        item = {"item": annotation_list}
        return pd.DataFrame(item)


if __name__ == "__main__":
    test_data = []
    import pandas as pd
    ds = ray.data.from_pandas(pd.DataFrame(test_data))
    labels = {"1": "aa", "2": "bb"}
    imagenet_formater = ImageNetFormatter(labels=labels)
    final_ds = imagenet_formater.transform(ds)
    print("final_ds", final_ds.take_all())