# encoding:utf-8
import math

import random

import time

from ascript.android import action

from ascript.android.action import Path

from functools import reduce

from ascript.android.screen import CompareColors

from .action.CommonClass import CommonAction

from .base.BaseProperties import AScriptQueryElement, CommonResult

from .element.Color import ColorQuery

from .element.Image import ImageQuery

from .action.ColorActionStrategy import ColorActionStrategy

from .action.ImageActionStrategy import ImageActionStrategy

from .action.NodeActionStrategy import NodeActionStrategy

from typing import cast

from .element.Node import NodeQuery

from ..common.Logger import log_ld

class LDFramework:

    """
    零动框架操作类
    """
    def __init__(self, elements: dict):
        self.elements = elements
        pass

    def _get_query_element(self, *args: str) -> AScriptQueryElement:
        """
        获取查询元素的对象
        :param args: 元素特征值
        :return: 元素查询对象
        """
        pass

    def element(self, *args: str) -> CommonAction:
        """
        获取元素的方法，可以利用获取的元素进行一系列操作
        :param args:元素特征信息
        :return:元素操作对象
        """
            # 如果需要处理的元素是图片
            # 如果需要处理的元素是颜色
            # 如果需要处理的元素是节点
        pass

    def element_exist(self, *args: str) -> CommonAction:
        """
        判断元素是否存在，如果存在返回元素的链式操作对象，不存在返回false
        :param args:
        :return:
        """
        pass

    def click_ele(self, element: list, r=5):
        """
        点击某个元素
        :param element: 需要点击的元素信息
        :param r: 随机范围
        :return:
        """
        pass

    def wait_element(self, element: list, timeout=3) -> CommonAction:
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        pass

    def find_element(self, *args: str) -> CommonResult:
        """
        查找并获取元素返回值
        :param args:元素特征信息
        """
        pass

    def find_all_element(self, *args: str) -> list:
        """
        查找并获取元素返回值
        :param args:元素特征信息
        """
        pass

    def click(x, y, r=5):
        """
        点击坐标
        :param x: X轴
        :param y: Y轴
        :param r: 偏移像素
        """
        # 生成随机角度
        # 生成随机偏移距离
        # 计算新坐标
        pass

    def swipe(from_point: [int, int], to_point: [int, int], timeout=1, will_continue=False, level=0.07):
        """
        滑动的方法，从一个点滑动到另外一个点
        :param level: 弯曲等级，数字越大就越弯曲，不要超过0.1
        :param from_point: 开始的点
        :param to_point: 结束的点
        :param timeout: 整个过程的时间，单位（秒）
        :param will_continue: 滑动完成后是否抬起手指
        :return:
        """
        pass

        # 计算起点和终点之间的对角线长度作为最大偏移量
        # 计算每个节点的坐标,并添加随机偏移
            # 从0到1的步长
    def execute_with_timeout(timeout, func, *args, **kwargs):
        """
        执行指定函数,在给定的超时时间后结束执行

        :param timeout: 超时时间(秒)
        :param func: 要执行的函数
        :param args: 传递给函数的位置参数
        :param kwargs: 传递给函数的关键字参数
        """
            # 避免 CPU 占用过高
        pass

    def sleep(timeout):
        """
        延迟
        :param timeout: 单位秒
        """
        pass

    def compare_color(self, *args) -> bool:
        """
        多点比色
        :param args: 特征信息
        :return: 是否成功
        """
        pass

    def wait_compare_color(self, element: list, timeout: int = 5) -> bool:
        """
        在时间内等待比色成功，在规定时间内仍然比色失败，则返回False
        :param element: 特征信息
        :param timeout: 等待时间
        :return:
        """
        pass

        def tmp(tmp_element: list):
            pass

class 零动框架:

    def __init__(self, 特征库: dict):
        pass

    def 元素_操作(self, *args: str) -> CommonAction:
        """
        获取元素的方法，可以利用获取的元素进行一系列操作
        :param args:元素特征信息
        :return:元素操作对象
        """
        pass

    def 获取_元素(self, *args) -> CommonResult:
        """
        获取元素
        :param args:元素特征信息
        """
        pass

    def 获取_全部元素(self, *args) -> list:
        """
        获取元素
        :param args:元素特征信息
        """
        pass

    def 点击_坐标(x, y, r=5):
        """
        点击坐标
        :param x: X轴
        :param y: Y轴
        :param r: 偏移像素
        """
        pass

    def 点击_元素(self, element: list, r=5):
        """
        点击某个元素
        :param element: 需要点击的元素信息
        :param r: 随机范围
        :return:
        """
        pass

    def 滑动(from_point: [int, int], to_point: [int, int], timeout=1, will_continue=False, level=0.07):
        """
        滑动的方法，从一个点滑动到另外一个点
        :param level: 弯曲等级，数字越大就越弯曲，不要超过0.1
        :param from_point: 开始的点
        :param to_point: 结束的点
        :param timeout: 整个过程的时间
        :param will_continue: 滑动完成后是否抬起手指
        :return:
        """
        pass

    def 元素_等待(self, element: list, timeout=3) -> CommonAction:
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        pass

    def 元素_是否存在(self, *args) -> CommonAction:
        """
        判断元素是否存在，如果存在返回元素的链式操作对象，不存在返回false
        :param args:
        :return:
        """
        pass

    def 延迟(self, timeout):
        pass

    def 比色(self, *args) -> bool:
        """
        多点比色
        :param args: 特征信息
        :return: 是否成功
        """
        pass

    def 等待_比色成功(self, element: list, timeout=5) -> bool:
        """
        在时间内等待比色成功，在规定时间内仍然比色失败，则返回False
        :param element: 特征信息
        :param timeout: 等待时间
        :return:
        """
