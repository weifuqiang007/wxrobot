#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息管理路由
"""

from flask import Blueprint, jsonify, request
from controllers.message_controller import MessageController

message_bp = Blueprint('message', __name__, url_prefix='/api')
message_controller = MessageController()

@message_bp.route('/send-message', methods=['POST'])
def send_message():
    """
    发送消息路由
    """
    data = request.get_json()
    result = message_controller.send_message(data)
    return jsonify(result), result.get('status_code', 200)

@message_bp.route('/start-monitoring', methods=['POST'])
def start_monitoring():
    """
    启动消息监控路由
    """
    data = request.get_json() or {}
    duration = data.get('duration', '1h')
    result = message_controller.start_message_monitoring(duration)
    return jsonify(result), result.get('status_code', 200)

@message_bp.route('/stop-monitoring', methods=['POST'])
def stop_monitoring():
    """
    停止消息监控路由
    """
    result = message_controller.stop_message_monitoring()
    return jsonify(result), result.get('status_code', 200)

@message_bp.route('/monitoring-status', methods=['GET'])
def get_monitoring_status():
    """
    获取消息监控状态路由
    """
    result = message_controller.get_monitoring_status()
    return jsonify(result), 200

@message_bp.route('/set-auto-reply', methods=['POST'])
def set_auto_reply():
    """
    设置自动回复消息路由
    """
    data = request.get_json()
    message = data.get('message') if data else None
    result = message_controller.set_auto_reply_message(message)
    return jsonify(result), result.get('status_code', 200)