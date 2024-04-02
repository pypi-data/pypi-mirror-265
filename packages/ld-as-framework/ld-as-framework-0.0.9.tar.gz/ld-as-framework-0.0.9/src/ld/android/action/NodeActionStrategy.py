# encoding:utf-8
from time import sleep

from .CommonClass import CommonAction, Method

from ..element.Node import NodeQuery

from ...common.Logger import log_ld

class NodeActionStrategy(CommonAction):

    """
    节点操作对象
    """
    def __init__(self, selector: NodeQuery, eleName, framework):
        pass

    def _click_element(self, r=5):
        return self

    def long_click(self):
        """
        长安查询到的节点信息，如果没有查询到则不执行
        """
        return self

    def 长按_节点(self):
        """
        长安查询到的节点信息，如果没有查询到则不执行
        """
        pass

    def _long_click(self):
        return self

    def input(self, msg: str):
        """
        长安查询到的节点信息，如果没有查询到则不执行
        """
        return self

    def 输入_文本(self, msg: str):
        """
        对查询到的节点信息输入文本
        """
        pass

    def _input(self, msg):
        return self
