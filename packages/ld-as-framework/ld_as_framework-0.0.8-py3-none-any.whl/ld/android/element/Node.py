# encoding:utf-8
from ascript.android.node import Selector

from ascript.android.node import Node

from ...common.Logger import log_ld

from ..base.BaseProperties import AScriptQueryElement, Rect, CommonResult

class NodeQuery(Selector, AScriptQueryElement):

    """
    节点查询对象
    """
    def _find_element(self, eleName):
        pass

    def _find_all_element(self, eleName):
        pass

class ElementNode(CommonResult, Node):

    """
       控件返回的节点，其属性如下

          id            控件ID 部分APP中ID属性,随手机安装可能动态变化,谨慎使用

          text          控件的文本

          type          控件的类型

          desc          控件的描述

          hintText      控件的默认展示文本

          packageName   控件所属包名

          childCount    子控件数量

          inputType     输入类型

          maxTextLength 控件最大文本长度

          drawingOrder  是否可点击

          checkable     是否可选中

          checked       是否已选中

          editable      是否支持编辑

          enabled       是否可访问

          visible       是否针对用户展示

          dismissable   是否可取消

          focusable     是否可以获取焦点

          focused       是否已获取了焦点

          longClickable 是否可以长按
       """
    def __init__(self, source_target, framework):
        pass

