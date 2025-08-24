#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻管理控制器
"""

from services.app_service import AppService

class NewsController:
    """
    新闻管理控制器
    """
    
    def __init__(self):
        self.app_service = AppService()
    
    def get_news_groups(self):
        """
        获取新闻推送群组列表
        
        Returns:
            dict: 群组列表
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            config = app_instance.get_config()
            news_groups = config.get('news', {}).get('target_groups', [])
            
            return {
                "success": True,
                "data": news_groups,
                "count": len(news_groups)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def add_news_group(self, data):
        """
        添加新闻推送群组
        
        Args:
            data (dict): 群组数据
            
        Returns:
            dict: 添加结果
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            group_name = data.get('group')
            if not group_name:
                return {
                    "success": False,
                    "error": "缺少群组名称",
                    "status_code": 400
                }
            
            success = app_instance.add_news_group(group_name)
            
            if success:
                return {
                    "success": True,
                    "message": f"已添加新闻推送群组: {group_name}"
                }
            else:
                return {
                    "success": False,
                    "error": "添加新闻推送群组失败",
                    "status_code": 500
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def remove_news_group(self, data):
        """
        移除新闻推送群组
        
        Args:
            data (dict): 群组数据
            
        Returns:
            dict: 移除结果
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            group_name = data.get('group')
            if not group_name:
                return {
                    "success": False,
                    "error": "缺少群组名称",
                    "status_code": 400
                }
            
            success = app_instance.remove_news_group(group_name)
            
            if success:
                return {
                    "success": True,
                    "message": f"已移除新闻推送群组: {group_name}"
                }
            else:
                return {
                    "success": False,
                    "error": "移除新闻推送群组失败",
                    "status_code": 500
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def set_news_time(self, data):
        """
        设置新闻推送时间
        
        Args:
            data (dict): 时间数据
            
        Returns:
            dict: 设置结果
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            push_time = data.get('time')
            if not push_time:
                return {
                    "success": False,
                    "error": "缺少推送时间",
                    "status_code": 400
                }
            
            success = app_instance.set_news_push_time(push_time)
            
            if success:
                return {
                    "success": True,
                    "message": f"已设置新闻推送时间: {push_time}"
                }
            else:
                return {
                    "success": False,
                    "error": "设置新闻推送时间失败",
                    "status_code": 500
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def test_news(self):
        """
        测试新闻获取
        
        Returns:
            dict: 测试结果
        """
        try:
            app_instance = self.app_service.get_app_instance()
            
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            news = app_instance.test_news_fetch()
            
            return {
                "success": True,
                "data": news,
                "length": len(news)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }