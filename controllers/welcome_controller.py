#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新成员欢迎控制器
处理新成员欢迎相关的HTTP请求和响应
"""

import logging
from typing import Dict, Any, List, Optional
from flask import request, jsonify

from services.welcome_service import WelcomeService

class WelcomeController:
    """
    新成员欢迎控制器类
    负责处理新成员欢迎相关的HTTP请求和响应
    """
    
    def __init__(self):
        self.welcome_service = WelcomeService()
        self.logger = logging.getLogger(__name__)
    
    def start_welcome_monitoring(self) -> Dict[str, Any]:
        """
        启动新成员欢迎监听
        
        Returns:
            dict: HTTP响应数据
        """
        try:
            # 获取请求参数
            data = request.get_json() or {}
            groups = data.get('groups')  # 可选的群组列表
            duration = data.get('duration', '24h')  # 默认24小时
            
            # 参数验证
            if groups is not None and not isinstance(groups, list):
                return {
                    'success': False,
                    'message': '群组列表参数格式错误，应为数组',
                    'data': None
                }, 400
            
            if not isinstance(duration, str) or not duration.strip():
                return {
                    'success': False,
                    'message': '持续时间参数格式错误',
                    'data': None
                }, 400
            
            # 调用服务层业务逻辑
            result = self.welcome_service.start_welcome_monitoring_business_logic(
                groups=groups,
                duration=duration.strip()
            )
            
            # 根据业务逻辑结果返回HTTP状态码
            if result['success']:
                return result, 200
            else:
                return result, 400
                
        except Exception as e:
            self.logger.error(f"启动新成员欢迎监听请求处理失败: {e}")
            return {
                'success': False,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }, 500
    
    def stop_welcome_monitoring(self) -> Dict[str, Any]:
        """
        停止新成员欢迎监听
        
        Returns:
            dict: HTTP响应数据
        """
        try:
            # 调用服务层业务逻辑
            result = self.welcome_service.stop_welcome_monitoring_business_logic()
            
            # 根据业务逻辑结果返回HTTP状态码
            if result['success']:
                return result, 200
            else:
                return result, 400
                
        except Exception as e:
            self.logger.error(f"停止新成员欢迎监听请求处理失败: {e}")
            return {
                'success': False,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }, 500
    
    def get_welcome_monitoring_status(self) -> Dict[str, Any]:
        """
        获取新成员欢迎监听状态
        
        Returns:
            dict: HTTP响应数据
        """
        try:
            # 调用服务层业务逻辑
            result = self.welcome_service.get_welcome_monitoring_status_business_logic()
            
            # 根据业务逻辑结果返回HTTP状态码
            if result['success']:
                return result, 200
            else:
                return result, 500
                
        except Exception as e:
            self.logger.error(f"获取新成员欢迎监听状态请求处理失败: {e}")
            return {
                'success': False,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }, 500
    
    def set_welcome_message_template(self) -> Dict[str, Any]:
        """
        设置欢迎消息模板
        
        Returns:
            dict: HTTP响应数据
        """
        try:
            # 获取请求参数
            data = request.get_json() or {}
            template = data.get('template')
            
            # 参数验证
            if not template or not isinstance(template, str):
                return {
                    'success': False,
                    'message': '欢迎消息模板参数不能为空且必须为字符串',
                    'data': None
                }, 400
            
            # 调用服务层业务逻辑
            result = self.welcome_service.set_welcome_message_template_business_logic(
                template=template
            )
            
            # 根据业务逻辑结果返回HTTP状态码
            if result['success']:
                return result, 200
            else:
                return result, 400
                
        except Exception as e:
            self.logger.error(f"设置欢迎消息模板请求处理失败: {e}")
            return {
                'success': False,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }, 500
    
    def get_monitored_groups(self) -> Dict[str, Any]:
        """
        获取可监听的群组列表
        
        Returns:
            dict: HTTP响应数据
        """
        try:
            # 调用服务层业务逻辑
            result = self.welcome_service.get_monitored_groups_business_logic()
            
            # 根据业务逻辑结果返回HTTP状态码
            if result['success']:
                return result, 200
            else:
                return result, 500
                
        except Exception as e:
            self.logger.error(f"获取群组列表请求处理失败: {e}")
            return {
                'success': False,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }, 500
    
    def get_welcome_message_template(self) -> Dict[str, Any]:
        """
        获取当前欢迎消息模板
        
        Returns:
            dict: HTTP响应数据
        """
        try:
            # 直接从服务层获取当前模板
            template = self.welcome_service.welcome_message_template
            
            return {
                'success': True,
                'message': '获取欢迎消息模板成功',
                'data': {
                    'template': template
                }
            }, 200
                
        except Exception as e:
            self.logger.error(f"获取欢迎消息模板请求处理失败: {e}")
            return {
                'success': False,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }, 500