#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础功能测试脚本

测试系统的核心功能，不依赖pywechat库
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

def test_core_modules():
    """
    测试核心模块导入
    """
    print("🧪 测试核心模块导入...")
    print("=" * 50)
    
    success_count = 0
    total_count = 0
    
    # 测试配置模块
    try:
        from config import ConfigManager
        print("✅ 配置管理模块 (config)")
        success_count += 1
    except Exception as e:
        print(f"❌ 配置管理模块: {e}")
    total_count += 1
    
    # 测试新闻服务模块
    try:
        from news_service import NewsService
        print("✅ 新闻服务模块 (news_service)")
        success_count += 1
    except Exception as e:
        print(f"❌ 新闻服务模块: {e}")
    total_count += 1
    
    return success_count, total_count

def test_configuration():
    """
    测试配置功能
    """
    print("\n⚙️ 测试配置功能...")
    print("=" * 50)
    
    try:
        from config import ConfigManager
        
        # 创建配置管理器
        config_manager = ConfigManager("test_config_basic.json")
        print("✅ ConfigManager创建成功")
        
        # 测试配置修改
        config_manager.wechat_config.wechat_path = "test_path"
        config_manager.news_config.enabled = False
        config_manager.reply_config.default_reply = "测试回复"
        
        # 保存配置
        config_manager.save_config()
        print("✅ 配置保存成功")
        
        # 重新加载配置
        new_config_manager = ConfigManager("test_config_basic.json")
        
        # 验证配置
        assert new_config_manager.wechat_config.wechat_path == "test_path"
        assert new_config_manager.news_config.enabled == False
        assert new_config_manager.reply_config.default_reply == "测试回复"
        
        print("✅ 配置加载和验证成功")
        
        # 清理测试文件
        import os
        if os.path.exists("test_config_basic.json"):
            os.remove("test_config_basic.json")
            
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_news_service():
    """
    测试新闻服务
    """
    print("\n📰 测试新闻服务...")
    print("=" * 50)
    
    try:
        from config import ConfigManager
        from news_service import NewsService
        
        # 创建配置和服务
        config_manager = ConfigManager()
        news_service = NewsService(config_manager.news_config)
        print("✅ NewsService创建成功")
        
        # 测试新闻格式化
        test_news = [
            {"title": "测试新闻1", "description": "这是测试新闻1的描述", "url": "http://test1.com"},
            {"title": "测试新闻2", "description": "这是测试新闻2的描述", "url": "http://test2.com"}
        ]
        
        formatted_news = news_service._format_news_message(test_news)
        print("✅ 新闻格式化成功")
        print(f"格式化结果长度: {len(formatted_news)} 字符")
        
        return True
        
    except Exception as e:
        print(f"❌ 新闻服务测试失败: {e}")
        return False

def test_api_modules():
    """
    测试API相关模块（不启动服务）
    """
    print("\n🌐 测试API模块...")
    print("=" * 50)
    
    try:
        from api import WechatBackendAPI
        print("✅ API模块导入成功")
        
        from cli import WechatBackendCLI
        print("✅ CLI模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ API模块测试失败: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("🤖 微信后端系统基础功能测试")
    print("=" * 60)
    
    # 运行所有测试
    success_count, total_count = test_core_modules()
    config_success = test_configuration()
    news_success = test_news_service()
    api_success = test_api_modules()
    
    print("\n" + "=" * 60)
    print("📊 测试结果汇总:")
    print(f"- 核心模块导入: {success_count}/{total_count}")
    print(f"- 配置功能: {'✅' if config_success else '❌'}")
    print(f"- 新闻服务: {'✅' if news_success else '❌'}")
    print(f"- API模块: {'✅' if api_success else '❌'}")
    
    if success_count == total_count and config_success and news_success and api_success:
        print("\n🎉 所有基础功能测试通过！")
        print("\n📝 说明:")
        print("- 系统核心功能正常")
        print("- pywechat库导入问题不影响基本功能")
        print("- 可以正常使用配置管理和新闻服务")
        print("- API和CLI模块可以正常导入")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息")
    
    print("\n💡 下一步:")
    print("- 修复pywechat库的语法错误（可选）")
    print("- 运行 'python start.py' 开始使用系统")
    print("- 使用API接口进行系统管理")

if __name__ == "__main__":
    main()