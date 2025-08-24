#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复版本的微信后端应用
"""

import sys
import traceback
from datetime import datetime

def test_basic_imports():
    """测试基础模块导入"""
    print("\n=== 测试基础模块导入 ===")
    
    try:
        # 测试配置模块
        from config import ConfigManager
        print("✅ config 模块导入成功")
        
        # 测试新闻服务
        from news_service import NewsService
        print("✅ news_service 模块导入成功")
        
        # 测试简化的微信服务
        from wechat_service_simple import WechatService
        print("✅ wechat_service_simple 模块导入成功")
        
        # 测试修复版本的应用
        from app_fixed import WechatBackendApp
        print("✅ app_fixed 模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 基础模块导入失败: {e}")
        traceback.print_exc()
        return False

def test_config_manager():
    """测试配置管理器"""
    print("\n=== 测试配置管理器 ===")
    
    try:
        from config import ConfigManager
        
        # 创建配置管理器
        config_manager = ConfigManager("test_config.json")
        print("✅ ConfigManager 创建成功")
        
        # 测试保存配置
        config_manager.save_config()
        print("✅ 配置保存成功")
        
        # 测试加载配置
        config_manager.load_config()
        print("✅ 配置加载成功")
        
        # 测试获取配置
        all_config = config_manager.get_all_config()
        print(f"✅ 获取所有配置成功: {len(all_config)} 个配置项")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置管理器测试失败: {e}")
        traceback.print_exc()
        return False

def test_news_service():
    """测试新闻服务"""
    print("\n=== 测试新闻服务 ===")
    
    try:
        from config import ConfigManager
        from news_service import NewsService
        
        # 创建配置管理器
        config_manager = ConfigManager("test_config.json")
        
        # 创建新闻服务
        news_service = NewsService(config_manager.news_config)
        print("✅ NewsService 创建成功")
        
        # 测试新闻格式化（不实际获取新闻）
        test_news = [
            {"title": "测试新闻1", "description": "这是一条测试新闻", "url": "http://example.com/1"},
            {"title": "测试新闻2", "description": "这是另一条测试新闻", "url": "http://example.com/2"}
        ]
        
        formatted_news = news_service._format_news(test_news)
        print(f"✅ 新闻格式化成功: {len(formatted_news)} 字符")
        
        return True
        
    except Exception as e:
        print(f"❌ 新闻服务测试失败: {e}")
        traceback.print_exc()
        return False

def test_wechat_service():
    """测试简化的微信服务"""
    print("\n=== 测试简化的微信服务 ===")
    
    try:
        from config import ConfigManager
        from wechat_service_simple import WechatService
        
        # 创建配置管理器
        config_manager = ConfigManager("test_config.json")
        
        # 创建微信服务
        wechat_service = WechatService(config_manager)
        print("✅ WechatService 创建成功")
        
        # 测试启动服务（模拟）
        wechat_service.start_service()
        print("✅ 微信服务启动成功（模拟）")
        
        # 测试获取好友列表（模拟）
        friends = wechat_service.get_friend_list()
        print(f"✅ 获取好友列表成功: {len(friends)} 个好友")
        
        # 测试获取群聊列表（模拟）
        groups = wechat_service.get_group_list()
        print(f"✅ 获取群聊列表成功: {len(groups)} 个群聊")
        
        # 测试发送消息（模拟）
        result = wechat_service.send_message_to_friend("测试好友", "测试消息")
        print(f"✅ 发送消息测试成功: {result}")
        
        # 测试停止服务
        wechat_service.stop_service()
        print("✅ 微信服务停止成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 微信服务测试失败: {e}")
        traceback.print_exc()
        return False

def test_app_creation():
    """测试应用创建"""
    print("\n=== 测试应用创建 ===")
    
    try:
        from app_fixed import WechatBackendApp
        
        # 创建应用
        app = WechatBackendApp("test_config.json")
        print("✅ WechatBackendApp 创建成功")
        
        # 测试获取状态
        status = app.get_status()
        print(f"✅ 获取应用状态成功: {status}")
        
        # 测试获取配置
        config = app.get_config()
        print(f"✅ 获取应用配置成功: {len(config)} 个配置项")
        
        # 测试新闻获取
        news = app.test_news_fetch()
        print(f"✅ 测试新闻获取成功: {len(news)} 字符")
        
        return True
        
    except Exception as e:
        print(f"❌ 应用创建测试失败: {e}")
        traceback.print_exc()
        return False

def test_api_imports():
    """测试API相关模块导入"""
    print("\n=== 测试API相关模块导入 ===")
    
    try:
        # 测试CLI模块
        from cli import main as cli_main
        print("✅ cli 模块导入成功")
        
        # 测试API模块
        from api import create_app
        print("✅ api 模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ API模块导入失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🧪 微信后端应用修复版本测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行所有测试
    tests = [
        ("基础模块导入", test_basic_imports),
        ("配置管理器", test_config_manager),
        ("新闻服务", test_news_service),
        ("微信服务", test_wechat_service),
        ("应用创建", test_app_creation),
        ("API模块导入", test_api_imports),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！修复版本工作正常")
        return True
    else:
        print(f"⚠️  有 {total - passed} 个测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)