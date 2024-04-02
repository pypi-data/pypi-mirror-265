# encoding:utf-8
import logging

class _MyLogger(logging.Logger):

    def __init__(self, name, level=logging.INFO):
        pass

log_ld = _MyLogger("零动插件", logging.INFO)

log = _MyLogger("日志", logging.INFO)

__all__ = ['log_ld', 'log']

