#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
联系人管理路由
"""

from flask import Blueprint, jsonify, current_app
from controllers.contact_controller import ContactController

contact_bp = Blueprint('contact', __name__, url_prefix='/api')
contact_controller = ContactController()

@contact_bp.route('/friends', methods=['GET'])
def get_friends():
    """
    获取好友列表
    """
    try:
        result = contact_controller.get_friends()
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"获取好友列表失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@contact_bp.route('/groups', methods=['GET'])
def get_groups():
    """
    获取群聊列表
    """
    try:
        result = contact_controller.get_groups()
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"获取群聊列表失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500