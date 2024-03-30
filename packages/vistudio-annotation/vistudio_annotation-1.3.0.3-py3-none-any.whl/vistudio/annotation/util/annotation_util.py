#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Authors: chujianfei
Date:    2024/02/22-11:56 AM
"""
import sys
from typing import List, Union, Iterator, Dict, Tuple
import numpy as np
import cv2

import xxhash
import base64


def fill_mask_with_rle(mask, rle: list, label_id: int):
    """
    generate mask from rle
    """
    sharpe = mask.shape
    pixel_count = 0
    for index, num_float in enumerate(rle):
        num = int(num_float)
        if index % 2 == 0:
            continue

        for i in range(0, num):
            m = (pixel_count + i) // sharpe[1]
            n = (pixel_count + i) % sharpe[1]
            mask[m][n] = label_id
        pixel_count += num


def fill_mask_with_polygon(mask, points: list, label_id: int):
    """
    generate mask from polygon
    """
    if len(points) % 2 == 0:
        polygon = [points[i:i + 2] for i in range(0, len(points), 2)]
        obj = np.array(object=[polygon], dtype=np.int32)
        cv2.fillPoly(img=mask, pts=obj, color=label_id)


def polygon_bbox_with_wh(polygon):
    """
    获取polygon的外接框。
    params:  polygon: 多边形。
    return:  bbox: 边界框 x, y, w, h
    """
    ymin, ymax, xmin, xmax = polygon_bbox(polygon)
    return xmin, ymin, xmax - xmin, ymax - ymin


def rle2mask(height, width, rle, gray=255):
        """
        Args:
            -rle: numpy array, 连续0或1的个数， 从0开始
            -height: 图片height
            -width: 图片width
        Returns:
            -mask: rle对应的mask
        """
        mask = np.zeros(height * width).astype(np.uint8)
        start = 0
        pixel = 0
        for num in rle:
            stop = start + num
            mask[start:stop] = pixel
            pixel = gray - pixel
            start = stop
        return mask.reshape(height, width)


def mask_bbox_with_wh(mask):
    """
    获取mask的外接框，包含height和width
    """
    polygons = mask2polygons(mask)
    return polygons_bbox_with_wh(polygons)


def mask2polygons(mask):
    """
    提取mask中所有的polygon
    """
    contours, hierarchy = cv2.findContours((mask).astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    segmentation = []
    for contour in contours:
        contour_list = contour.flatten().tolist()
        if len(contour_list) > 4:
            segmentation.append(contour_list)
    return segmentation


def polygons_bbox_with_wh(polygons):
    """
    获取多个polygon的外接框，包含height和width
    """
    ymin, ymax, xmin, xmax = polygons_bbox(polygons)
    return xmin, ymin, xmax - xmin, ymax - ymin


def polygons_bbox(polygons):
    """
    获取多个polygon的外接框范围
    """
    xmin, ymin = sys.maxsize, sys.maxsize
    xmax, ymax = 0, 0
    for polygon in polygons:
        ymin1, ymax1, xmin1, xmax1 = polygon_bbox(polygon)
        xmin = min(xmin, xmin1)
        xmax = max(xmax, xmax1)
        ymin = min(ymin, ymin1)
        ymax = max(ymax, ymax1)
    return ymin, ymax, xmin, xmax


def polygon_bbox(polygon):
    """
    获取polygon的外接框
    """
    xmin, ymin = sys.maxsize, sys.maxsize
    xmax, ymax = 0, 0
    for i in range(0, len(polygon), 2):
        x, y = int(polygon[i]), int(polygon[i + 1])
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)
    return ymin, ymax, xmin, xmax


def polygon_area(polygon: List[float]) -> float:
    """
    计算polygon的面积
    """
    x, y = np.array(polygon[::2]), np.array(polygon[1::2])
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def rle_area(rle):
    """
    计算rle的面积
    """
    area = 0
    for i in range(1, len(rle), 2):
        area += rle[i]
    return area


def generate_md5(data):
    """
    生成md5
    :param data:
    :return:
    """
    hash64 = xxhash.xxh64(data).hexdigest()
    return hash64


def generate_random_string(length):
    """
    生成一个随机字符串
    :param length:
    :return:
    """
    import random
    import string
    # 可选的字符集合
    characters = string.ascii_letters + string.digits + string.punctuation
    # 生成随机字符串
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def encode_to_base64(input_string):
    """
    将给定的字符串编码为 Base64 格式。

    参数:
    input_string (str): 要编码的字符串。

    返回:
    str: Base64 编码后的字符串。
    """
    # 将字符串编码为字节对象
    input_bytes = input_string.encode('utf-8')

    # 使用 base64 编码
    base64_encoded = base64.b64encode(input_bytes)

    # 将字节对象转换为字符串
    base64_string = base64_encoded.decode('utf-8')

    return base64_string


def decode_from_base64(base64_string):
    """
    将给定的 Base64 编码字符串解码为原始字符串。

    参数:
    base64_string (str): Base64 编码的字符串。

    返回:
    str: 解码后的原始字符串。
    """
    # 将 Base64 字符串解码为字节对象
    base64_bytes = base64_string.encode('utf-8')

    # 使用 base64 解码
    decoded_bytes = base64.b64decode(base64_bytes)

    # 将字节对象解码为字符串
    decoded_string = decoded_bytes.decode('utf-8')

    return decoded_string


def generate_random_digits(length=6):
    import string
    import random
    """
    生成指定长度的随机数字字符串。

    参数：
    length (int): 生成的字符串长度，默认为 6。

    返回：
    str: 生成的随机数字字符串。
    """
    # 定义包含数字 0 到 9 的字符串
    digits = string.digits

    # 使用 random 模块生成指定长度的随机数字字符串
    random_string = ''.join(random.choice(digits) for _ in range(length))

    return random_string



