# !/usr/bin/env python3.10
# -*- coding: utf-8 -*-
import conf
import logging


def __set_logger():
    _logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s]  [%(levelname)s]\t%(message)s')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    _logger.setLevel(conf.LOG_LEVEL)
    return _logger


logger = __set_logger()
