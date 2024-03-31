# encoding:utf-8
from .CommonClass import CommonAction

from ..element.Color import ColorQuery, ElementColor

from ...common.Logger import log_ld

class ColorActionStrategy(CommonAction):

    """
    颜色操作对象
    """
    def __init__(self, selector: ColorQuery, eleName, framework):
        pass

    def _find(self):
        return self
