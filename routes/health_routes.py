#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康检查路由
"""

from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint('health', __name__, url_prefix='/api')

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    健康检查接口
    """
    return jsonify({
        "success": True,
        "message": "微信后端API服务正常",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@health_bp.route('/docs', methods=['GET'])
def api_docs():
    """
    API文档
    """
    docs = {
        "title": "微信后端自动化系统 API",
        "version": "1.0.0",
        "description": "提供微信自动化操作的REST API接口",
        "endpoints": {
            "GET /api/health": "健康检查",
            "GET /api/status": "获取服务状态",
            "GET /api/config": "获取当前配置",
            "POST /api/config": "更新配置",
            "GET /api/friends": "获取好友列表",
            "GET /api/groups": "获取群聊列表",
            "POST /api/send-message": "发送消息",
            "GET /api/news/groups": "获取新闻推送群组",
            "POST /api/news/groups": "添加新闻推送群组",
            "DELETE /api/news/groups": "移除新闻推送群组",
            "POST /api/news/time": "设置新闻推送时间",
            "GET /api/news/test": "测试新闻获取",
            "GET /api/docs": "API文档"
        }
    }
    
    return jsonify({
        "success": True,
        "data": docs
    })