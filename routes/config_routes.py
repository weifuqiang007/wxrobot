#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理路由
"""

from flask import Blueprint, jsonify, request, current_app
from controllers.config_controller import ConfigController

config_bp = Blueprint('config', __name__, url_prefix='/api')
config_controller = ConfigController()

@config_bp.route('/config', methods=['GET'])
def get_config():
    """
    获取当前配置
    """
    try:
        result = config_controller.get_config()
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"获取配置失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@config_bp.route('/config', methods=['POST'])
def update_config():
    """
    更新配置
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "请求数据为空"
            }), 400
        
        result = config_controller.update_config(data)
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"更新配置失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500