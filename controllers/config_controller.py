#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理控制器
"""

from services.app_service import AppService

class ConfigController:
    """
    配置管理控制器
    """
    
    def __init__(self):
        self.app_service = AppService()
    
    def get_config(self):
        """
        获取当前配置
        
        Returns:
            dict: 配置信息
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            config = app_instance.get_config()
            return {
                "success": True,
                "data": config
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def update_config(self, data):
        """
        更新配置
        
        Args:
            data (dict): 配置数据
            
        Returns:
            dict: 更新结果
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            config_type = data.get('type')
            if not config_type:
                return {
                    "success": False,
                    "error": "缺少配置类型",
                    "status_code": 400
                }
            
            # 提取配置参数
            config_params = {k: v for k, v in data.items() if k != 'type'}
            
            success = app_instance.update_config(config_type, **config_params)
            
            if success:
                return {
                    "success": True,
                    "message": "配置更新成功"
                }
            else:
                return {
                    "success": False,
                    "error": "配置更新失败",
                    "status_code": 500
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }