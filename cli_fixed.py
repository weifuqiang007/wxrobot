#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信后端命令行接口（修复版本）
使用简化的WechatService避免pywechat语法错误
"""

import argparse
import sys
import json
from datetime import datetime

from config import ConfigManager
from app_fixed import WechatBackendApp

def create_parser():
    """
    创建命令行参数解析器
    
    Returns:
        argparse.ArgumentParser: 参数解析器
    """
    parser = argparse.ArgumentParser(
        description="微信后端自动化系统命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s start                    # 启动微信后端服务
  %(prog)s status                   # 查看服务状态
  %(prog)s send-message "好友名" "消息内容"  # 发送消息给好友
  %(prog)s send-group "群名" "消息内容"      # 发送消息到群聊
  %(prog)s list-friends             # 列出所有好友
  %(prog)s list-groups              # 列出所有群聊
  %(prog)s add-news-group "群名"     # 添加新闻推送群组
  %(prog)s remove-news-group "群名"  # 移除新闻推送群组
  %(prog)s set-news-time "09:00"     # 设置新闻推送时间
  %(prog)s test-news                # 测试新闻获取
  %(prog)s config                   # 查看当前配置
        """
    )
    
    # 添加子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # start 命令
    start_parser = subparsers.add_parser('start', help='启动微信后端服务')
    start_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    # status 命令
    status_parser = subparsers.add_parser('status', help='查看服务状态')
    status_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    # send-message 命令
    send_msg_parser = subparsers.add_parser('send-message', help='发送消息给好友')
    send_msg_parser.add_argument('friend', help='好友名称')
    send_msg_parser.add_argument('message', help='消息内容')
    send_msg_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    # send-group 命令
    send_group_parser = subparsers.add_parser('send-group', help='发送消息到群聊')
    send_group_parser.add_argument('group', help='群聊名称')
    send_group_parser.add_argument('message', help='消息内容')
    send_group_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    # list-friends 命令
    list_friends_parser = subparsers.add_parser('list-friends', help='列出所有好友')
    list_friends_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    # list-groups 命令
    list_groups_parser = subparsers.add_parser('list-groups', help='列出所有群聊')
    list_groups_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    # add-news-group 命令
    add_news_parser = subparsers.add_parser('add-news-group', help='添加新闻推送群组')
    add_news_parser.add_argument('group', help='群聊名称')
    add_news_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    # remove-news-group 命令
    remove_news_parser = subparsers.add_parser('remove-news-group', help='移除新闻推送群组')
    remove_news_parser.add_argument('group', help='群聊名称')
    remove_news_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    # set-news-time 命令
    set_time_parser = subparsers.add_parser('set-news-time', help='设置新闻推送时间')
    set_time_parser.add_argument('time', help='推送时间（HH:MM格式）')
    set_time_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    # test-news 命令
    test_news_parser = subparsers.add_parser('test-news', help='测试新闻获取')
    test_news_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    # config 命令
    config_parser = subparsers.add_parser('config', help='查看当前配置')
    config_parser.add_argument('--config', '-c', default='config.json', help='配置文件路径')
    
    return parser

def handle_start(args):
    """
    处理 start 命令
    
    Args:
        args: 命令行参数
    """
    print("🚀 启动微信后端服务...")
    
    try:
        app = WechatBackendApp(args.config)
        app.start()
    except KeyboardInterrupt:
        print("\n👋 用户中断，服务停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1
    
    return 0

def handle_status(args):
    """
    处理 status 命令
    
    Args:
        args: 命令行参数
    """
    try:
        app = WechatBackendApp(args.config)
        status = app.get_status()
        
        print("📊 服务状态:")
        print(f"  运行状态: {'🟢 运行中' if status['running'] else '🔴 已停止'}")
        print(f"  微信服务: {'🟢 正常' if status['wechat_service'] else '🔴 异常'}")
        print(f"  检查时间: {status['timestamp']}")
        print(f"  版本信息: {status['version']}")
        
    except Exception as e:
        print(f"❌ 获取状态失败: {e}")
        return 1
    
    return 0

def handle_send_message(args):
    """
    处理 send-message 命令
    
    Args:
        args: 命令行参数
    """
    try:
        app = WechatBackendApp(args.config)
        success = app.send_message(args.friend, args.message, "friend")
        
        if success:
            print(f"✅ 消息已发送给 {args.friend}")
        else:
            print(f"❌ 发送消息失败")
            return 1
            
    except Exception as e:
        print(f"❌ 发送消息失败: {e}")
        return 1
    
    return 0

def handle_send_group(args):
    """
    处理 send-group 命令
    
    Args:
        args: 命令行参数
    """
    try:
        app = WechatBackendApp(args.config)
        success = app.send_message(args.group, args.message, "group")
        
        if success:
            print(f"✅ 消息已发送到群聊 {args.group}")
        else:
            print(f"❌ 发送消息失败")
            return 1
            
    except Exception as e:
        print(f"❌ 发送消息失败: {e}")
        return 1
    
    return 0

def handle_list_friends(args):
    """
    处理 list-friends 命令
    
    Args:
        args: 命令行参数
    """
    try:
        app = WechatBackendApp(args.config)
        friends = app.get_friends()
        
        print(f"👥 好友列表 (共 {len(friends)} 个):")
        for i, friend in enumerate(friends, 1):
            print(f"  {i:2d}. {friend}")
            
    except Exception as e:
        print(f"❌ 获取好友列表失败: {e}")
        return 1
    
    return 0

def handle_list_groups(args):
    """
    处理 list-groups 命令
    
    Args:
        args: 命令行参数
    """
    try:
        app = WechatBackendApp(args.config)
        groups = app.get_groups()
        
        print(f"👥 群聊列表 (共 {len(groups)} 个):")
        for i, group in enumerate(groups, 1):
            print(f"  {i:2d}. {group}")
            
    except Exception as e:
        print(f"❌ 获取群聊列表失败: {e}")
        return 1
    
    return 0

def handle_add_news_group(args):
    """
    处理 add-news-group 命令
    
    Args:
        args: 命令行参数
    """
    try:
        app = WechatBackendApp(args.config)
        success = app.add_news_group(args.group)
        
        if success:
            print(f"✅ 已添加新闻推送群组: {args.group}")
        else:
            print(f"❌ 添加新闻推送群组失败")
            return 1
            
    except Exception as e:
        print(f"❌ 添加新闻推送群组失败: {e}")
        return 1
    
    return 0

def handle_remove_news_group(args):
    """
    处理 remove-news-group 命令
    
    Args:
        args: 命令行参数
    """
    try:
        app = WechatBackendApp(args.config)
        success = app.remove_news_group(args.group)
        
        if success:
            print(f"✅ 已移除新闻推送群组: {args.group}")
        else:
            print(f"❌ 移除新闻推送群组失败")
            return 1
            
    except Exception as e:
        print(f"❌ 移除新闻推送群组失败: {e}")
        return 1
    
    return 0

def handle_set_news_time(args):
    """
    处理 set-news-time 命令
    
    Args:
        args: 命令行参数
    """
    try:
        app = WechatBackendApp(args.config)
        success = app.set_news_push_time(args.time)
        
        if success:
            print(f"✅ 已设置新闻推送时间: {args.time}")
        else:
            print(f"❌ 设置新闻推送时间失败")
            return 1
            
    except Exception as e:
        print(f"❌ 设置新闻推送时间失败: {e}")
        return 1
    
    return 0

def handle_test_news(args):
    """
    处理 test-news 命令
    
    Args:
        args: 命令行参数
    """
    try:
        app = WechatBackendApp(args.config)
        news = app.test_news_fetch()
        
        print("📰 新闻获取测试结果:")
        print("-" * 50)
        print(news)
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ 新闻获取测试失败: {e}")
        return 1
    
    return 0

def handle_config(args):
    """
    处理 config 命令
    
    Args:
        args: 命令行参数
    """
    try:
        app = WechatBackendApp(args.config)
        config = app.get_config()
        
        print("⚙️  当前配置:")
        print(json.dumps(config, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ 获取配置失败: {e}")
        return 1
    
    return 0

def main():
    """
    主函数
    
    Returns:
        int: 退出码
    """
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # 显示标题
    print("🤖 微信后端自动化系统 CLI v1.0.0")
    print("=" * 50)
    
    # 根据命令调用相应的处理函数
    handlers = {
        'start': handle_start,
        'status': handle_status,
        'send-message': handle_send_message,
        'send-group': handle_send_group,
        'list-friends': handle_list_friends,
        'list-groups': handle_list_groups,
        'add-news-group': handle_add_news_group,
        'remove-news-group': handle_remove_news_group,
        'set-news-time': handle_set_news_time,
        'test-news': handle_test_news,
        'config': handle_config,
    }
    
    handler = handlers.get(args.command)
    if handler:
        try:
            return handler(args)
        except KeyboardInterrupt:
            print("\n👋 用户中断")
            return 1
        except Exception as e:
            print(f"❌ 执行命令失败: {e}")
            import traceback
            traceback.print_exc()
            return 1
    else:
        print(f"❌ 未知命令: {args.command}")
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())