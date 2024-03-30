#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
CocoMerger.py
"""

from typing import Union, Dict, Any

import pandas
import ray.data
from ray.data.preprocessor import Preprocessor


class CocoMerger(Preprocessor):
    """
    use this Preprocessor to merge coco dataset by item
    for example:
    ds = [{"images":[{"file_name":"b.jpg"}, ],"annotations":[{"image_id":2}],"categories":[{"name":"piaofu"}]},
        {{"images":[{"file_name":"a.jpg"}],"annotations":[{"image_id":3}],"categories":[{"name":"piaofu"}]}]

    merge_ds = CocoMerger.fit(ds)
    merge_ds= [
                {"images":[{"file_name":"b.jpg"}, {"name":"piaofu"}],
                "annotations":[{"image_id":2},{"image_id":3}],
                "categories":[{"name":"piaofu"},{"name":"piaofu"}]}
                ]
    """

    def __init__(self):
        self._is_fittable = True
        self._fitted = True

    def _fit(self, ds: "Dataset") -> "Preprocessor":
        print("coco merge ds", ds.take_all())
        df = ds.to_pandas()

        #image_merge_list = df.explode('images').groupby(level=0)['images'].agg(lambda x: x.tolist())
        image_merge_list = df['images'].sum()
        anno_merge_list = df['annotations'].sum()

        cate_merge_list = df['categories'].sum()

        cate_ids = set()
        cate_unique_list = []
        for item in cate_merge_list:
            if item["id"] not in cate_ids:
                cate_ids.add(item["id"])
                cate_unique_list.append(item)

        res = [{
            "images": image_merge_list,
            "annotations": anno_merge_list,
            "categories": cate_unique_list
        }]
        res_ds = ray.data.from_pandas(pandas.DataFrame(res))
        #res_ds = ray.data.from_pandas(res)
        self.stats_ = res_ds
        return self


