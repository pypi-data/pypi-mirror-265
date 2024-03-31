# encoding:utf-8
from android.graphics import Point

from ascript.android.node import Node

from ...common.Logger import log_ld

class Rect:

    """
    获取控件在屏幕中的位置

    left x坐标

    top y坐标

    width 控件的宽度

    height 控件的高度

    centerX 控件的中心坐标X

    centerY 控件的中心坐标Y
    """
    def __init__(self, rect=None, left=None, top=None, width=None, height=None, centerX=None, centerY=None):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY
        pass

class CommonResult:

    """
    查询元素的公共返回体
    """
    def __init__(self, source_target, framework, find_range: [int, int, int, int] = None):
        """
        调用获取元素方法后拿到的返回结果，经过统一包装
        :param source_target: 查询后的源对象
        :param framework: 框架引用
        :param find_range: 查询范围（节点没有）
        """
        pass

    def _deal_color(self):
        """
        处理颜色对象的方法
        """
        pass

    def _deal_node(self):
        """
        处理节点对象的方法
        """
        pass

    def _deal_image(self):
        """
        处理图片对象的方法
        :return:
        """
        pass

    def click(self, r):
        """
        点击元素所在坐标
        :param r: 随机偏移
        :return:
        """
        pass

class AScriptQueryElement:

    """
    AS元素查询父类，所有的元素查询都需要继承该类
    """
    def __init__(self):
        pass

    def _find_element(self, eleName):
        pass

    def _find_all_element(self, eleName):
        pass

