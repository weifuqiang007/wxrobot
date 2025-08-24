#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信数据访问对象
负责与微信服务的数据交互
"""

from typing import List, Dict, Any, Optional
import logging
from wechat_service_simple import WechatService
from dao.config_dao import ConfigDAO

class WechatDAO:
    """
    微信数据访问对象
    """
    
    def __init__(self, config_dao: ConfigDAO = None):
        """
        初始化微信DAO
        
        Args:
            config_dao (ConfigDAO): 配置数据访问对象
        """
        self.config_dao = config_dao or ConfigDAO()
        self.logger = logging.getLogger(__name__)
        self._wechat_service = None
    
    @property
    def wechat_service(self) -> Optional[WechatService]:
        """
        获取微信服务实例
        
        Returns:
            Optional[WechatService]: 微信服务实例
        """
        if self._wechat_service is None:
            try:
                # 这里需要传入配置管理器，但为了简化，我们直接创建
                from config import ConfigManager
                config_manager = ConfigManager()
                self._wechat_service = WechatService(config_manager)
                self.logger.info("微信服务实例创建成功")
            except Exception as e:
                self.logger.error(f"创建微信服务实例失败: {e}")
                self._wechat_service = None
        
        return self._wechat_service
    
    def get_friends_list(self) -> List[str]:
        """
        获取好友列表
        
        Returns:
            List[str]: 好友名称列表
        """
        try:
            if self.wechat_service:
                return self.wechat_service.get_friend_list()
            else:
                self.logger.warning("微信服务未初始化，返回空好友列表")
                return []
        except Exception as e:
            self.logger.error(f"获取好友列表失败: {e}")
            return []
    
    def get_groups_list(self) -> List[str]:
        """
        获取群聊列表
        
        Returns:
            List[str]: 群聊名称列表
        """
        try:
            if self.wechat_service:
                return self.wechat_service.get_group_list()
            else:
                self.logger.warning("微信服务未初始化，返回空群聊列表")
                return []
        except Exception as e:
            self.logger.error(f"获取群聊列表失败: {e}")
            return []
    
    def send_message_to_friend(self, friend_name: str, message: str) -> bool:
        """
        发送消息给好友
        
        Args:
            friend_name (str): 好友名称
            message (str): 消息内容
            
        Returns:
            bool: 发送是否成功
        """
        try:
            if self.wechat_service:
                return self.wechat_service.send_message_to_friend(friend_name, message)
            else:
                self.logger.error("微信服务未初始化，无法发送消息")
                return False
        except Exception as e:
            self.logger.error(f"发送消息给好友失败: {e}")
            return False
    
    def send_message_to_group(self, group_name: str, message: str) -> bool:
        """
        发送消息到群聊
        
        Args:
            group_name (str): 群聊名称
            message (str): 消息内容
            
        Returns:
            bool: 发送是否成功
        """
        try:
            if self.wechat_service:
                return self.wechat_service.send_message_to_group(group_name, message)
            else:
                self.logger.error("微信服务未初始化，无法发送消息")
                return False
        except Exception as e:
            self.logger.error(f"发送消息到群聊失败: {e}")
            return False
    
    def get_wechat_status(self) -> Dict[str, Any]:
        """
        获取微信状态
        
        Returns:
            Dict[str, Any]: 微信状态信息
        """
        try:
            if self.wechat_service:
                return {
                    "is_running": self.wechat_service.is_running,
                    "service_status": "active" if self.wechat_service.is_running else "inactive"
                }
            else:
                return {
                    "is_running": False,
                    "service_status": "not_initialized"
                }
        except Exception as e:
            self.logger.error(f"获取微信状态失败: {e}")
            return {
                "is_running": False,
                "service_status": "error",
                "error": str(e)
            }
    
    def start_wechat_service(self) -> bool:
        """
        启动微信服务
        
        Returns:
            bool: 启动是否成功
        """
        try:
            if self.wechat_service:
                self.wechat_service.start_service()
                self.logger.info("微信服务启动成功")
                return True
            else:
                self.logger.error("微信服务未初始化，无法启动")
                return False
        except Exception as e:
            self.logger.error(f"启动微信服务失败: {e}")
            return False
    
    def stop_wechat_service(self) -> bool:
        """
        停止微信服务
        
        Returns:
            bool: 停止是否成功
        """
        try:
            if self.wechat_service:
                self.wechat_service.stop_service()
                self.logger.info("微信服务停止成功")
                return True
            else:
                self.logger.warning("微信服务未初始化，无需停止")
                return True
        except Exception as e:
            self.logger.error(f"停止微信服务失败: {e}")
            return False
    
    def get_news_groups(self) -> List[str]:
        """
        获取新闻推送群组列表
        
        Returns:
            List[str]: 新闻推送群组列表
        """
        try:
            news_config = self.config_dao.get_config_section("news")
            if news_config:
                return news_config.get("target_groups", [])
            return []
        except Exception as e:
            self.logger.error(f"获取新闻推送群组失败: {e}")
            return []
    
    def add_news_group(self, group_name: str) -> bool:
        """
        添加新闻推送群组
        
        Args:
            group_name (str): 群组名称
            
        Returns:
            bool: 添加是否成功
        """
        try:
            news_groups = self.get_news_groups()
            if group_name not in news_groups:
                news_groups.append(group_name)
                return self.config_dao.update_config_section("news", {"target_groups": news_groups})
            else:
                self.logger.warning(f"群组 {group_name} 已存在于新闻推送列表中")
                return True
        except Exception as e:
            self.logger.error(f"添加新闻推送群组失败: {e}")
            return False
    
    def remove_news_group(self, group_name: str) -> bool:
        """
        移除新闻推送群组
        
        Args:
            group_name (str): 群组名称
            
        Returns:
            bool: 移除是否成功
        """
        try:
            news_groups = self.get_news_groups()
            if group_name in news_groups:
                news_groups.remove(group_name)
                return self.config_dao.update_config_section("news", {"target_groups": news_groups})
            else:
                self.logger.warning(f"群组 {group_name} 不在新闻推送列表中")
                return True
        except Exception as e:
            self.logger.error(f"移除新闻推送群组失败: {e}")
            return False