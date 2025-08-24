#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
状态管理控制器
"""

from services.app_service import AppService

class StatusController:
    """
    状态管理控制器
    """
    
    def __init__(self):
        self.app_service = AppService()
    
    def get_status(self):
        """
        获取服务状态
        
        Returns:
            dict: 状态信息
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            status = app_instance.get_status()
            return {
                "success": True,
                "data": status
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }