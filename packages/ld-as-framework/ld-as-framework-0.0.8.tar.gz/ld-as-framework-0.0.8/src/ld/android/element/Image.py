# encoding:utf-8
from ...common.Logger import log_ld

from ..base.BaseProperties import AScriptQueryElement, CommonResult

from ascript.android.system import R

from ascript.android.screen import FindImages

class ImageQuery(AScriptQueryElement):

    def __init__(self, mode="find"):
        # 局部图片名称或路径 当只填写图片名称时,将在res/img下找到该名称的图片
        # 非必填，圈定屏幕范围
        # 图片结果的可信度0-1之间, 1为100%匹配,低于该可信度的结果将被过滤掉 默认:0.9
        pass

    def res(self, part_img: str):
        return self

    def sd(self, part_img: str):
        return self

    def rect(self, x, y, x1, y1):
        return self

    def confidence(self, confidence: float):
        return self

    def _find_element(self, eleName):
        pass

    def _find_all_element(self, eleName):
        pass

class ElementImage(CommonResult):

    def click(self, r):
        pass

