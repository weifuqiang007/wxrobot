#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信后端系统使用示例

这个文件展示了如何使用微信后端系统的各种功能
"""

import time
import threading
from wechat_backend.app import WechatBackendApp
from wechat_backend.config import ConfigManager
from wechat_backend.news_service import NewsService

def example_basic_usage():
    """
    基础使用示例
    """
    print("=== 基础使用示例 ===")
    
    # 创建应用实例
    app = WechatBackendApp()
    
    try:
        # 添加新闻推送群
        app.add_news_group("测试群")
        app.add_news_group("工作群")
        
        # 设置推送时间为当前时间后1分钟（用于测试）
        from datetime import datetime, timedelta
        test_time = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
        app.set_news_time(test_time)
        print(f"设置测试推送时间: {test_time}")
        
        # 启动服务（这会阻塞主线程）
        print("启动微信服务...")
        print("按 Ctrl+C 停止服务")
        app.start()
        
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        app.stop()
        print("服务已停止")

def example_config_management():
    """
    配置管理示例
    """
    print("=== 配置管理示例 ===")
    
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 更新微信配置
    config_manager.update_wechat_config(
        wechat_path="C:\\Program Files\\Tencent\\WeChat\\WeChat.exe",
        is_maximize=True
    )
    print("已更新微信配置")
    
    # 更新回复配置
    config_manager.update_reply_config(
        default_reply="您好！我已收到您的消息，稍后会回复您。",
        welcome_message_template="🎉 热烈欢迎 {name} 加入我们的大家庭！"
    )
    print("已更新回复配置")
    
    # 更新新闻配置
    config_manager.update_news_config(
        push_time="08:30",
        enabled=True
    )
    print("已更新新闻配置")
    
    # 添加新闻推送群
    config_manager.add_news_group("技术交流群")
    config_manager.add_news_group("产品讨论群")
    print("已添加新闻推送群")
    
    # 显示当前配置
    print("\n当前配置:")
    import json
    config = config_manager.get_all_config()
    print(json.dumps(config, ensure_ascii=False, indent=2))

def example_news_service():
    """
    新闻服务示例
    """
    print("=== 新闻服务示例 ===")
    
    # 创建新闻服务
    news_service = NewsService()
    
    # 获取每日新闻
    print("获取每日新闻...")
    news_list = news_service.get_daily_news(count=3)
    
    print(f"\n获取到 {len(news_list)} 条新闻:")
    for i, news in enumerate(news_list, 1):
        print(f"{i}. {news.title}")
        if news.content:
            print(f"   内容: {news.content[:50]}...")
        if news.source:
            print(f"   来源: {news.source}")
        print()
    
    # 格式化为微信消息
    print("格式化为微信消息:")
    print("-" * 50)
    formatted_news = news_service.format_news_for_wechat(news_list)
    print(formatted_news)
    print("-" * 50)
    
    # 获取综合每日消息
    print("\n获取综合每日消息:")
    print("-" * 50)
    comprehensive_message = news_service.create_comprehensive_daily_message()
    print(comprehensive_message)
    print("-" * 50)

def example_api_client():
    """
    API客户端示例
    """
    print("=== API客户端示例 ===")
    
    import requests
    import json
    
    base_url = "http://127.0.0.1:5000/api"
    
    try:
        # 检查API服务状态
        print("检查API服务状态...")
        response = requests.get(f"{base_url}/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"API服务状态: {status['data']['api_status']}")
        else:
            print("API服务未运行，请先启动API服务")
            return
            
        # 获取配置
        print("\n获取当前配置...")
        response = requests.get(f"{base_url}/config")
        if response.status_code == 200:
            config = response.json()
            print(json.dumps(config['data'], ensure_ascii=False, indent=2))
            
        # 添加新闻推送群
        print("\n添加新闻推送群...")
        data = {"group_name": "API测试群"}
        response = requests.post(
            f"{base_url}/news/groups",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            result = response.json()
            print(result['message'])
            
        # 测试新闻获取
        print("\n测试新闻获取...")
        response = requests.get(f"{base_url}/news/test")
        if response.status_code == 200:
            news_data = response.json()
            print("新闻内容预览:")
            print(news_data['data']['content'][:200] + "...")
            
    except requests.exceptions.ConnectionError:
        print("无法连接到API服务，请确保API服务已启动")
        print("启动命令: python -m wechat_backend.api")
    except Exception as e:
        print(f"API调用出错: {e}")

def example_custom_message_handler():
    """
    自定义消息处理示例
    """
    print("=== 自定义消息处理示例 ===")
    
    from wechat_backend.wechat_service import WechatService
    
    # 创建微信服务
    wechat_service = WechatService()
    
    # 保存原始的消息处理方法
    original_handle_message = wechat_service._handle_message
    
    def custom_message_handler(friend_name, friend_type, content, message_type):
        """
        自定义消息处理逻辑
        """
        print(f"收到消息 - 来自: {friend_name}, 类型: {friend_type}, 内容: {content}")
        
        # 根据消息内容进行不同的回复
        if "天气" in content:
            reply = "今天天气不错，适合出行！"
        elif "新闻" in content:
            reply = "最新新闻已为您准备，请稍候..."
        elif "帮助" in content or "help" in content.lower():
            reply = "我可以帮您查看天气、获取新闻等。发送'天气'或'新闻'试试看！"
        else:
            # 使用原始处理逻辑
            return original_handle_message(friend_name, friend_type, content, message_type)
            
        # 发送自定义回复
        try:
            wechat_service.send_message(friend_name, reply)
            print(f"已回复: {reply}")
        except Exception as e:
            print(f"发送回复失败: {e}")
    
    # 替换消息处理方法
    wechat_service._handle_message = custom_message_handler
    
    print("自定义消息处理器已设置")
    print("现在系统会根据消息内容进行智能回复")
    
    return wechat_service

def example_scheduled_tasks():
    """
    定时任务示例
    """
    print("=== 定时任务示例 ===")
    
    import schedule
    
    def send_morning_greeting():
        """发送早安问候"""
        app = WechatBackendApp()
        app.initialize_services()
        
        greeting = "🌅 早上好！新的一天开始了，祝大家工作顺利！"
        
        # 向所有新闻推送群发送问候
        config_manager = ConfigManager()
        for group in config_manager.news_config.target_groups:
            try:
                app.send_message(group, greeting)
                print(f"已向 {group} 发送早安问候")
            except Exception as e:
                print(f"向 {group} 发送问候失败: {e}")
    
    def send_evening_summary():
        """发送晚间总结"""
        app = WechatBackendApp()
        app.initialize_services()
        
        summary = "🌙 晚上好！今天辛苦了，记得早点休息哦！"
        
        config_manager = ConfigManager()
        for group in config_manager.news_config.target_groups:
            try:
                app.send_message(group, summary)
                print(f"已向 {group} 发送晚间总结")
            except Exception as e:
                print(f"向 {group} 发送总结失败: {e}")
    
    # 注意：这里只是示例，实际使用时需要安装schedule库
    # pip install schedule
    
    print("定时任务配置示例:")
    print("- 每天 08:00 发送早安问候")
    print("- 每天 18:00 发送晚间总结")
    print("- 每天 09:00 发送新闻（由系统自动处理）")
    
    # schedule.every().day.at("08:00").do(send_morning_greeting)
    # schedule.every().day.at("18:00").do(send_evening_summary)
    
    print("\n要启用定时任务，请取消注释上面的schedule代码")

def main():
    """
    主函数 - 选择要运行的示例
    """
    examples = {
        "1": ("配置管理示例", example_config_management),
        "2": ("新闻服务示例", example_news_service),
        "3": ("API客户端示例", example_api_client),
        "4": ("自定义消息处理示例", example_custom_message_handler),
        "5": ("定时任务示例", example_scheduled_tasks),
        "6": ("基础使用示例（启动服务）", example_basic_usage),
    }
    
    print("微信后端系统使用示例")
    print("=" * 30)
    
    for key, (name, _) in examples.items():
        print(f"{key}. {name}")
    
    print("\n请选择要运行的示例 (1-6):")
    choice = input().strip()
    
    if choice in examples:
        name, func = examples[choice]
        print(f"\n运行示例: {name}")
        print("=" * 50)
        func()
    else:
        print("无效选择")

if __name__ == "__main__":
    main()