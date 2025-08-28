#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路由模块初始化文件
"""

from .health_routes import health_bp
from .status_routes import status_bp
from .config_routes import config_bp
from .message_routes import message_bp
from .news_routes import news_bp
from .contact_routes import contact_bp
from .welcome_routes import welcome_bp

# 导出所有蓝图
__all__ = [
    'health_bp',
    'status_bp', 
    'config_bp',
    'message_bp',
    'news_bp',
    'contact_bp',
    'welcome_bp'
]