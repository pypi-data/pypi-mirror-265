# __init__.py 为初始化加载文件
# from .test import *
from .common.Logger import log_ld

# 把日志级别设置为INFO，生产环境打开
log_ld.setLevel(20)

