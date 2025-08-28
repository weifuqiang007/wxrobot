#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信API服务层
专门处理与微信API的直接交互
"""

import sys
import os
import logging
from typing import List, Dict, Any, Optional

# 添加pywechat路径到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.pywechat.pywechat.interface import WechatAuto

class WechatAPIService:
    """
    微信API服务类
    负责处理所有与微信API的直接交互
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
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
                self.logger.info("微信自动化实例初始化成功")
            except Exception as e:
                self.logger.error(f"微信自动化实例初始化失败: {e}")
                self._wechat_auto = None
        return self._wechat_auto
    
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
            if self.wechat_auto:
                self.wechat_auto.send_message_to_friend(
                    friend=friend_name,
                    message=message,
                    close_wechat=False
                )
                return True
            else:
                self.logger.error("微信自动化实例未初始化")
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
            if self.wechat_auto:
                _ = self.wechat_auto.send_message_to_group(group_name, message)
                if _:
                    #todo 将内容保存在数据库中
                    pass
                return True
            else:
                self.logger.error("微信自动化实例未初始化")
                return False
        except Exception as e:
            self.logger.error(f"发送消息到群聊失败: {e}")
            return False
    
    def check_new_messages(self, duration: str = "10s") -> List[Dict[str, Any]]:
        """
        检查新消息
        
        Args:
            duration (str): 检查时长
            
        Returns:
            List[Dict[str, Any]]: 新消息列表
        """
        try:
            if self.wechat_auto:
                new_messages = self.wechat_auto.check_new_message(
                    duration=duration,
                    close_wechat=False
                )
                return new_messages if new_messages else []
            else:
                self.logger.error("微信自动化实例未初始化")
                return []
        except Exception as e:
            self.logger.error(f"检查新消息失败: {e}")
            return []