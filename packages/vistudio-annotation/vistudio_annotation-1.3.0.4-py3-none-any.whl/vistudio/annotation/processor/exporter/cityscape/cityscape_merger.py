#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
CityscapeMerger
"""
import pandas as pd
import ray.data
from ray.data.preprocessor import Preprocessor


class CityscapeMerger(Preprocessor):
    """
    use this Preprocessor to merge  every item of dataset  and convert list
    The purpose is to write this list to txt file
    for example:
    ds = [
         {"item": 'aaa' },
         {"item": 'bbb'}
     ]

    merge_list = CityscapeMerger.fit(ds)
    merge_list= ['aaa','bbb']
    """

    def __init__(self):
        self._is_fittable = True
        self._fitted = True

    def _fit(self, ds: "Dataset") -> "Preprocessor":
        list = ds.to_pandas()['item'].to_list()
        self.stats_ = list
        return self


if __name__ == "__main__":
    data = [{'item': 'example_110912.jpg windmill/store/workspaces/cjftest/example_110912.png\n'},
            {'item': 'example_110913.jpg windmill/store/workspaces/cjftest/example_110913.png\n'}]
    ds = ray.data.from_pandas(pd.DataFrame(data))
    cityscape_merge = CityscapeMerger()
    final_list = cityscape_merge.fit(ds).stats_
    print("final_list", final_list)
