#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信后端REST API接口（修复版本）
使用简化的WechatService避免pywechat语法错误
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import traceback

from config import ConfigManager
from app_fixed import WechatBackendApp

# 全局应用实例
app_instance = None

def create_app(config_file="config.json"):
    """
    创建Flask应用
    
    Args:
        config_file: 配置文件路径
        
    Returns:
        Flask: Flask应用实例
    """
    global app_instance
    
    # 创建Flask应用
    app = Flask(__name__)
    
    # 启用CORS
    CORS(app)
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建微信后端应用实例
    try:
        app_instance = WechatBackendApp(config_file)
        app.logger.info("微信后端应用实例创建成功")
    except Exception as e:
        app.logger.error(f"创建微信后端应用实例失败: {e}")
        app_instance = None
    
    # 错误处理器
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
    
    # API路由
    
    @app.route('/api/health', methods=['GET'])
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
    
    @app.route('/api/status', methods=['GET'])
    def get_status():
        """
        获取服务状态
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            status = app_instance.get_status()
            return jsonify({
                "success": True,
                "data": status
            })
            
        except Exception as e:
            app.logger.error(f"获取状态失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/config', methods=['GET'])
    def get_config():
        """
        获取当前配置
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            config = app_instance.get_config()
            return jsonify({
                "success": True,
                "data": config
            })
            
        except Exception as e:
            app.logger.error(f"获取配置失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/config', methods=['POST'])
    def update_config():
        """
        更新配置
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            data = request.get_json()
            if not data:
                return jsonify({
                    "success": False,
                    "error": "请求数据为空"
                }), 400
            
            config_type = data.get('type')
            if not config_type:
                return jsonify({
                    "success": False,
                    "error": "缺少配置类型"
                }), 400
            
            # 提取配置参数
            config_params = {k: v for k, v in data.items() if k != 'type'}
            
            success = app_instance.update_config(config_type, **config_params)
            
            if success:
                return jsonify({
                    "success": True,
                    "message": "配置更新成功"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "配置更新失败"
                }), 500
                
        except Exception as e:
            app.logger.error(f"更新配置失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/friends', methods=['GET'])
    def get_friends():
        """
        获取好友列表
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            friends = app_instance.get_friends()
            return jsonify({
                "success": True,
                "data": friends,
                "count": len(friends)
            })
            
        except Exception as e:
            app.logger.error(f"获取好友列表失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/groups', methods=['GET'])
    def get_groups():
        """
        获取群聊列表
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            groups = app_instance.get_groups()
            return jsonify({
                "success": True,
                "data": groups,
                "count": len(groups)
            })
            
        except Exception as e:
            app.logger.error(f"获取群聊列表失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/send-message', methods=['POST'])
    def send_message():
        """
        发送消息
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            data = request.get_json()
            if not data:
                return jsonify({
                    "success": False,
                    "error": "请求数据为空"
                }), 400
            
            target = data.get('target')
            message = data.get('message')
            target_type = data.get('type', 'friend')  # 默认为好友
            
            if not target or not message:
                return jsonify({
                    "success": False,
                    "error": "缺少目标或消息内容"
                }), 400
            
            success = app_instance.send_message(target, message, target_type)
            
            if success:
                return jsonify({
                    "success": True,
                    "message": f"消息已发送到 {target}"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "发送消息失败"
                }), 500
                
        except Exception as e:
            app.logger.error(f"发送消息失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/news/groups', methods=['GET'])
    def get_news_groups():
        """
        获取新闻推送群组列表
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            config = app_instance.get_config()
            news_groups = config.get('news', {}).get('target_groups', [])
            
            return jsonify({
                "success": True,
                "data": news_groups,
                "count": len(news_groups)
            })
            
        except Exception as e:
            app.logger.error(f"获取新闻群组失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/news/groups', methods=['POST'])
    def add_news_group():
        """
        添加新闻推送群组
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            data = request.get_json()
            if not data:
                return jsonify({
                    "success": False,
                    "error": "请求数据为空"
                }), 400
            
            group_name = data.get('group')
            if not group_name:
                return jsonify({
                    "success": False,
                    "error": "缺少群组名称"
                }), 400
            
            success = app_instance.add_news_group(group_name)
            
            if success:
                return jsonify({
                    "success": True,
                    "message": f"已添加新闻推送群组: {group_name}"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "添加新闻推送群组失败"
                }), 500
                
        except Exception as e:
            app.logger.error(f"添加新闻群组失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/news/groups', methods=['DELETE'])
    def remove_news_group():
        """
        移除新闻推送群组
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            data = request.get_json()
            if not data:
                return jsonify({
                    "success": False,
                    "error": "请求数据为空"
                }), 400
            
            group_name = data.get('group')
            if not group_name:
                return jsonify({
                    "success": False,
                    "error": "缺少群组名称"
                }), 400
            
            success = app_instance.remove_news_group(group_name)
            
            if success:
                return jsonify({
                    "success": True,
                    "message": f"已移除新闻推送群组: {group_name}"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "移除新闻推送群组失败"
                }), 500
                
        except Exception as e:
            app.logger.error(f"移除新闻群组失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/news/time', methods=['POST'])
    def set_news_time():
        """
        设置新闻推送时间
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            data = request.get_json()
            if not data:
                return jsonify({
                    "success": False,
                    "error": "请求数据为空"
                }), 400
            
            push_time = data.get('time')
            if not push_time:
                return jsonify({
                    "success": False,
                    "error": "缺少推送时间"
                }), 400
            
            success = app_instance.set_news_push_time(push_time)
            
            if success:
                return jsonify({
                    "success": True,
                    "message": f"已设置新闻推送时间: {push_time}"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "设置新闻推送时间失败"
                }), 500
                
        except Exception as e:
            app.logger.error(f"设置新闻推送时间失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/api/news/test', methods=['GET'])
    def test_news():
        """
        测试新闻获取
        """
        try:
            if not app_instance:
                return jsonify({
                    "success": False,
                    "error": "微信后端应用未初始化"
                }), 500
            
            news = app_instance.test_news_fetch()
            
            return jsonify({
                "success": True,
                "data": news,
                "length": len(news)
            })
            
        except Exception as e:
            app.logger.error(f"测试新闻获取失败: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    # API文档路由
    @app.route('/api/docs', methods=['GET'])
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
    
    return app

def main():
    """
    主函数 - 启动API服务器
    """
    print("🚀 启动微信后端API服务器...")
    
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