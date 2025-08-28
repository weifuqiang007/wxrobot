import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
import logging

class WechatService:
    """
    微信自动化服务类（简化版本）
    提供与pywechat兼容的接口，但暂时使用模拟实现
    """
    
    def __init__(self, config_manager):
        """
        初始化微信服务
        
        Args:
            config_manager: 配置管理器
        """
        self.config_manager = config_manager
        self.is_running = False
        self.message_handlers = []
        self.group_handlers = []
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 模拟pywechat组件
        self.messages = MockMessages()
        self.contacts = MockContacts()
        self.tools = MockTools()
        
        self.logger.info("微信服务初始化完成（简化模式）")
    
    def start_service(self):
        """
        启动微信服务
        """
        if self.is_running:
            self.logger.warning("微信服务已在运行")
            return
        
        self.is_running = True
        self.logger.info("启动微信服务...")
        
        # 启动消息监听线程
        self.message_thread = threading.Thread(target=self._message_listener, daemon=True)
        self.message_thread.start()
        
        # 启动定时新闻推送线程
        self.news_thread = threading.Thread(target=self._daily_news_scheduler, daemon=True)
        self.news_thread.start()
        
        self.logger.info("微信服务启动成功")
    
    def stop_service(self):
        """
        停止微信服务
        """
        self.logger.info("停止微信服务...")
        self.is_running = False
        self.logger.info("微信服务已停止")
    
    def process_messages(self):
        """
        处理消息（模拟）
        """
        self.logger.info("处理消息中...")
        # 模拟消息处理逻辑
        return True
    
    def push_daily_news(self):
        """
        推送每日新闻（模拟）
        """
        self.logger.info("推送每日新闻...")
        # 模拟新闻推送逻辑
        return True
    
    def _message_listener(self):
        """
        消息监听器（模拟实现）
        """
        self.logger.info("消息监听器启动")
        
        while self.is_running:
            try:
                # 模拟消息检查
                time.sleep(5)  # 每5秒检查一次
                
                # 这里应该调用pywechat的消息检查功能
                # 暂时使用模拟实现
                self._simulate_message_check()
                
            except Exception as e:
                self.logger.error(f"消息监听器错误: {e}")
                time.sleep(10)
    
    def _simulate_message_check(self):
        """
        模拟消息检查（用于测试）
        """
        # 这里可以添加模拟消息处理逻辑
        pass
    
    def _handle_message(self, friend_name: str, friend_type: str, content: str, message_type: str):
        """
        处理接收到的消息
        
        Args:
            friend_name: 发送者名称
            friend_type: 消息类型（群聊/私聊）
            content: 消息内容
            message_type: 消息类型
        """
        try:
            # 检查是否启用自动回复
            if not self.config_manager.reply_config.enabled:
                return
            
            # 处理群聊消息
            if friend_type == "群聊":
                # 检查新成员加入
                if self._is_new_member_message(content):
                    self._handle_new_member(friend_name, content)
                    return
                
                # 检查是否只回复@消息
                if self.config_manager.reply_config.reply_to_group_at_only:
                    if "@" not in content:  # 简化的@检测
                        return
                
                # 发送群聊回复
                reply_message = self.config_manager.reply_config.default_reply
                self._send_message(friend_name, reply_message)
                
            # 处理私聊消息
            elif friend_type == "私聊":
                if self.config_manager.reply_config.reply_to_private:
                    reply_message = self.config_manager.reply_config.default_reply
                    self._send_message(friend_name, reply_message)
                    
        except Exception as e:
            self.logger.error(f"处理消息时出错: {e}")
    
    def _is_new_member_message(self, content: str) -> bool:
        """
        检查是否为新成员加入消息
        """
        keywords = ["加入了群聊", "邀请", "加入群聊", "通过扫描"]
        return any(keyword in content for keyword in keywords)
    
    def _handle_new_member(self, group_name: str, content: str):
        """
        处理新成员加入
        
        Args:
            group_name: 群聊名称
            content: 消息内容
        """
        try:
            # 提取新成员名称
            member_name = self._extract_member_name(content)
            
            # 格式化欢迎消息
            welcome_template = self.config_manager.reply_config.welcome_message_template
            welcome_message = welcome_template.format(
                name=member_name,
                group=group_name
            )
            
            # 发送欢迎消息
            self._send_message(group_name, welcome_message)
            
            self.logger.info(f"已向 {group_name} 发送新成员 {member_name} 的欢迎消息")
            
        except Exception as e:
            self.logger.error(f"处理新成员加入时出错: {e}")
    
    def _extract_member_name(self, content: str) -> str:
        """
        从消息内容中提取新成员名称
        
        Args:
            content: 消息内容
            
        Returns:
            str: 成员名称
        """
        # 简化的名称提取逻辑
        # 实际应该根据微信的具体消息格式来解析
        import re
        
        patterns = [
            r'"([^"]+)".*加入了群聊',
            r'([^\s]+).*加入了群聊',
            r'邀请"([^"]+)"加入了群聊'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
        
        return "新成员"
    
    def _daily_news_scheduler(self):
        """
        定时新闻推送调度器
        """
        while self.is_running:
            try:
                # 检查是否启用新闻推送
                if not self.config_manager.news_config.enabled:
                    time.sleep(60)  # 如果未启用，等待1分钟后再检查
                    continue
                
                # 获取推送时间
                push_time = self.config_manager.news_config.push_time
                current_time = datetime.now().strftime("%H:%M")
                
                if current_time == push_time:
                    self._send_daily_news()
                    # 等待到下一分钟，避免重复发送
                    time.sleep(60)
                else:
                    time.sleep(30)  # 每30秒检查一次
                    
            except Exception as e:
                self.logger.error(f"定时新闻调度器错误: {e}")
                time.sleep(60)
    
    def _send_daily_news(self):
        """
        发送每日新闻
        """
        try:
            # 获取新闻内容
            news_content = self._get_daily_news()
            
            # 获取目标群组
            target_groups = self.config_manager.news_config.target_groups
            
            if not target_groups:
                self.logger.warning("没有配置新闻推送目标群组")
                return
            
            # 向每个群组发送新闻
            for group_name in target_groups:
                self._send_message(group_name, news_content)
                time.sleep(1)  # 避免发送过快
            
            self.logger.info(f"已向 {len(target_groups)} 个群组发送每日新闻")
            
        except Exception as e:
            self.logger.error(f"发送每日新闻时出错: {e}")
    
    def _get_daily_news(self) -> str:
        """
        获取每日新闻内容
        
        Returns:
            str: 格式化的新闻内容
        """
        try:
            from news_service import NewsService
            news_service = NewsService(self.config_manager.news_config)
            return news_service.get_daily_news()
        except Exception as e:
            self.logger.error(f"获取新闻失败: {e}")
            return "📰 今日新闻获取失败，请稍后再试。"
    
    def _send_message(self, target: str, message: str):
        """
        发送消息（模拟实现）
        
        Args:
            target: 目标（群聊名称或好友名称）
            message: 消息内容
        """
        # 这里应该调用pywechat的发送消息功能
        # 暂时使用日志模拟
        self.logger.info(f"[模拟发送] 向 {target} 发送消息: {message[:50]}...")
        
        # 实际实现应该是：
        # self.messages.send_message_to_friend(target, message)
    
    def send_message_to_friend(self, friend_name: str, message: str) -> bool:
        """
        向好友发送消息
        
        Args:
            friend_name: 好友名称
            message: 消息内容
            
        Returns:
            bool: 发送是否成功
        """
        try:
            self._send_message(friend_name, message)
            return True
        except Exception as e:
            self.logger.error(f"发送消息失败: {e}")
            return False
    
    def send_message_to_group(self, group_name: str, message: str) -> bool:
        """
        向群聊发送消息
        
        Args:
            group_name: 群聊名称
            message: 消息内容
            
        Returns:
            bool: 发送是否成功
        """
        try:
            self._send_message(group_name, message)
            return True
        except Exception as e:
            self.logger.error(f"发送群聊消息失败: {e}")
            return False
    
    def get_friend_list(self) -> List[str]:
        """
        获取好友列表
        
        Returns:
            List[str]: 好友名称列表
        """
        # 模拟返回
        return ["好友1", "好友2", "好友3"]
    
    def get_group_list(self) -> List[str]:
        """
        获取群聊列表
        
        Returns:
            List[str]: 群聊名称列表
        """
        # 模拟返回
        return ["群聊1", "群聊2", "群聊3"]


class MockMessages:
    """模拟pywechat的Messages类"""
    
    def send_message_to_friend(self, friend_name: str, message: str):
        print(f"[Mock] 向好友 {friend_name} 发送消息: {message}")
    
    def send_message_to_group(self, group_name: str, message: str):
        print(f"[Mock] 向群聊 {group_name} 发送消息: {message}")


class MockContacts:
    """模拟pywechat的Contacts类"""
    
    def get_all_friends(self):
        return ["好友1", "好友2", "好友3"]
    
    def get_all_groups(self):
        return ["群聊1", "群聊2", "群聊3"]


class MockTools:
    """模拟pywechat的Tools类"""
    
    def check_wechat_status(self):
        return True
    
    def open_wechat(self):
        print("[Mock] 打开微信")