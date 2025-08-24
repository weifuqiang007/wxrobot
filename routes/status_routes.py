#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
状态管理路由
"""

from flask import Blueprint, jsonify, current_app
from controllers.status_controller import StatusController

status_bp = Blueprint('status', __name__, url_prefix='/api')
status_controller = StatusController()

@status_bp.route('/status', methods=['GET'])
def get_status():
    """
    获取服务状态
    """
    try:
        result = status_controller.get_status()
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"获取状态失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500