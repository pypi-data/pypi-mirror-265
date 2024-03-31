# encoding:utf-8
import time

from typing import TypeVar

from ..base.BaseProperties import AScriptQueryElement

from ..element.Image import ElementImage

from ..element.Color import ElementColor

from ..element.Node import ElementNode

from ...common.Logger import log_ld

class Method:

    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        pass

    def execute(self):
        pass

CommonActionType = TypeVar('CommonActionType', bound='CommonAction | None')

class CommonAction:

    def __init__(self, selector: AScriptQueryElement, eleName, framework):
        # 查询对象
        # 对框架本身的引用，只要被实例化就绝对不可能为空
        # 当前查询元素的特征信息
        # 用来存放操作的链
        # 查询元素以后的返回值
        pass

    def _find(self):
            return self

    def execute(self, sleep=0.5, loop=1):
        """
        执行动作链
        :param sleep: 执行一次延迟时间，单位（秒）
        :param loop:执行次数
        """
                        # 如果是等待元素之类的任务，需要有元素才可以继续
        pass

    def 执行(self, sleep=0.5, loop=1) -> CommonActionType:
        pass

    def element(self, *args: str) -> CommonActionType:
        """
        查找一个元素，并可以执行后面的操作
        :param args:元素特征信息
        :return: 元素操作对象
        """
        return self

    def 元素_操作(self, *args: str) -> CommonActionType:
        """
        查找一个元素，并可以执行后面的操作
        :param args:元素特征信息
        :return: 元素操作对象
        """
        pass

    def _element(self, *args: str) -> CommonActionType:
        pass

    def sleep(self, second) -> CommonActionType:
        """
        延迟
        :param second:延迟时间，单位秒
        """
        return self

    def 延迟(self, second) -> CommonActionType:
        """
        延迟
        :param second:延迟时间，单位秒
        """
        pass

    def _sleep(self, second) -> CommonActionType:
        return self

    def assert_element(self, condition) -> CommonActionType:
        """
        断言
        :param condition:断言表达式，可以是一个方法，也可以是一个lambda
        """
        return self

    def 断言_元素(self, condition) -> CommonActionType:
        pass

    def _assert_element(self, condition) -> bool:
        pass

    def click(self, x=None, y=None, r=5):
        return self

    def 点击_坐标(self, x=None, y=None, r=5) -> CommonActionType:
        pass

    def _click(self, x, y, r):
        return self

    def click_element(self, r=5):
        """
        如果是节点，该方法是点击节点，如果是其他元素，则是坐标，偏移参数对点击节点无效
        :param r: 偏移像素
        """
        return self

    def 点击_元素(self, r=5) -> CommonActionType:
        """
        如果是节点，该方法是点击节点，如果是其他元素，则是坐标，偏移参数对点击节点无效
        :param r: 偏移像素
        """
        pass

    def _click_element(self, r=5):
        return self

    def wait_element(self, element: list, timeout=3) -> CommonActionType:
        return self

    def 元素_等待(self, element: list, timeout=3) -> CommonActionType:
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        pass

    def _wait_element(self, element: list, timeout=3):
        """
        等待元素出现
        :param element:需要等待的元素特征信息
        :param timeout:等待的时间
        """
        pass

        def tmp():
            pass

        log_ld.debug(f"等待元素结束:{element},返回值：{ele}")

    def swipe(self, from_point: [int, int], to_point: [int, int], timeout=1, will_continue=False):
        """
        执行一个滑动的动作
        :param from_point: 滑动起点
        :param to_point: 滑动终点
        :param timeout: 过程执行时间，单位(秒)
        :param will_continue: 结束时候是否抬起手指
        """
        return self

    def 滑动(self, from_point: [int, int], to_point: [int, int], timeout=1, will_continue=False) -> CommonActionType:
        """
        执行一个滑动的动作
        :param from_point: 滑动起点
        :param to_point: 滑动终点
        :param timeout: 过程执行时间
        :param will_continue: 结束时候是否抬起手指
        """
        pass

    def _swipe(self, from_point, to_point, timeout=1, will_continue=True):
        pass

    def compare_color(self, *args):
        return self

    def 比色(self, *args):
        pass

    def _compare_color(self, *args):
        pass

