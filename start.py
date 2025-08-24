#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信后端系统快速启动脚本

这个脚本提供了一个简单的菜单界面，方便用户选择不同的启动方式
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """
    检查依赖是否已安装
    """
    required_packages = [
        'flask',
        'flask_cors',
        'requests',
        'pywinauto',
        'pyautogui'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖已安装")
    return True

def check_pywechat():
    """
    检查pywechat是否可用
    """
    try:
        from utils import pywechat
        print("✅ pywechat 已安装")
        return True
    except ImportError:
        print("❌ pywechat 未安装")
        print("请检查utils/pywechat目录是否存在")
        return False

def start_cli_service():
    """
    启动命令行服务
    """
    print("🚀 启动命令行服务...")
    try:
        from .cli import main
        main()
    except ImportError:
        # 如果直接运行脚本，使用subprocess
        subprocess.run([sys.executable, "-m", "wechat_backend.cli", "start"])

def start_api_service():
    """
    启动API服务
    """
    print("🌐 启动API服务...")
    print("API服务将在 http://127.0.0.1:5000 启动")
    print("按 Ctrl+C 停止服务")
    
    try:
        from .api import main
        main()
    except ImportError:
        subprocess.run([sys.executable, "-m", "wechat_backend.api"])

def start_both_services():
    """
    同时启动命令行和API服务
    """
    print("🔥 同时启动命令行和API服务...")
    
    import threading
    import time
    
    # 在新线程中启动API服务
    api_thread = threading.Thread(target=start_api_service, daemon=True)
    api_thread.start()
    
    # 等待API服务启动
    time.sleep(2)
    
    # 启动命令行服务
    start_cli_service()

def show_configuration_guide():
    """
    显示配置指南
    """
    print("⚙️ 配置指南")
    print("=" * 50)
    
    print("\n1. 基础配置:")
    print("   python -m wechat_backend.cli show-config")
    
    print("\n2. 设置微信路径（如果需要）:")
    print('   python -m wechat_backend.cli set-wechat-path "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"')
    
    print("\n3. 添加新闻推送群:")
    print('   python -m wechat_backend.cli add-group "群名称"')
    
    print("\n4. 设置新闻推送时间:")
    print('   python -m wechat_backend.cli set-time "09:00"')
    
    print("\n5. 测试新闻获取:")
    print("   python -m wechat_backend.cli test-news")
    
    print("\n6. 发送测试消息:")
    print('   python -m wechat_backend.cli send-test "好友名称" "测试消息"')
    
    print("\n更多命令请查看:")
    print("   python -m wechat_backend.cli --help")

def show_api_guide():
    """
    显示API使用指南
    """
    print("🌐 API使用指南")
    print("=" * 50)
    
    print("\n启动API服务:")
    print("   python -m wechat_backend.api")
    
    print("\n主要API接口:")
    print("   GET  /api/status              - 获取服务状态")
    print("   POST /api/wechat/start        - 启动微信服务")
    print("   POST /api/wechat/stop         - 停止微信服务")
    print("   POST /api/message/send        - 发送消息")
    print("   GET  /api/news/groups         - 获取新闻推送群")
    print("   POST /api/news/groups         - 添加新闻推送群")
    print("   PUT  /api/news/time           - 设置推送时间")
    print("   GET  /api/news/test           - 测试新闻获取")
    
    print("\n示例API调用:")
    print("   curl http://127.0.0.1:5000/api/status")
    print('   curl -X POST http://127.0.0.1:5000/api/news/groups -H "Content-Type: application/json" -d \'{"group_name":"测试群"}\'")

def run_example():
    """
    运行示例代码
    """
    print("📚 运行示例代码...")
    try:
        from . import example
        example.main()
    except ImportError:
        subprocess.run([sys.executable, "-m", "wechat_backend.example"])

def install_dependencies():
    """
    安装依赖
    """
    print("📦 安装依赖包...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if requirements_file.exists():
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], check=True)
            print("✅ 依赖安装完成")
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败")
    else:
        print("❌ 找不到 requirements.txt 文件")

def main():
    """
    主菜单
    """
    print("🤖 微信后端自动化系统")
    print("=" * 40)
    
    # 检查环境
    print("\n🔍 检查运行环境...")
    deps_ok = check_dependencies()
    pywechat_ok = check_pywechat()
    
    if not deps_ok or not pywechat_ok:
        print("\n❌ 环境检查失败，请先解决依赖问题")
        if not deps_ok:
            print("\n是否现在安装依赖? (y/n): ", end="")
            if input().lower() == 'y':
                install_dependencies()
        return
    
    print("\n✅ 环境检查通过")
    
    while True:
        print("\n" + "=" * 40)
        print("请选择操作:")
        print("1. 启动命令行服务")
        print("2. 启动API服务")
        print("3. 同时启动两个服务")
        print("4. 配置指南")
        print("5. API使用指南")
        print("6. 运行示例代码")
        print("7. 安装/更新依赖")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-7): ").strip()
        
        try:
            if choice == "1":
                start_cli_service()
            elif choice == "2":
                start_api_service()
            elif choice == "3":
                start_both_services()
            elif choice == "4":
                show_configuration_guide()
            elif choice == "5":
                show_api_guide()
            elif choice == "6":
                run_example()
            elif choice == "7":
                install_dependencies()
            elif choice == "0":
                print("👋 再见！")
                break
            else:
                print("❌ 无效选择，请重新输入")
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出程序")
            break
        except Exception as e:
            print(f"\n❌ 执行出错: {e}")
            print("请检查错误信息并重试")

if __name__ == "__main__":
    main()