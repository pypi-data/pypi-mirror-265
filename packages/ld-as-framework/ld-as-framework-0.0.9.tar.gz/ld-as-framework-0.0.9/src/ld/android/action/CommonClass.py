# encoding:utf-8
import time

from typing import TypeVar

from ..base.BaseProperties import AScriptQueryElement, CommonResult

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
        :param condition:断言表达式，可以是一个方法，也可以是一个lambda，如果返回False，则不执行后面的链
        """
        return self

    def 断言_元素(self, condition) -> CommonActionType:
        """
        断言
        :param condition:断言表达式，可以是一个方法，也可以是一个lambda，如果返回False，则不执行后面的链
        """
        pass

    def _assert_element(self, condition) -> bool:
        pass

    def execute_method(self, method) -> CommonActionType:
        """
        执行一个方法，如果方法返回False，则不继续执行后面的链
        :param method:需要执行的方法
        """
        return self

    def 执行_方法(self, method) -> CommonActionType:
        """
        执行一个方法，如果方法返回False，则不继续执行后面的链
        :param method:需要执行的方法
        """
        pass

    def _execute_method(method) -> bool:
        pass

    def click(self, x=None, y=None, r=5, rx: int = 0, ry: int = 0):
        """
        点击某个坐标，如果不穿参数，则是点击找到元素的位置
        :param x:屏幕的绝对x坐标，和y一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param y:屏幕的绝对y坐标，和x一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param r:随机偏移坐标，以x,y为中心，点击的时候偏移r个像素
        :param rx:相对坐标x，以x（不管是元素的还是传入的）为中心加上rx作为点击的偏移像素
        :param ry:相对坐标y，以y（不管是元素的还是传入的）为中心加上ry作为点击的偏移像素
        """
        return self

    def 点击_坐标(self, x=None, y=None, r=5, rx: int = 0, ry: int = 0) -> CommonActionType:
        """
        点击某个坐标，如果不穿参数，则是点击找到元素的位置
        :param x:屏幕的绝对x坐标，和y一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param y:屏幕的绝对y坐标，和x一起使用，点击屏幕上的一个点，如果不填写则使用找到元素的位置
        :param r:随机偏移坐标，以x,y为中心，点击的时候偏移r个像素
        :param rx:相对坐标x，以x（不管是元素的还是传入的）为中心加上rx作为点击的偏移像素
        :param ry:相对坐标y，以y（不管是元素的还是传入的）为中心加上ry作为点击的偏移像素
        """
        pass

    def _click(self, x, y, r, rx=0, ry=0):
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

