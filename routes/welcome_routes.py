#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新成员欢迎路由
定义新成员欢迎相关的API路由
"""

from flask import Blueprint
from controllers.welcome_controller import WelcomeController

# 创建蓝图
welcome_bp = Blueprint('welcome', __name__, url_prefix='/api/welcome')

# 创建控制器实例
welcome_controller = WelcomeController()

@welcome_bp.route('/monitoring/start', methods=['POST'])
def start_welcome_monitoring():
    """
    启动新成员欢迎监听
    这个接口是 启动新成员欢迎监听 的API端点，用于开始监控微信群聊中的新成员加入事件并自动发送欢迎消息。
    
    POST /api/welcome/monitoring/start
    
    Request Body:
    {
        "groups": ["群组1", "群组2"],  // 可选，要监听的群组列表，不传则监听所有群组
        "duration": "24h"              // 可选，监听持续时间，默认24小时
    }
    
    Returns:
        JSON响应
        {
    "data": {
        "duration": "24h",
        "monitored_groups": [
            "测试微信发送消息"
        ],
        "start_time": 1756346048.6187952,
        "status": "started"
    },
    "message": "新成员欢迎监听已启动，监听 1 个群组",
    "success": true
}
    """
    return welcome_controller.start_welcome_monitoring()

@welcome_bp.route('/monitoring/stop', methods=['POST'])
def stop_welcome_monitoring():
    """
    停止新成员欢迎监听
    
    POST /api/welcome/monitoring/stop
    
    Returns:
        JSON响应
    """
    return welcome_controller.stop_welcome_monitoring()

@welcome_bp.route('/monitoring/status', methods=['GET'])
def get_welcome_monitoring_status():
    """
    获取新成员欢迎监听状态
    
    GET /api/welcome/monitoring/status
    
    Returns:
        JSON响应，包含监听状态信息
    """
    return welcome_controller.get_welcome_monitoring_status()

@welcome_bp.route('/template', methods=['POST'])
def set_welcome_message_template():
    """
    设置欢迎消息模板
    
    POST /api/welcome/template
    
    Request Body:
    {
        "template": "欢迎 @{member_name} 加入群聊！🎉"  // 欢迎消息模板，支持 {member_name} 占位符
    }
    
    Returns:
        JSON响应
    """
    return welcome_controller.set_welcome_message_template()

@welcome_bp.route('/template', methods=['GET'])
def get_welcome_message_template():
    """
    获取当前欢迎消息模板
    
    GET /api/welcome/template
    
    Returns:
        JSON响应，包含当前模板
    """
    return welcome_controller.get_welcome_message_template()

@welcome_bp.route('/groups', methods=['GET'])
def get_monitored_groups():
    """
    获取可监听的群组列表
    
    GET /api/welcome/groups
    
    Returns:
        JSON响应，包含所有群组和当前监听的群组
    """
    return welcome_controller.get_monitored_groups()