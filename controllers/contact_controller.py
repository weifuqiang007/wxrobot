#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
联系人管理控制器
"""

from services.app_service import AppService

class ContactController:
    """
    联系人管理控制器
    """
    
    def __init__(self):
        self.app_service = AppService()
    
    def get_friends(self):
        """
        获取好友列表
        
        Returns:
            dict: 好友列表
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            friends = app_instance.get_friends()
            return {
                "success": True,
                "data": friends,
                "count": len(friends)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def get_groups(self):
        """
        获取群聊列表
        
        Returns:
            dict: 群聊列表
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            groups = app_instance.get_groups()
            return {
                "success": True,
                "data": groups,
                "count": len(groups)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }