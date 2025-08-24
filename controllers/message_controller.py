#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息管理控制器
"""

from services.app_service import AppService

class MessageController:
    """
    消息管理控制器
    """
    
    def __init__(self):
        self.app_service = AppService()
    
    def send_message(self, data):
        """
        发送消息
        
        Args:
            data (dict): 消息数据
            
        Returns:
            dict: 发送结果
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            target = data.get('target')
            message = data.get('message')
            target_type = data.get('type', 'friend')  # 默认为好友
            
            if not target or not message:
                return {
                    "success": False,
                    "error": "缺少目标或消息内容",
                    "status_code": 400
                }
            
            success = app_instance.send_message(target, message, target_type)
            
            if success:
                return {
                    "success": True,
                    "message": f"消息已发送到 {target}"
                }
            else:
                return {
                    "success": False,
                    "error": "发送消息失败",
                    "status_code": 500
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }