#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新成员欢迎服务层
处理群组新成员自动欢迎的业务逻辑
"""

import sys
import os
import threading
import time
import logging
import re
from typing import List, Dict, Any, Optional

# 添加pywechat路径到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils', 'pywechat'))

from services.app_service import AppService
from services.wechat_api_service import WechatAPIService
from dao.wechat_dao import WechatDAO
from dao.config_dao import ConfigDAO

class WelcomeService:
    """
    新成员欢迎服务类
    负责处理群组新成员自动欢迎的业务逻辑
    """
    
    def __init__(self):
        self.app_service = AppService()
        self.wechat_dao = WechatDAO()
        self.wechat_api_service = WechatAPIService()
        self.config_dao = ConfigDAO()
        self.logger = logging.getLogger(__name__)
        
        # 监听状态
        self.monitoring = False
        self.monitor_thread = None
        self.start_time = None
        self.processed_count = 0
        self.welcome_count = 0
        
        # 配置信息
        self.monitored_groups = []  # 监听的群组列表
        self.welcome_message_template = "欢迎 @{member_name} 加入群聊！🎉"
        self.new_member_patterns = [
            r'"(.+?)"通过扫描你分享的二维码加入群聊',
            r'"(.+?)"加入了群聊',
            r'你邀请"(.+?)"加入了群聊',
            r'(.+?)加入了群聊',
            r'"(.+?)"已加入群聊'
        ]
    
    def start_welcome_monitoring_business_logic(self, groups: List[str] = None, duration: str = "24h") -> Dict[str, Any]:
        """
        开始新成员欢迎监听的业务逻辑
        
        Args:
            groups (List[str]): 要监听的群组列表，None表示监听所有群组
            duration (str): 监听持续时间
            
        Returns:
            dict: 处理结果


        """

        #todo 这里需要做数据库的查询
        if self.monitoring:
            return {
                'success': False,
                'message': '新成员欢迎监听已在运行中',
                'data': {
                    'status': 'already_running',
                    'start_time': self.start_time,
                    'monitored_groups': self.monitored_groups
                }
            }
        
        # 验证持续时间格式
        if not self._validate_duration_format(duration):
            return {
                'success': False,
                'message': f'持续时间格式无效: {duration}，请使用如 "1h", "30m", "2d" 等格式',
                'data': None
            }
        
        # 设置监听的群组
        if groups is None:
            # 获取所有群组
            all_groups = self.wechat_dao.get_groups_list()
            self.monitored_groups = all_groups
        else:
            self.monitored_groups = groups
            
        try:
            
            # 启动监听线程
            self.monitoring = True
            self.start_time = time.time()
            self.processed_count = 0
            self.welcome_count = 0
            
            self.monitor_thread = threading.Thread(
                target=self._monitor_new_members_business_logic,
                args=(duration,),
                daemon=True
            )
            self.monitor_thread.start()
            
            self.logger.info(f"新成员欢迎监听已启动，监听群组: {len(self.monitored_groups)} 个，持续时间: {duration}")
            
            return {
                'success': True,
                'message': f'新成员欢迎监听已启动，监听 {len(self.monitored_groups)} 个群组',
                'data': {
                    'status': 'started',
                    'start_time': self.start_time,
                    'duration': duration,
                    'monitored_groups': self.monitored_groups
                }
            }
            
        except Exception as e:
            self.logger.error(f"启动新成员欢迎监听失败: {e}")
            return {
                'success': False,
                'message': f'启动新成员欢迎监听失败: {str(e)}',
                'data': None
            }
    
    def stop_welcome_monitoring_business_logic(self) -> Dict[str, Any]:
        """
        停止新成员欢迎监听的业务逻辑
        
        Returns:
            dict: 处理结果
        """
        try:
            if not self.monitoring:
                return {
                    'success': False,
                    'message': '新成员欢迎监听未在运行',
                    'data': {
                        'status': 'not_running'
                    }
                }
            
            # 停止监听
            self.monitoring = False
            
            # 等待监听线程结束
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=5)
            
            end_time = time.time()
            duration = end_time - self.start_time if self.start_time else 0
            
            self.logger.info(f"新成员欢迎监听已停止，运行时长: {duration:.2f}秒，处理消息: {self.processed_count} 条，发送欢迎: {self.welcome_count} 次")
            
            result_data = {
                'status': 'stopped',
                'duration': duration,
                'processed_count': self.processed_count,
                'welcome_count': self.welcome_count,
                'monitored_groups': self.monitored_groups
            }
            
            # 重置状态
            self.start_time = None
            self.processed_count = 0
            self.welcome_count = 0
            self.monitored_groups = []
            
            return {
                'success': True,
                'message': f'新成员欢迎监听已停止，共发送 {result_data["welcome_count"]} 次欢迎消息',
                'data': result_data
            }
            
        except Exception as e:
            self.logger.error(f"停止新成员欢迎监听失败: {e}")
            return {
                'success': False,
                'message': f'停止新成员欢迎监听失败: {str(e)}',
                'data': None
            }
    
    def get_welcome_monitoring_status_business_logic(self) -> Dict[str, Any]:
        """
        获取新成员欢迎监听状态的业务逻辑
        
        Returns:
            dict: 监听状态信息
        """
        try:
            if self.monitoring and self.start_time:
                current_time = time.time()
                running_duration = current_time - self.start_time
                
                status_data = {
                    'status': 'running',
                    'start_time': self.start_time,
                    'running_duration': running_duration,
                    'processed_count': self.processed_count,
                    'welcome_count': self.welcome_count,
                    'monitored_groups': self.monitored_groups,
                    'monitored_groups_count': len(self.monitored_groups)
                }
            else:
                status_data = {
                    'status': 'stopped',
                    'start_time': None,
                    'running_duration': 0,
                    'processed_count': 0,
                    'welcome_count': 0,
                    'monitored_groups': [],
                    'monitored_groups_count': 0
                }
            
            return {
                'success': True,
                'message': '获取新成员欢迎监听状态成功',
                'data': status_data
            }
            
        except Exception as e:
            self.logger.error(f"获取新成员欢迎监听状态失败: {e}")
            return {
                'success': False,
                'message': f'获取新成员欢迎监听状态失败: {str(e)}',
                'data': None
            }
    
    def set_welcome_message_template_business_logic(self, template: str) -> Dict[str, Any]:
        """
        设置欢迎消息模板的业务逻辑
        
        Args:
            template (str): 欢迎消息模板，支持 {member_name} 占位符
            
        Returns:
            dict: 处理结果
        """
        try:
            if not template or not template.strip():
                return {
                    'success': False,
                    'message': '欢迎消息模板不能为空',
                    'data': None
                }
            
            self.welcome_message_template = template.strip()
            self.logger.info(f"欢迎消息模板已更新: {self.welcome_message_template}")
            
            return {
                'success': True,
                'message': '欢迎消息模板设置成功',
                'data': {
                    'template': self.welcome_message_template
                }
            }
            
        except Exception as e:
            self.logger.error(f"设置欢迎消息模板失败: {e}")
            return {
                'success': False,
                'message': f'设置欢迎消息模板失败: {str(e)}',
                'data': None
            }
    
    def get_monitored_groups_business_logic(self) -> Dict[str, Any]:
        """
        获取当前监听的群组列表的业务逻辑
        
        Returns:
            dict: 群组列表信息
        """
        try:
            all_groups = self.wechat_dao.get_groups_list()
            
            return {
                'success': True,
                'message': '获取群组列表成功',
                'data': {
                    'all_groups': all_groups,
                    'monitored_groups': self.monitored_groups,
                    'monitoring_status': self.monitoring
                }
            }
            
        except Exception as e:
            self.logger.error(f"获取群组列表失败: {e}")
            return {
                'success': False,
                'message': f'获取群组列表失败: {str(e)}',
                'data': None
            }
    
    def _validate_duration_format(self, duration: str) -> bool:
        """
        验证持续时间格式
        
        Args:
            duration (str): 持续时间字符串
            
        Returns:
            bool: 格式是否有效
        """
        pattern = r'^\d+[smhd]$'
        return bool(re.match(pattern, duration.lower()))
    
    def _monitor_new_members_business_logic(self, duration: str):
        """
        新成员监控主循环的业务逻辑
        
        Args:
            duration (str): 监控持续时间
        """
        try:
            self.logger.info(f"开始监控群组新成员，监听群组: {len(self.monitored_groups)} 个，持续时间: {duration}")
            
            while self.monitoring:
                try:
                    # 业务逻辑：检查新消息（通过微信API服务）
                    new_messages = self.wechat_api_service.check_new_messages("10s")
                    
                    if new_messages:
                        self.logger.debug(f"检测到 {len(new_messages)} 条新消息")
                        self.processed_count += len(new_messages)
                        
                        # 业务逻辑：处理每条新消息，检查是否为新成员加入消息
                        for message_info in new_messages:
                            if self._process_new_member_message_business_logic(message_info):
                                self.welcome_count += 1
                    
                    # 业务逻辑：休眠间隔
                    time.sleep(10)
                    
                except Exception as e:
                    self.logger.error(f"监控新成员业务逻辑处理时发生错误: {e}")
                    time.sleep(5)
                    
        except Exception as e:
            self.logger.error(f"新成员监控线程业务逻辑异常: {e}")
        finally:
            self.monitoring = False
            self.logger.info("新成员监控已结束")
    
    def _process_new_member_message_business_logic(self, message_info: Dict[str, Any]) -> bool:
        """
        处理新消息并检查是否为新成员加入消息的业务逻辑
        
        Args:
            message_info (dict): 消息信息
            
        Returns:
            bool: 是否成功发送欢迎消息
        """
        try:
            friend_name = message_info.get('好友名称', '')
            friend_type = message_info.get('好友类型', '')
            message_contents = message_info.get('消息内容', [])
            
            # 业务逻辑：只处理群聊消息
            if friend_type != '群聊':
                return False
            
            # 业务逻辑：检查是否在监听的群组中
            if self.monitored_groups and friend_name not in self.monitored_groups:
                return False
            
            # 业务逻辑：检查消息内容是否为新成员加入消息
            for content in message_contents:
                new_member_name = self._extract_new_member_name_business_logic(content)
                if new_member_name:
                    self.logger.info(f"检测到新成员 {new_member_name} 加入群聊 {friend_name}")
                    
                    # 业务逻辑：发送欢迎消息
                    welcome_message = self.welcome_message_template.format(member_name=new_member_name)
                    
                    try:
                        # 调用微信API服务发送欢迎消息
                        success = self.wechat_api_service.send_message_to_group(friend_name, welcome_message)
                        if success:
                            self.logger.info(f"已向群聊 {friend_name} 发送欢迎消息: {welcome_message}")
                            # 保存欢迎消息记录到数据库
                            self.wechat_dao.save_message_record_to_database(
                                friend_name, welcome_message, '群聊', 'welcome_sent'
                            )
                            return True
                        else:
                            self.logger.error(f"向群聊 {friend_name} 发送欢迎消息失败")
                            return False
                            
                    except Exception as e:
                        self.logger.error(f"向群聊 {friend_name} 发送欢迎消息失败: {e}")
                        return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"处理新成员消息业务逻辑时发生错误: {e}")
            return False
    
    def _extract_new_member_name_business_logic(self, message_content: str) -> Optional[str]:
        """
        从消息内容中提取新成员名称的业务逻辑
        
        Args:
            message_content (str): 消息内容
            
        Returns:
            Optional[str]: 新成员名称，如果不是新成员消息则返回None
        """
        try:
            for pattern in self.new_member_patterns:
                match = re.search(pattern, message_content)
                if match:
                    member_name = match.group(1)
                    self.logger.debug(f"匹配到新成员模式: {pattern}, 成员名称: {member_name}")
                    return member_name
            
            return None
            
        except Exception as e:
            self.logger.error(f"提取新成员名称时发生错误: {e}")
            return None