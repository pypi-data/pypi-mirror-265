# encoding:utf-8
from ...common.Logger import log_ld

from ..base.BaseProperties import AScriptQueryElement, CommonResult, Rect

from ascript.android.system import R

from ascript.android.screen import FindImages

class BaseImageQuery(AScriptQueryElement):

    def __init__(self):
        # 局部图片名称或路径 当只填写图片名称时,将在res/img下找到该名称的图片
        # 非必填，圈定屏幕范围
        # 图片结果的可信度0-1之间, 1为100%匹配,低于该可信度的结果将被过滤掉 默认:0.9
        pass

    def img(self, part_img: str):
        return self

    def res(self, part_img: str):
        return self

    def sd(self, part_img: str):
        return self

    def rect(self, x, y, x1, y1):
        return self

    def confidence(self, confidence: float):
        return self

    def _build_result(ele_target):
        """
        包装统一返回类
        :param ele_target: 原始返回对象
        """
        pass

    def _find_element(self, eleName):
        pass

    def _find_all_element(self, eleName):
        pass

class ImageFindQuery(BaseImageQuery):

    def __init__(self):
        pass

    def _find_all_element(self, eleName):
        pass

class ImageFindTemplateQuery(BaseImageQuery):

    def __init__(self):
        # 参数为False: 使用灰度图匹配
        # 参数为True:使用原色图匹配.
        pass

    def rgb(self, rgb: bool = True):
        return self

    def _find_all_element(self, eleName):
        # 查询所有也没有rgb
        pass

class ImageFindSiftQuery(BaseImageQuery):

    def __init__(self):
        # 参数为False: 使用灰度图匹配
        # 参数为True:使用原色图匹配.
        pass

    def _find_all_element(self, eleName):
        pass

class ImageQuery:

    def find() -> ImageFindQuery:
        pass

    def find_template() -> ImageFindTemplateQuery:
        pass

    def find_sift() -> ImageFindSiftQuery:
        pass

