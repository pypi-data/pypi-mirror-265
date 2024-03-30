# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
"""


import pyarrow as pa

from ray.data.preprocessor import Preprocessor
from ray.util.annotations import PublicAPI



@PublicAPI(stability="alpha")
class Reader(Preprocessor):
    """Reader."""

    def read(self):
        """Read the data."""
        raise NotImplementedError

    def get_schema(self) -> pa.schema:
        """Get the schema of the reader."""
        raise NotImplementedError