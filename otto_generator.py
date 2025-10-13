#!user/bin/env python
# -*- coding:utf-8 -*-
"""Stereographic-Projection-of-Otto:
@File: main.py
@Brief: 通过球极投影的方式得到otto的多种形态。
@Author: Golevka2001<gol3vka@163.com>
@Created Date: 2022/11/29
@Last Modified Date: 2022/12/02
github:https://github.com/Golevka2001/Stereographic-Projection-of-Otto
"""

# 开导：
import os

from numpy import ndarray,float32,array,arccos,arctan2,pi,zeros,uint8,cos,sin,ndindex,dot
from PIL import Image

# --------------- 参数部分 --------------- #

# # 原始图像路径：
# PATH_IMG = "./xixi1.png"
# # 投影图像输出路径：
# PATH_PROJ = "./xixi.png"


# # 投影图像输出尺寸（单位：像素）：
# w_proj = 800  # 400
# h_proj = 600  # 300

# # 偏移量（单位：百分比）：
# # 注：用于调整输出的投影图像中心在投影平面上的位置：
# offset_hor = 0  # 水平方向偏移量（向右为正）
# offset_ver = 0.5  # 垂直方向偏移量（向下为正）

# # 缩放倍数
# scale = 1.2  # 1.5

# # 坐标轴的旋转角度：
# # 注：旋转是为了得到不同的球面投影情况（说的道理/栗子头）
# alpha = -5 * np.pi / 180  # 绕x轴旋转角度 -5
# beta = 5 * np.pi / 180  # 绕y轴旋转角度（150°左右可得到栗子头） #-5
# gamma = -10 * np.pi / 180  # 绕z轴旋转角度

# --------------- 实现 --------------- #


def get_point_on_sphere(point: ndarray, r: float) -> ndarray:
    """计算z=0平面上一点Q与投影点D连线在球面上的交点P的坐标

    Args:
        point (np.ndarray): 点Q坐标
        r (float): 球半径

    Returns:
        np.ndarray: 球面上交点P的坐标
    """
    [x, y, z] = point
    k = 2 * r**2 / (x**2 + y**2 + r**2)  # 推导、化简得到的系数（推导过程见README.md）
    return array([k * x, k * y, (k - 1) * r], dtype=float32)


def axis_rotate(point: ndarray, rot_mat: ndarray) -> ndarray:
    """计算坐标系旋转后，点P坐标的变化

    Args:
        point (np.ndarray): 点P坐标
        rot_mat (np.ndarray): 旋转矩阵（推导过程见README.md）

    Returns:
        np.ndarray: 变换后的点P坐标
    """
    return dot(rot_mat, point)


def get_pix_on_img(point: ndarray, r: float, h_img: int, w_img: int) -> tuple:
    """球面投影的逆过程，计算球面上一点P在原图像上的坐标

    Args:
        point (np.ndarray): 点P坐标
        r (float): 球半径
        h_img (int): 原始图像高度
        w_img (int): 原始图像宽度

    Returns:
        tuple: 对应在原始图像上的像素点坐标
    """
    [x, y, z] = point
    if z > r:
        z = r
    row = arccos(z / r) / pi
    col = arctan2(y, x) / 2 / pi + 0.5  # 加0.5是把图像中心移到平面y=0处
    # 坐标范围恢复到原始图像的尺寸：
    row = round(row * h_img) % h_img
    col = round(col * w_img) % w_img
    return (row, col)


def projection(
    pix_proj: tuple, r: float, h_img: int, w_img: int, h_proj: int, w_proj: int,rot_mat,offset_ver,offset_hor
) -> tuple:
    """球极投影

    Args:
        pix_proj (tuple): 投影图像上的像素点坐标
        r (float): 球半径
        h_img (int): 原始图像高度
        w_img (int): 原始图像宽度
        h_proj (int): 投影图像高度
        w_proj (int): 投影图像宽度

    Returns:
        tuple: 对应在原始图像上的像素点坐标
    """
    # 投影图像上像素点坐标转为三维坐标：
    (row, col) = pix_proj
    x = row + (offset_ver - 0.5) * h_proj
    y = col + (offset_hor - 0.5) * w_proj
    z = 0
    Q = array([x, y, z], dtype=float32)
    P = get_point_on_sphere(Q, r)
    P = axis_rotate(P, rot_mat)
    return get_pix_on_img(P, r, h_img, w_img)


def getimage(PATH_IMG,PATH_PROJ,w_proj = 800,h_proj=600,offset_hor = 0,offset_ver = 0.5,scale=1.2,alpha=-5,beta=-5,gamma =0)->Image:
    path_img = os.path.join(os.path.abspath(os.path.dirname(__file__)), PATH_IMG)
    path_proj = os.path.join(os.path.abspath(os.path.dirname(__file__)), PATH_PROJ)

    arr_img = array(Image.open(path_img))
    arr_proj = zeros((h_proj, w_proj, 3), dtype=uint8)

    h_img = arr_img.shape[0]
    w_img = arr_img.shape[1]

    r = min(h_proj, w_proj) / 10 * scale  # 球的半径会影响到投影图像上呈现内容的多少

    # 这个总是被自动格式化成这样很丑
    rot_mat = array(
        [
            [
                cos(gamma) * cos(beta),
                cos(gamma) * sin(beta) * sin(alpha)
                - sin(gamma) * cos(alpha),
                cos(gamma) * sin(beta) * cos(alpha)
                + sin(gamma) * sin(alpha),
            ],
            [
                sin(gamma) * cos(beta),
                sin(gamma) * sin(beta) * sin(alpha)
                + cos(gamma) * cos(alpha),
                sin(gamma) * sin(beta) * cos(alpha)
                - cos(gamma) * sin(alpha),
            ],
            [-sin(beta), cos(beta) * sin(alpha), cos(beta) * cos(alpha)],
        ]
    )

    # 即把目标图像平铺在xy平面上（图片中心在O，所以注意坐标的范围）
    # 遍历每一个像素点，得到在球上的交点坐标，再由球面投影的逆变换对应到原图像上的像素点
    for pix_proj in ndindex(arr_proj.shape[:2]):
        pix_img = projection(pix_proj, r, h_img, w_img, h_proj, w_proj,rot_mat,offset_ver=offset_ver,offset_hor=offset_hor)
        arr_proj[pix_proj] = arr_img[pix_img][:3]

    return Image.fromarray(arr_proj)  # 注释掉这行可以不弹出显示
    #Image.fromarray(arr_proj).save(path_proj)  # 注释掉这行可以不输出文件



if __name__ == "__main__":
    img = getimage(PATH_IMG="./goog.png",PATH_PROJ="./1234.png")
    img.show()