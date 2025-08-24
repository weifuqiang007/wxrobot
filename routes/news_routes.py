#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻管理路由
"""

from flask import Blueprint, jsonify, request, current_app
from controllers.news_controller import NewsController

news_bp = Blueprint('news', __name__, url_prefix='/api/news')
news_controller = NewsController()

@news_bp.route('/groups', methods=['GET'])
def get_news_groups():
    """
    获取新闻推送群组列表
    """
    try:
        result = news_controller.get_news_groups()
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"获取新闻群组失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@news_bp.route('/groups', methods=['POST'])
def add_news_group():
    """
    添加新闻推送群组
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "请求数据为空"
            }), 400
        
        result = news_controller.add_news_group(data)
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"添加新闻群组失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@news_bp.route('/groups', methods=['DELETE'])
def remove_news_group():
    """
    移除新闻推送群组
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "请求数据为空"
            }), 400
        
        result = news_controller.remove_news_group(data)
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"移除新闻群组失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@news_bp.route('/time', methods=['POST'])
def set_news_time():
    """
    设置新闻推送时间
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "请求数据为空"
            }), 400
        
        result = news_controller.set_news_time(data)
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"设置新闻推送时间失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@news_bp.route('/test', methods=['GET'])
def test_news():
    """
    测试新闻获取
    """
    try:
        result = news_controller.test_news()
        return jsonify(result), result.get('status_code', 200)
        
    except Exception as e:
        current_app.logger.error(f"测试新闻获取失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500