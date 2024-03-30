#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Authors: chujianfei
Date:    2024/02/22-11:56 AM
"""


def convert_ext_with_png(file_name):
    """
    转换文件后缀为png
    """
    import os
    splitext = os.path.splitext(file_name)
    if len(splitext) == 2:
        return os.path.splitext(file_name)[0] + ".png"
    return file_name