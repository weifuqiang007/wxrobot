#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息服务层
处理所有消息相关的业务逻辑
"""

import sys
import os
import threading
import time
import logging
from typing import List, Dict, Any, Optional

# 添加pywechat路径到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils', 'pywechat'))

from services.app_service import AppService
from services.wechat_api_service import WechatAPIService
from dao.wechat_dao import WechatDAO

class MessageService:
    """
    消息服务类
    负责处理所有消息相关的业务逻辑
    """
    
    def __init__(self):
        self.app_service = AppService()
        self.wechat_dao = WechatDAO()
        self.wechat_api_service = WechatAPIService()
        self.logger = logging.getLogger(__name__)
        self.monitoring = False
        self.monitor_thread = None
        self.auto_reply_message = "恭喜发财"  # 默认自动回复消息
        self.start_time = None
        self.processed_count = 0
        self.reply_count = 0
    
    def send_message_business_logic(self, target: str, message: str, target_type: str = 'friend') -> Dict[str, Any]:
        """
        发送消息的业务逻辑
        
        Args:
            target (str): 目标用户或群组
            message (str): 消息内容
            target_type (str): 目标类型（friend/group）
            
        Returns:
            dict: 处理结果
        """
        try:
            # 业务逻辑：验证参数
            if not target or not target.strip():
                return {
                    "success": False,
                    "error": "目标不能为空",
                    "status_code": 400
                }
            
            if not message or not message.strip():
                return {
                    "success": False,
                    "error": "消息内容不能为空",
                    "status_code": 400
                }
            
            # 业务逻辑：检查应用实例
            app_instance = self.app_service.get_app_instance()
            if not app_instance:
                return {
                    "success": False,
                    "error": "微信后端应用未初始化",
                    "status_code": 500
                }
            
            # 业务逻辑：调用微信API发送消息
            if target_type == 'friend':
                success = self.wechat_api_service.send_message_to_friend(target.strip(), message.strip())
            elif target_type == 'group':
                success = self.wechat_api_service.send_message_to_group(target.strip(), message.strip())
            else:
                return {
                    "success": False,
                    "error": f"不支持的目标类型: {target_type}",
                    "status_code": 400
                }
            
            if success:
                # 业务逻辑：记录发送成功的消息到数据库
                self.wechat_dao.save_message_record_to_database(target.strip(), message.strip(), target_type, 'sent')
                return {
                    "success": True,
                    "message": f"消息已发送到 {target.strip()}"
                }
            else:
                return {
                    "success": False,
                    "error": "发送消息失败",
                    "status_code": 500
                }
                
        except Exception as e:
            self.logger.error(f"发送消息业务逻辑处理失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def start_monitoring_business_logic(self, duration: str = "1h") -> Dict[str, Any]:
        """
        启动消息监控的业务逻辑
        
        Args:
            duration (str): 监控持续时间
            
        Returns:
            dict: 处理结果
        """
        try:
            # 业务逻辑：检查监控状态
            if self.monitoring:
                return {
                    "success": False,
                    "error": "消息监控已在运行中",
                    "status_code": 400
                }
            
            # 业务逻辑：验证持续时间格式
            if not self._validate_duration_format(duration):
                return {
                    "success": False,
                    "error": "持续时间格式无效，支持格式：1s, 30min, 2h",
                    "status_code": 400
                }
            
            # 业务逻辑：启动监控
            self.monitoring = True
            self.start_time = time.time()
            self.processed_count = 0
            self.reply_count = 0
            
            self.monitor_thread = threading.Thread(
                target=self._monitor_messages_business_logic,
                args=(duration,),
                daemon=True
            )
            self.monitor_thread.start()
            
            self.logger.info(f"消息监控已启动，持续时间: {duration}")
            return {
                "success": True,
                "message": f"消息监控已启动，持续时间: {duration}"
            }
            
        except Exception as e:
            self.logger.error(f"启动消息监控业务逻辑处理失败: {e}")
            self.monitoring = False
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def stop_monitoring_business_logic(self) -> Dict[str, Any]:
        """
        停止消息监控的业务逻辑
        
        Returns:
            dict: 处理结果
        """
        try:
            # 业务逻辑：检查监控状态
            if not self.monitoring:
                return {
                    "success": False,
                    "error": "消息监控未在运行",
                    "status_code": 400
                }
            
            # 业务逻辑：停止监控
            self.monitoring = False
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=5)
            
            self.logger.info("消息监控已停止")
            return {
                "success": True,
                "message": "消息监控已停止"
            }
            
        except Exception as e:
            self.logger.error(f"停止消息监控业务逻辑处理失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def get_monitoring_status_business_logic(self) -> Dict[str, Any]:
        """
        获取监控状态的业务逻辑
        
        Returns:
            dict: 监控状态信息
        """
        try:
            # 业务逻辑：计算运行时间
            running_duration = 0
            if self.monitoring and self.start_time:
                running_duration = int(time.time() - self.start_time)
            
            return {
                "success": True,
                "data": {
                    "monitoring": self.monitoring,
                    "auto_reply_message": self.auto_reply_message,
                    "thread_alive": self.monitor_thread.is_alive() if self.monitor_thread else False,
                    "start_time": self.start_time,
                    "running_duration": running_duration,
                    "processed_count": self.processed_count,
                    "reply_count": self.reply_count
                }
            }
        except Exception as e:
            self.logger.error(f"获取监控状态业务逻辑处理失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def set_auto_reply_message_business_logic(self, message: str) -> Dict[str, Any]:
        """
        设置自动回复消息的业务逻辑
        
        Args:
            message (str): 自动回复消息内容
            
        Returns:
            dict: 处理结果
        """
        try:
            # 业务逻辑：验证消息内容
            if not message or not message.strip():
                return {
                    "success": False,
                    "error": "回复消息不能为空",
                    "status_code": 400
                }
            
            # 业务逻辑：验证消息长度
            if len(message.strip()) > 500:
                return {
                    "success": False,
                    "error": "回复消息长度不能超过500字符",
                    "status_code": 400
                }
            
            # 业务逻辑：设置自动回复消息
            self.auto_reply_message = message.strip()
            self.logger.info(f"自动回复消息已设置为: {self.auto_reply_message}")
            
            return {
                "success": True,
                "message": f"自动回复消息已设置为: {self.auto_reply_message}"
            }
            
        except Exception as e:
            self.logger.error(f"设置自动回复消息业务逻辑处理失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    def _validate_duration_format(self, duration: str) -> bool:
        """
        验证持续时间格式的业务逻辑
        
        Args:
            duration (str): 持续时间字符串
            
        Returns:
            bool: 格式是否有效
        """
        import re
        pattern = r'^\d+[smh]$|^\d+min$'
        return bool(re.match(pattern, duration.lower()))
    
    def _monitor_messages_business_logic(self, duration: str):
        """
        消息监控主循环的业务逻辑
        
        Args:
            duration (str): 监控持续时间
        """
        try:
            self.logger.info(f"开始监控微信消息，持续时间: {duration}")
            
            while self.monitoring:
                try:
                    # 业务逻辑：检查新消息（通过微信API服务）
                    new_messages = self.wechat_api_service.check_new_messages("10s")
                    
                    if new_messages:
                        self.logger.info(f"检测到 {len(new_messages)} 条新消息")
                        self.processed_count += len(new_messages)
                        
                        # 业务逻辑：处理每条新消息
                        for message_info in new_messages:
                            if self._process_new_message_business_logic(message_info):
                                self.reply_count += 1
                    
                    # 业务逻辑：休眠间隔
                    time.sleep(10)
                    
                except Exception as e:
                    self.logger.error(f"监控消息业务逻辑处理时发生错误: {e}")
                    time.sleep(5)
                    
        except Exception as e:
            self.logger.error(f"消息监控线程业务逻辑异常: {e}")
        finally:
            self.monitoring = False
            self.logger.info("消息监控已结束")
    
    def _process_new_message_business_logic(self, message_info: Dict[str, Any]) -> bool:
        """
        处理新消息并自动回复的业务逻辑
        
        Args:
            message_info (dict): 消息信息
            
        Returns:
            bool: 是否成功回复
        """
        try:
            friend_name = message_info.get('好友名称', '')
            friend_type = message_info.get('好友类型', '')
            message_count = message_info.get('新消息条数', 0)
            message_contents = message_info.get('消息内容', [])
            
            self.logger.info(f"处理来自 {friend_name}({friend_type}) 的 {message_count} 条新消息")
            
            # 业务逻辑：记录消息内容
            for i, content in enumerate(message_contents):
                self.logger.info(f"消息 {i+1}: {content}")
                # 保存接收到的消息记录到数据库
                self.wechat_dao.save_message_record_to_database(friend_name, content, friend_type, 'received')
            
            # 业务逻辑：判断是否需要自动回复
            if friend_name and friend_type in ['好友', '群聊'] and self.auto_reply_message:
                try:
                    # 调用微信API服务发送自动回复
                    success = self.wechat_api_service.send_message_to_friend(friend_name, self.auto_reply_message)
                    if success:
                        self.logger.info(f"已向 {friend_name} 自动回复: {self.auto_reply_message}")
                        # 保存自动回复记录到数据库
                        self.wechat_dao.save_auto_reply_to_database(friend_name, self.auto_reply_message, message_contents[-1] if message_contents else '')
                    else:
                        self.logger.error(f"向 {friend_name} 发送自动回复失败")
                    
                    if success:
                        return True
                    else:
                        self.logger.error(f"向 {friend_name} 自动回复失败")
                        return False
                        
                except Exception as e:
                    self.logger.error(f"向 {friend_name} 自动回复失败: {e}")
                    return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"处理新消息业务逻辑时发生错误: {e}")
            return False