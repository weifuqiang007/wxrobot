import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class WechatConfig:
    """
    微信配置类
    """
    wechat_path: str = None
    is_maximize: bool = True
    close_wechat: bool = False
    
@dataclass
class NewsConfig:
    """
    新闻推送配置类
    """
    enabled: bool = True
    push_time: str = "09:00"
    target_groups: List[str] = None
    news_api_url: str = None
    news_api_key: str = None
    
    def __post_init__(self):
        if self.target_groups is None:
            self.target_groups = []
            
@dataclass
class ReplyConfig:
    """
    自动回复配置类
    """
    enabled: bool = True
    default_reply: str = "收到！"
    welcome_message_template: str = "欢迎{name}用户加入群聊！"
    reply_to_private: bool = True
    reply_to_group_at_only: bool = True
    
class ConfigManager:
    """
    配置管理器
    """
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.wechat_config = WechatConfig()
        self.news_config = NewsConfig()
        self.reply_config = ReplyConfig()
        
        # 加载配置
        self.load_config()
        
    def load_config(self):
        """
        从文件加载配置
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    
                # 加载微信配置
                if 'wechat' in config_data:
                    wechat_data = config_data['wechat']
                    self.wechat_config = WechatConfig(**wechat_data)
                    
                # 加载新闻配置
                if 'news' in config_data:
                    news_data = config_data['news']
                    self.news_config = NewsConfig(**news_data)
                    
                # 加载回复配置
                if 'reply' in config_data:
                    reply_data = config_data['reply']
                    self.reply_config = ReplyConfig(**reply_data)
                    
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                self._create_default_config()
        else:
            self._create_default_config()
            
    def save_config(self):
        """
        保存配置到文件
        """
        try:
            config_data = {
                'wechat': asdict(self.wechat_config),
                'news': asdict(self.news_config),
                'reply': asdict(self.reply_config),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            
    def _create_default_config(self):
        """
        创建默认配置
        """
        self.wechat_config = WechatConfig()
        self.news_config = NewsConfig()
        self.reply_config = ReplyConfig()
        self.save_config()
        
    def update_wechat_config(self, **kwargs):
        """
        更新微信配置
        """
        for key, value in kwargs.items():
            if hasattr(self.wechat_config, key):
                setattr(self.wechat_config, key, value)
        self.save_config()
        
    def update_news_config(self, **kwargs):
        """
        更新新闻配置
        """
        for key, value in kwargs.items():
            if hasattr(self.news_config, key):
                setattr(self.news_config, key, value)
        self.save_config()
        
    def update_reply_config(self, **kwargs):
        """
        更新回复配置
        """
        for key, value in kwargs.items():
            if hasattr(self.reply_config, key):
                setattr(self.reply_config, key, value)
        self.save_config()
        
    def add_news_group(self, group_name: str):
        """
        添加新闻推送群
        """
        if group_name not in self.news_config.target_groups:
            self.news_config.target_groups.append(group_name)
            self.save_config()
            
    def remove_news_group(self, group_name: str):
        """
        移除新闻推送群
        """
        if group_name in self.news_config.target_groups:
            self.news_config.target_groups.remove(group_name)
            self.save_config()
            
    def get_all_config(self) -> Dict[str, Any]:
        """
        获取所有配置
        """
        return {
            'wechat': asdict(self.wechat_config),
            'news': asdict(self.news_config),
            'reply': asdict(self.reply_config)
        }