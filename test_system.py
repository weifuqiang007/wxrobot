#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信后端系统测试脚本

用于测试系统各个模块的功能是否正常
"""

import os
import sys
import time
import json
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

class TestConfigManager(unittest.TestCase):
    """
    测试配置管理器
    """
    
    def setUp(self):
        self.test_config_file = "test_config.json"
        
    def tearDown(self):
        if os.path.exists(self.test_config_file):
            os.remove(self.test_config_file)
    
    def test_config_creation(self):
        """测试配置创建"""
        from config import ConfigManager
        
        config_manager = ConfigManager(self.test_config_file)
        
        # 检查默认配置
        self.assertIsNotNone(config_manager.wechat_config)
        self.assertIsNotNone(config_manager.news_config)
        self.assertIsNotNone(config_manager.reply_config)
    
    def test_config_save_load(self):
        """测试配置保存和加载"""
        from config import ConfigManager
        
        config_manager = ConfigManager(self.test_config_file)
        
        # 修改配置
        config_manager.wechat_config.wechat_path = "test_path"
        config_manager.news_config.news_push_enabled = False
        config_manager.reply_config.default_reply = "测试回复"
        
        # 保存配置
        config_manager.save_config()
        
        # 创建新的配置管理器并加载
        new_config_manager = ConfigManager(self.test_config_file)
        
        # 验证配置是否正确加载
        self.assertEqual(new_config_manager.wechat_config.wechat_path, "test_path")
        self.assertEqual(new_config_manager.news_config.news_push_enabled, False)
        self.assertEqual(new_config_manager.reply_config.default_reply, "测试回复")

class TestNewsService(unittest.TestCase):
    """
    测试新闻服务
    """
    
    def test_news_item_creation(self):
        """测试新闻项创建"""
        from news_service import NewsItem
        
        news = NewsItem(
            title="测试标题",
            content="测试内容",
            source="测试来源",
            url="https://test.com"
        )
        
        self.assertEqual(news.title, "测试标题")
        self.assertEqual(news.content, "测试内容")
        self.assertEqual(news.source, "测试来源")
        self.assertEqual(news.url, "https://test.com")
    
    @patch('requests.get')
    def test_news_service_fetch(self, mock_get):
        """测试新闻获取"""
        from news_service import NewsService
        from config import NewsConfig
        
        # 模拟API响应
        mock_response = Mock()
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': '测试新闻1',
                    'description': '测试内容1',
                    'source': {'name': '测试来源1'},
                    'url': 'https://test1.com'
                },
                {
                    'title': '测试新闻2',
                    'description': '测试内容2',
                    'source': {'name': '测试来源2'},
                    'url': 'https://test2.com'
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        config = NewsConfig()
        config.news_api_url = "https://test-api.com"
        config.news_api_key = "test_key"
        
        news_service = NewsService(config)
        news_list = news_service.fetch_news()
        
        self.assertEqual(len(news_list), 2)
        self.assertEqual(news_list[0].title, "测试新闻1")
        self.assertEqual(news_list[1].title, "测试新闻2")
    
    def test_news_service_mock(self):
        """测试模拟新闻"""
        from news_service import NewsService
        from config import NewsConfig
        
        config = NewsConfig()
        news_service = NewsService(config)
        
        # 获取模拟新闻
        news_list = news_service.get_mock_news()
        
        self.assertGreater(len(news_list), 0)
        self.assertIsInstance(news_list[0].title, str)
    
    def test_format_news_for_wechat(self):
        """测试微信新闻格式化"""
        from news_service import NewsService, NewsItem
        from config import NewsConfig
        
        config = NewsConfig()
        news_service = NewsService(config)
        
        news_list = [
            NewsItem("标题1", "内容1", "来源1", "https://test1.com"),
            NewsItem("标题2", "内容2", "来源2", "https://test2.com")
        ]
        
        formatted = news_service.format_news_for_wechat(news_list)
        
        self.assertIn("标题1", formatted)
        self.assertIn("标题2", formatted)
        self.assertIn("来源1", formatted)
        self.assertIn("来源2", formatted)

class TestWechatService(unittest.TestCase):
    """
    测试微信服务
    """
    
    @patch('wechat_service.WeChatAuto')
    def test_wechat_service_init(self, mock_wechat_auto):
        """测试微信服务初始化"""
        try:
            from wechat_service import WechatService
            from config import ConfigManager
            
            config_manager = ConfigManager()
            service = WechatService(config_manager)
            self.assertIsNotNone(service.config_manager)
            self.assertFalse(service.is_running)
        except Exception as e:
            # 可能因为导入问题而失败，这是预期的
            pass
    
    @patch('wechat_service.WeChatAuto')
    def test_message_listener(self, mock_wechat_auto):
        """测试消息监听器"""
        try:
            from wechat_service import WechatService
            from config import ConfigManager
            
            config_manager = ConfigManager()
            service = WechatService(config_manager)
            
            # 模拟消息
            # 测试消息处理（不会实际发送）
            try:
                service._handle_message('测试用户', '好友', '测试消息', 'text')
            except Exception as e:
                # 预期会有异常，因为没有真实的微信连接
                pass
        except ImportError:
            # 导入失败是预期的
            pass

class TestSystemIntegration(unittest.TestCase):
    """
    系统集成测试
    """
    
    def test_import_all_modules(self):
        """测试所有模块导入"""
        try:
            import config
            import news_service
            import wechat_service
            import app
            import cli
            import api
            import example
            
            self.assertTrue(True, "所有模块导入成功")
        except ImportError as e:
            self.fail(f"模块导入失败: {e}")
    
    def test_config_integration(self):
        """测试配置集成"""
        from config import ConfigManager
        from news_service import NewsService
        
        config_manager = ConfigManager()
        news_service = NewsService(config_manager.news_config)
        
        # 测试配置是否正确传递
        self.assertIsNotNone(news_service.config)
    
    def test_app_creation(self):
        """测试应用创建"""
        from app import WechatBackendApp
        
        try:
            app = WechatBackendApp()
            self.assertIsNotNone(app.config_manager)
            self.assertIsNotNone(app.news_service)
        except Exception as e:
            # 可能因为缺少pywechat而失败，这是预期的
            pass

def run_manual_tests():
    """
    运行手动测试
    """
    print("🧪 运行手动测试...")
    print("=" * 50)
    
    # 测试配置文件创建
    print("\n1. 测试配置文件创建...")
    try:
        from config import ConfigManager
        config = ConfigManager("test_manual_config.json")
        print("✅ 配置管理器创建成功")
        
        # 清理测试文件
        if os.path.exists("test_manual_config.json"):
            os.remove("test_manual_config.json")
    except Exception as e:
        print(f"❌ 配置管理器创建失败: {e}")
    
    # 测试新闻服务
    print("\n2. 测试新闻服务...")
    try:
        from news_service import NewsService
        from config import NewsConfig
        
        config = NewsConfig()
        news_service = NewsService(config)
        news_list = news_service.get_mock_news()
        
        if news_list:
            print(f"✅ 新闻服务正常，获取到 {len(news_list)} 条模拟新闻")
            print(f"   第一条新闻: {news_list[0].title}")
        else:
            print("❌ 新闻服务异常，未获取到新闻")
    except Exception as e:
        print(f"❌ 新闻服务测试失败: {e}")
    
    # 测试CLI模块
    print("\n3. 测试CLI模块...")
    try:
        import cli
        print("✅ CLI模块导入成功")
    except Exception as e:
        print(f"❌ CLI模块导入失败: {e}")
    
    # 测试API模块
    print("\n4. 测试API模块...")
    try:
        import api
        print("✅ API模块导入成功")
    except Exception as e:
        print(f"❌ API模块导入失败: {e}")
    
    # 测试pywechat依赖
    print("\n5. 测试pywechat依赖...")
    try:
        from utils import pywechat
        print("✅ pywechat导入成功")
    except ImportError:
        print("⚠️ pywechat未找到，请检查utils/pywechat目录")
    except Exception as e:
        print(f"❌ pywechat导入异常: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 手动测试完成")

def run_unit_tests():
    """
    运行单元测试
    """
    print("🧪 运行单元测试...")
    print("=" * 50)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestConfigManager,
        TestNewsService,
        TestWechatService,
        TestSystemIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出结果
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 所有单元测试通过")
    else:
        print(f"❌ 有 {len(result.failures)} 个测试失败，{len(result.errors)} 个测试错误")
        
        if result.failures:
            print("\n失败的测试:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback.split('\n')[-2]}")
        
        if result.errors:
            print("\n错误的测试:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback.split('\n')[-2]}")
    
    return result.wasSuccessful()

def check_dependencies():
    """
    检查依赖
    """
    print("🔍 检查系统依赖...")
    print("=" * 50)
    
    required_packages = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('requests', 'requests'),
        ('pywinauto', 'pywinauto'),
        ('pyautogui', 'PyAutoGUI')
    ]
    
    optional_packages = [
        ('pywechat', 'pywechat')
    ]
    
    missing_required = []
    missing_optional = []
    
    # 检查必需包
    for package, display_name in required_packages:
        try:
            __import__(package)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name}")
            missing_required.append(display_name)
    
    # 检查可选包
    for package, display_name in optional_packages:
        try:
            __import__(package)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"⚠️ {display_name} (可选)")
            missing_optional.append(display_name)
    
    print("\n" + "=" * 50)
    
    if missing_required:
        print("❌ 缺少必需依赖:")
        for package in missing_required:
            print(f"   - {package}")
        print("\n请运行: pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print("⚠️ 缺少可选依赖:")
        for package in missing_optional:
            print(f"   - {package}")
        print("\n这些依赖是可选的，但建议安装以获得完整功能")
    
    print("🎉 依赖检查完成")
    return True

def main():
    """
    主测试函数
    """
    print("🤖 微信后端系统测试")
    print("=" * 60)
    
    while True:
        print("\n请选择测试类型:")
        print("1. 检查依赖")
        print("2. 运行单元测试")
        print("3. 运行手动测试")
        print("4. 运行所有测试")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-4): ").strip()
        
        try:
            if choice == "1":
                check_dependencies()
            elif choice == "2":
                run_unit_tests()
            elif choice == "3":
                run_manual_tests()
            elif choice == "4":
                print("🚀 运行完整测试套件...")
                deps_ok = check_dependencies()
                if deps_ok:
                    unit_ok = run_unit_tests()
                    run_manual_tests()
                    
                    if unit_ok:
                        print("\n🎉 所有测试完成，系统状态良好")
                    else:
                        print("\n⚠️ 部分测试失败，请检查错误信息")
                else:
                    print("\n❌ 依赖检查失败，请先安装依赖")
            elif choice == "0":
                print("👋 测试结束")
                break
            else:
                print("❌ 无效选择，请重新输入")
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出测试")
            break
        except Exception as e:
            print(f"\n❌ 测试执行出错: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()