#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息管理控制器
只负责接口设计，不包含业务逻辑
"""

from typing import Dict, Any
from services.message_service import MessageService

class MessageController:
    """
    消息管理控制器
    只负责接口设计，不包含业务逻辑
    """
    
    def __init__(self):
        self.message_service = MessageService()
    
    def send_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送消息接口
        
        Args:
            data (dict): 消息数据
            
        Returns:
            dict: 发送结果
        """
        target = data.get('target')
        message = data.get('message')
        target_type = data.get('type', 'friend')
        
        return self.message_service.send_message_business_logic(target, message, target_type)
    
    def start_message_monitoring(self, duration: str = "1h") -> Dict[str, Any]:
        """
        启动消息监控接口
        
        Args:
            duration (str): 监控持续时间
            
        Returns:
            dict: 启动结果
        """
        return self.message_service.start_monitoring_business_logic(duration)
    
    def stop_message_monitoring(self) -> Dict[str, Any]:
        """
        停止消息监控接口
        
        Returns:
            dict: 停止结果
        """
        return self.message_service.stop_monitoring_business_logic()
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """
        获取监控状态接口
        
        Returns:
            dict: 监控状态信息
        """
        return self.message_service.get_monitoring_status_business_logic()
    
    def set_auto_reply_message(self, message: str) -> Dict[str, Any]:
        """
        设置自动回复消息接口
        
        Args:
            message (str): 自动回复消息内容
            
        Returns:
            dict: 设置结果
        """
        return self.message_service.set_auto_reply_message_business_logic(message)