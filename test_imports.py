#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导入修复脚本

用于验证所有模块的导入是否正确
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """
    测试所有模块的导入
    """
    print("🧪 测试模块导入...")
    print("=" * 50)
    
    # 测试基础模块
    modules_to_test = [
        ('config', '配置管理模块'),
        ('news_service', '新闻服务模块'),
        ('wechat_service', '微信服务模块'),
        ('app', '主应用模块'),
        ('cli', '命令行工具'),
        ('api', 'Web API模块'),
        ('example', '示例模块')
    ]
    
    success_count = 0
    total_count = len(modules_to_test)
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description} ({module_name})")
            success_count += 1
        except ImportError as e:
            print(f"❌ {description} ({module_name}): {e}")
        except Exception as e:
            print(f"⚠️ {description} ({module_name}): {e}")
    
    print("\n" + "=" * 50)
    print(f"导入测试完成: {success_count}/{total_count} 成功")
    
    # 测试pywechat导入
    print("\n🔍 测试pywechat导入...")
    try:
        from utils import pywechat
        print("✅ pywechat导入成功")
        
        # 测试具体的类导入
        try:
            from utils.pywechat import WeChatAuto
            print("✅ WeChatAuto类导入成功")
        except ImportError as e:
            print(f"❌ WeChatAuto类导入失败: {e}")
            
    except ImportError as e:
        print(f"❌ pywechat导入失败: {e}")
    except Exception as e:
        print(f"⚠️ pywechat导入异常: {e}")
    
    return success_count == total_count

def test_service_creation():
    """
    测试服务创建
    """
    print("\n🏗️ 测试服务创建...")
    print("=" * 50)
    
    try:
        from config import ConfigManager
        config_manager = ConfigManager()
        print("✅ ConfigManager创建成功")
        
        try:
            from news_service import NewsService
            news_service = NewsService(config_manager.news_config)
            print("✅ NewsService创建成功")
        except Exception as e:
            print(f"❌ NewsService创建失败: {e}")
        
        try:
            from wechat_service import WechatService
            wechat_service = WechatService(config_manager)
            print("✅ WechatService创建成功")
        except Exception as e:
            print(f"❌ WechatService创建失败: {e}")
            
        try:
            from app import WechatBackendApp
            app = WechatBackendApp()
            print("✅ WechatBackendApp创建成功")
        except Exception as e:
            print(f"❌ WechatBackendApp创建失败: {e}")
            
    except Exception as e:
        print(f"❌ 基础配置创建失败: {e}")

def test_configuration():
    """
    测试配置功能
    """
    print("\n⚙️ 测试配置功能...")
    print("=" * 50)
    
    try:
        from config import ConfigManager
        
        # 创建临时配置文件
        test_config_file = "test_config_temp.json"
        config_manager = ConfigManager(test_config_file)
        
        # 测试配置修改
        config_manager.wechat_config.wechat_path = "test_path"
        config_manager.news_config.enabled = False
        config_manager.reply_config.default_reply = "测试回复"
        
        # 保存配置
        config_manager.save_config()
        print("✅ 配置保存成功")
        
        # 重新加载配置
        new_config_manager = ConfigManager(test_config_file)
        
        # 验证配置
        assert new_config_manager.wechat_config.wechat_path == "test_path"
        assert new_config_manager.news_config.enabled == False
        assert new_config_manager.reply_config.default_reply == "测试回复"
        
        print("✅ 配置加载和验证成功")
        
        # 清理测试文件
        import os
        if os.path.exists(test_config_file):
            os.remove(test_config_file)
            
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")

def main():
    """
    主测试函数
    """
    print("🤖 微信后端系统导入测试")
    print("=" * 60)
    
    # 运行所有测试
    import_success = test_imports()
    test_service_creation()
    test_configuration()
    
    print("\n" + "=" * 60)
    if import_success:
        print("🎉 所有导入测试通过，系统准备就绪！")
    else:
        print("⚠️ 部分导入测试失败，请检查错误信息")
    
    print("\n💡 提示:")
    print("- 如果pywechat导入失败，请确保utils/pywechat目录存在")
    print("- 如果其他模块导入失败，请检查相关依赖是否安装")
    print("- 运行 'python start.py' 开始使用系统")

if __name__ == "__main__":
    main()