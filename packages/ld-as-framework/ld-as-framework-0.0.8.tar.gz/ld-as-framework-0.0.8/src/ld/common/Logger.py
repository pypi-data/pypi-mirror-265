# encoding:utf-8
import logging

class _MyLogger(logging.Logger):

    def __init__(self, name, level=logging.INFO):
        pass

log_ld = _MyLogger("零动插件", logging.DEBUG)

log = _MyLogger("日志", logging.DEBUG)

__all__ = ['log_ld', 'log']

