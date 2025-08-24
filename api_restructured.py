#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信后端REST API接口（重构版本）
采用MVC架构模式，分离路由、控制器和服务层
"""

from flask import Flask
from flask_cors import CORS
import logging
import traceback

# 导入路由蓝图
from routes import (
    health_bp,
    status_bp,
    config_bp,
    message_bp,
    news_bp,
    contact_bp
)

def create_app(config_file="config.json"):
    """
    创建Flask应用
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        Flask: Flask应用实例
    """
    # 创建Flask应用
    app = Flask(__name__)
    
    # 启用CORS
    CORS(app)
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app.logger.info("正在初始化微信后端API服务...")
    
    # 注册错误处理器
    register_error_handlers(app)
    
    # 注册路由蓝图
    register_blueprints(app)
    
    app.logger.info("微信后端API服务初始化完成")
    
    return app

def register_error_handlers(app):
    """
    注册错误处理器
    
    Args:
        app: Flask应用实例
    """
    from flask import jsonify
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "API端点不存在",
            "code": 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": "服务器内部错误",
            "code": 500
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": "请求参数错误",
            "code": 400
        }), 400
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"未处理的异常: {error}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": "服务器内部错误",
            "code": 500
        }), 500

def register_blueprints(app):
    """
    注册路由蓝图
    
    Args:
        app: Flask应用实例
    """
    # 注册所有蓝图
    app.register_blueprint(health_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(config_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(contact_bp)
    
    app.logger.info("所有路由蓝图注册完成")

def main():
    """
    主函数 - 启动API服务器
    """
    print("🚀 启动微信后端API服务器（重构版本）...")
    
    try:
        app = create_app()
        
        # 启动服务器
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 用户中断，API服务器停止")
    except Exception as e:
        print(f"❌ API服务器启动失败: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()