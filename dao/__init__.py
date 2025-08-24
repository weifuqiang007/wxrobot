#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据访问层(DAO)模块初始化文件
"""

from .config_dao import ConfigDAO
from .wechat_dao import WechatDAO

# 导出所有DAO
__all__ = [
    'ConfigDAO',
    'WechatDAO'
]