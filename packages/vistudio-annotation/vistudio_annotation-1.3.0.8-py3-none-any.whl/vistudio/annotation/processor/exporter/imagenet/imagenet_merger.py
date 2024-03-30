#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
formater.py
"""
from ray.data.preprocessor import Preprocessor
import ray


class ImageNetMerger(Preprocessor):
    """
        use this Preprocessor to gather  every item of dataset and convert list
        The purpose is to write this list to txt file
        for example:
        ds = [
             {"item": ['aaa','bbb'], },
             {"item": ['ccc']}
         ]

        merge_list = ImageNetMerger.fit(ds)
        merge_list= ['aaa','bbb', 'ccc']
        """
    def __init__(self):
        self._is_fittable = True
        self._fitted = True

    def _fit(self, ds: "Dataset") -> "Preprocessor":
        list = ds.to_pandas()['item'].to_list()
        self.stats_ = list
        return self


if __name__ == "__main__":
    test_data = [{'item': 's3://bucket/example_110912.jpg 0'},
                 {'item': 's3://bucket/example_110912.jpg 1'},
                 {'item': 's3://bucket/example_110913.jpg 0'},
                 {'item': 's3://bucket/example_110913.jpg 1'}]
    import pandas as pd
    ds = ray.data.from_pandas(pd.DataFrame(test_data))
    imagenet_merger = ImageNetMerger()
    final_list = imagenet_merger.fit(ds).stats_
    print("final_list", final_list)