# encoding:utf-8
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
    def __init__(self, left=None, top=None, width=None, height=None, centerX=None, centerY=None):
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
    def __init__(self, source_target, rect: Rect):
        """
        调用获取元素方法后拿到的返回结果，经过统一包装
        :param source_target: 查询后的源对象
        :param rect: 查询后得到的坐标信息对象，要自行包装
        """
        pass

class AScriptQueryElement:

    """
    AS元素查询父类，所有的元素查询都需要继承该类
    """
    def __init__(self):
        pass

    def _find_element(self, eleName) -> CommonResult:
        pass

    def _find_all_element(self, eleName) -> list:
        pass

