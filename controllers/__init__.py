#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控制器模块初始化文件
"""

from .status_controller import StatusController
from .config_controller import ConfigController
from .message_controller import MessageController
from .news_controller import NewsController
from .contact_controller import ContactController

# 导出所有控制器
__all__ = [
    'StatusController',
    'ConfigController',
    'MessageController',
    'NewsController',
    'ContactController'
]