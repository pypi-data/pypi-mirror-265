#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
CocoMerger.py
"""
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


if __name__ == "__main__":
    test_data = [
      {
        'images': [
          {
            'file_name': 's3://bucket/example_110912.jpg',
            'height': 1080,
            'width': 1920,
            'id': 184088570330734313981524315960151407680
          },
          {
            'file_name': 's3://bucket/example_110913.jpg',
            'height': 1080,
            'width': 1920,
            'id': 184088570330734313981524315960151407680
          }
        ],
        'annotations': [
          {
            'id': 'aitem_1',
            'image_id': 184088570330734313981524315960151407680,
            'bbox': [
              10,
              20,
              30,
              40
            ],
            'area': 200,
            'iscrowd': 0,
            'category_id': '1',
            'segmentation': {

            }
          },
          {
            'id': 'aitem_1',
            'image_id': 184088570330734313981524315960151407680,
            'bbox': [
              10,
              20,
              30,
              40
            ],
            'area': 200,
            'iscrowd': 0,
            'category_id': '2',
            'segmentation': {

            }
          },
          {
            'id': 'aitem_1',
            'image_id': 184088570330734313981524315960151407680,
            'bbox': [
              10,
              20,
              30,
              40
            ],
            'area': 200,
            'iscrowd': 0,
            'category_id': '1',
            'segmentation': {

            }
          },
          {
            'id': 'aitem_1',
            'image_id': 184088570330734313981524315960151407680,
            'bbox': [
              10,
              20,
              30,
              40
            ],
            'area': 200,
            'iscrowd': 0,
            'category_id': '2',
            'segmentation': {

            }
          }
        ],
        'categories': [
          {
            'id': '1',
            'name': 'aa',
            'supercategory': 'aa'
          },
          {
            'id': '2',
            'name': 'bb',
            'supercategory': 'bb'
          },
          {
            'id': '1',
            'name': 'aa',
            'supercategory': 'aa'
          },
          {
            'id': '2',
            'name': 'bb',
            'supercategory': 'bb'
          }
        ]
      }
    ]
    import pandas as pd
    ds = ray.data.from_pandas(pd.DataFrame(test_data))
    labels = {"1": "aa", "2": "bb"}
    coco_formater = CocoMerger()
    final_ds = coco_formater.fit(ds).stats_
    print("final_ds", final_ds.take_all())