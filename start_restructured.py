#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信后端自动化系统 - 重构版启动脚本

使用重构后的MVC架构启动Flask API服务
"""

import os
import sys
import json
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """配置日志系统"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('wechat_backend.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(__name__)

def check_dependencies():
    """检查必要的依赖包"""
    required_packages = [
        'flask',
        'flask_cors',
        'pywinauto',
        'pyautogui',
        'requests',
        'psutil'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包检查通过")
    return True

def check_config():
    """检查配置文件"""
    config_path = project_root / 'config.json'
    if not config_path.exists():
        print("❌ 配置文件 config.json 不存在")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查必要的配置项
        required_keys = ['wechat', 'news', 'auto_reply']
        for key in required_keys:
            if key not in config:
                print(f"❌ 配置文件缺少必要配置项: {key}")
                return False
        
        print("✅ 配置文件检查通过")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False

def check_wechat_service():
    """检查微信服务可用性"""
    try:
        from wechat_service_simple import WechatService
        service = WechatService()
        
        # 简单的可用性检查
        if hasattr(service, 'get_friends'):
            print("✅ 微信服务模块检查通过")
            return True
        else:
            print("⚠️  微信服务模块功能不完整")
            return False
    except ImportError as e:
        print(f"❌ 无法导入微信服务模块: {e}")
        return False
    except Exception as e:
        print(f"⚠️  微信服务检查异常: {e}")
        return True  # 允许继续运行

def start_api_server(host='127.0.0.1', port=5000, debug=False):
    """启动重构后的API服务器"""
    try:
        from api_restructured import create_app
        
        app = create_app()
        
        print(f"\n🚀 启动微信后端API服务器...")
        print(f"📍 服务地址: http://{host}:{port}")
        print(f"📖 API文档: http://{host}:{port}/api/docs")
        print(f"💓 健康检查: http://{host}:{port}/api/health")
        print("\n按 Ctrl+C 停止服务器\n")
        
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=False  # 避免重复启动
        )
        
    except ImportError as e:
        print(f"❌ 无法导入重构后的API模块: {e}")
        print("请确保 api_restructured.py 文件存在且正确")
        return False
    except Exception as e:
        print(f"❌ 启动API服务器失败: {e}")
        return False
    
    return True

def show_menu():
    """显示主菜单"""
    print("\n" + "="*60)
    print("🤖 微信后端自动化系统 - 重构版")
    print("="*60)
    print("1. 🚀 启动API服务器 (生产模式)")
    print("2. 🔧 启动API服务器 (调试模式)")
    print("3. 🔍 系统检查")
    print("4. 📖 查看API文档")
    print("5. ⚙️  查看配置")
    print("6. 📊 查看架构文档")
    print("0. 🚪 退出")
    print("="*60)

def show_system_check():
    """显示系统检查结果"""
    print("\n🔍 系统检查中...\n")
    
    checks = [
        ("依赖包检查", check_dependencies),
        ("配置文件检查", check_config),
        ("微信服务检查", check_wechat_service)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"📋 {name}:")
        result = check_func()
        if not result:
            all_passed = False
        print()
    
    if all_passed:
        print("✅ 所有检查通过，系统可以正常运行")
    else:
        print("❌ 部分检查未通过，请修复后重试")
    
    return all_passed

def show_api_docs():
    """显示API文档信息"""
    print("\n📖 API文档")
    print("="*50)
    print("启动服务器后，可通过以下地址访问:")
    print("• 在线文档: http://127.0.0.1:5000/api/docs")
    print("• 健康检查: http://127.0.0.1:5000/api/health")
    print("• 服务状态: http://127.0.0.1:5000/api/status")
    print("\n主要API端点:")
    print("• GET  /api/health     - 健康检查")
    print("• GET  /api/status     - 服务状态")
    print("• GET  /api/config     - 获取配置")
    print("• POST /api/config     - 更新配置")
    print("• POST /api/send-message - 发送消息")
    print("• GET  /api/friends    - 获取好友列表")
    print("• GET  /api/groups     - 获取群聊列表")
    print("• GET  /api/news/groups - 获取新闻推送群组")
    print("• POST /api/news/groups - 添加新闻推送群组")

def show_config():
    """显示当前配置"""
    config_path = project_root / 'config.json'
    if not config_path.exists():
        print("❌ 配置文件不存在")
        return
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("\n⚙️  当前配置")
        print("="*50)
        print(json.dumps(config, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ 读取配置失败: {e}")

def show_architecture():
    """显示架构文档"""
    arch_path = project_root / 'ARCHITECTURE.md'
    if not arch_path.exists():
        print("❌ 架构文档不存在")
        return
    
    try:
        with open(arch_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n📊 架构文档")
        print("="*50)
        # 只显示前几行，避免输出过长
        lines = content.split('\n')[:30]
        for line in lines:
            print(line)
        
        if len(content.split('\n')) > 30:
            print("\n... (更多内容请查看 ARCHITECTURE.md 文件)")
    except Exception as e:
        print(f"❌ 读取架构文档失败: {e}")

def main():
    """主函数"""
    logger = setup_logging()
    
    while True:
        show_menu()
        
        try:
            choice = input("\n请选择操作 (0-6): ").strip()
            
            if choice == '0':
                print("\n👋 再见！")
                break
            elif choice == '1':
                if show_system_check():
                    start_api_server(debug=False)
                else:
                    input("\n按回车键继续...")
            elif choice == '2':
                if show_system_check():
                    start_api_server(debug=True)
                else:
                    input("\n按回车键继续...")
            elif choice == '3':
                show_system_check()
                input("\n按回车键继续...")
            elif choice == '4':
                show_api_docs()
                input("\n按回车键继续...")
            elif choice == '5':
                show_config()
                input("\n按回车键继续...")
            elif choice == '6':
                show_architecture()
                input("\n按回车键继续...")
            else:
                print("❌ 无效选择，请重试")
                
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            logger.error(f"程序异常: {e}")
            print(f"❌ 程序异常: {e}")
            input("\n按回车键继续...")

if __name__ == '__main__':
    main()