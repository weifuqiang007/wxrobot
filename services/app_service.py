#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用服务层
管理微信后端应用实例
"""

from app_fixed import WechatBackendApp
import logging

class AppService:
    """
    应用服务类
    单例模式管理微信后端应用实例
    """
    
    _instance = None
    _app_instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.logger = logging.getLogger(__name__)
            self.initialized = True
    
    def get_app_instance(self, config_file="config.json"):
        """
        获取微信后端应用实例
        
        Args:
            config_file (str): 配置文件路径
            
        Returns:
            WechatBackendApp: 应用实例
        """
        if self._app_instance is None:
            try:
                self._app_instance = WechatBackendApp(config_file)
                self.logger.info("微信后端应用实例创建成功")
            except Exception as e:
                self.logger.error(f"创建微信后端应用实例失败: {e}")
                self._app_instance = None
        
        return self._app_instance
    
    def reset_app_instance(self):
        """
        重置应用实例
        """
        if self._app_instance:
            try:
                self._app_instance.stop()
            except Exception as e:
                self.logger.error(f"停止应用实例失败: {e}")
        
        self._app_instance = None
        self.logger.info("应用实例已重置")
    
    def is_app_running(self):
        """
        检查应用是否正在运行
        
        Returns:
            bool: 运行状态
        """
        if self._app_instance:
            return self._app_instance.is_running
        return False