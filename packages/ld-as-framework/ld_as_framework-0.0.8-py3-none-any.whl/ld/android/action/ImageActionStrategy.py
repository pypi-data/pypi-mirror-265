# encoding:utf-8
from ..action.CommonClass import CommonAction

from ..element.Image import ImageQuery, ElementImage

class ImageActionStrategy(CommonAction):

    """
    图片操作对象
    """
    def __init__(self, selector: ImageQuery, eleName, framework):
        pass

    def _find(self):
        return self
