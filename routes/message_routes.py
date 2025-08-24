#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息管理路由
"""

from flask import Blueprint, jsonify, request, current_app
from controllers.message_controller import MessageController

message_bp = Blueprint('message', __name__, url_prefix='/api')
message_controller = MessageController()

@message_bp.route('/send-message', methods=['POST'])
def send_message():
    """
    发送消息
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "请求数据为空"
            }), 400
        
        result = message_controller.send_message(data)
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"发送消息失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500