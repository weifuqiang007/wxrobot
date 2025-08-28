#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信数据访问对象
负责与微信服务的数据交互
"""

import sys
import os
import time
from typing import List, Dict, Any, Optional
import logging
from services.wechat_service_simple import WechatService
from dao.config_dao import ConfigDAO

# 添加pywechat路径到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.pywechat.pywechat.interface import WechatAuto

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
        self._wechat_auto = None
    
    @property
    def wechat_auto(self) -> Optional[WechatAuto]:
        """
        获取微信自动化实例
        
        Returns:
            Optional[WechatAuto]: 微信自动化实例
        """
        if self._wechat_auto is None:
            try:
                self._wechat_auto = WechatAuto()
                self.logger.info("微信自动化实例创建成功")
            except Exception as e:
                self.logger.error(f"创建微信自动化实例失败: {e}")
                self._wechat_auto = None
        
        return self._wechat_auto
    
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
            
    
    def send_message_to_database(self, target: str, message: str, target_type: str = 'friend') -> bool:
        """
        将消息数据保存到数据库（纯数据访问操作）
        
        Args:
            target (str): 目标用户或群组
            message (str): 消息内容
            target_type (str): 目标类型
            
        Returns:
            bool: 保存是否成功
        """
        # TODO: 实现数据库保存逻辑
        # 例如: INSERT INTO messages (target, message, target_type, timestamp) VALUES (...)
        pass
        
    def get_message_history_from_database(self, target: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        从数据库获取消息历史（纯数据访问操作）
        
        Args:
            target (str): 目标用户或群组
            limit (int): 获取条数限制
            
        Returns:
            List[Dict[str, Any]]: 消息历史列表
        """
        # TODO: 实现数据库查询逻辑
        # 例如: SELECT * FROM messages WHERE target = ? ORDER BY timestamp DESC LIMIT ?
        pass
    
    def get_new_messages_from_database(self, last_check_time: float) -> List[Dict[str, Any]]:
        """
        从数据库获取新消息（纯数据访问操作）
        
        Args:
            last_check_time (float): 上次检查时间戳
            
        Returns:
            List[Dict[str, Any]]: 新消息列表
        """
        # TODO: 实现数据库查询逻辑
        # 例如: SELECT * FROM messages WHERE timestamp > ? AND message_type = 'received'
        pass
    
    def save_auto_reply_to_database(self, friend_name: str, message: str, original_message: str) -> bool:
        """
        保存自动回复记录到数据库（纯数据访问操作）
        
        Args:
            friend_name (str): 好友名称
            message (str): 回复消息
            original_message (str): 原始消息
            
        Returns:
            bool: 保存是否成功
        """
        # TODO: 实现数据库保存逻辑
        # 例如: INSERT INTO auto_replies (friend_name, reply_message, original_message, timestamp) VALUES (...)
        pass
    
    def save_message_record_to_database(self, target: str, message: str, target_type: str, message_type: str) -> bool:
        """
        保存消息记录到数据库（纯数据访问操作）
        
        Args:
            target (str): 目标用户或群组
            message (str): 消息内容
            target_type (str): 目标类型
            message_type (str): 消息类型（sent/received/auto_reply/welcome_sent）
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # TODO: 实现数据库保存逻辑
            # 例如: INSERT INTO message_records (target, message, target_type, message_type, timestamp) VALUES (...)
            self.logger.info(f"保存消息记录: {target} - {message_type} - {message[:50]}...")
            return True
        except Exception as e:
            self.logger.error(f"保存消息记录失败: {e}")
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
            self.logger.error(f"移除新闻群组失败: {e}")
            return False
    
    def save_welcome_record_to_database(self, group_name: str, member_name: str, welcome_message: str) -> bool:
        """
        保存新成员欢迎记录到数据库（纯数据访问操作）
        
        Args:
            group_name (str): 群聊名称
            member_name (str): 新成员名称
            welcome_message (str): 欢迎消息内容
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # TODO: 实现数据库保存逻辑
            # 例如: INSERT INTO welcome_records (group_name, member_name, welcome_message, timestamp) VALUES (...)
            self.logger.info(f"保存欢迎记录: {group_name} - {member_name} - {welcome_message[:50]}...")
            return True
        except Exception as e:
            self.logger.error(f"保存欢迎记录失败: {e}")
            return False
    
    def get_welcome_statistics_from_database(self, group_name: str = None, days: int = 7) -> Dict[str, Any]:
        """
        从数据库获取新成员欢迎统计信息（纯数据访问操作）
        
        Args:
            group_name (str): 群聊名称，None表示所有群聊
            days (int): 统计天数
            
        Returns:
            Dict[str, Any]: 统计信息
        """
        try:
            # TODO: 实现数据库查询逻辑
            # 例如: SELECT COUNT(*) FROM welcome_records WHERE timestamp >= DATE_SUB(NOW(), INTERVAL ? DAY)
            return {
                'total_welcomes': 0,
                'groups_count': 0,
                'recent_welcomes': []
            }
        except Exception as e:
            self.logger.error(f"获取欢迎统计失败: {e}")
            return {
                'total_welcomes': 0,
                'groups_count': 0,
                'recent_welcomes': []
            }
    
    def get_monitored_groups_from_database(self) -> List[str]:
        """
        从数据库获取当前监听的群组列表（纯数据访问操作）
        
        Returns:
            List[str]: 监听的群组列表
        """
        try:
            # TODO: 实现数据库查询逻辑
            # 例如: SELECT group_name FROM monitored_groups WHERE is_active = 1
            return []
        except Exception as e:
            self.logger.error(f"获取监听群组列表失败: {e}")
            return []
    
    def save_monitored_groups_to_database(self, groups: List[str]) -> bool:
        """
        保存监听的群组列表到数据库（纯数据访问操作）
        
        Args:
            groups (List[str]): 要监听的群组列表
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # TODO: 实现数据库保存逻辑
            # 例如: DELETE FROM monitored_groups; INSERT INTO monitored_groups (group_name, is_active) VALUES (...)
            self.logger.info(f"保存监听群组列表: {len(groups)} 个群组")
            return True
        except Exception as e:
            self.logger.error(f"保存监听群组列表失败: {e}")
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