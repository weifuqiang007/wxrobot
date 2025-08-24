#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置数据访问对象
负责配置文件的读写操作
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import logging

class ConfigDAO:
    """
    配置数据访问对象
    """
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置DAO
        
        Args:
            config_file (str): 配置文件路径
        """
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        
        # 确保配置文件存在
        self._ensure_config_file()
    
    def _ensure_config_file(self):
        """
        确保配置文件存在，如果不存在则创建默认配置
        """
        if not os.path.exists(self.config_file):
            default_config = self._get_default_config()
            self.save_config(default_config)
            self.logger.info(f"创建默认配置文件: {self.config_file}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置
        
        Returns:
            Dict[str, Any]: 默认配置字典
        """
        return {
            "wechat": {
                "wechat_path": None,
                "is_maximize": True,
                "close_wechat": False
            },
            "news": {
                "enabled": True,
                "push_time": "09:00",
                "target_groups": [],
                "news_api_url": None,
                "news_api_key": None
            },
            "reply": {
                "enabled": True,
                "default_reply": "收到！",
                "welcome_message_template": "欢迎{name}用户加入群聊！",
                "reply_to_private": True,
                "reply_to_group_at_only": True
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def load_config(self) -> Optional[Dict[str, Any]]:
        """
        加载配置文件
        
        Returns:
            Optional[Dict[str, Any]]: 配置字典，加载失败返回None
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.logger.debug(f"配置文件加载成功: {self.config_file}")
            return config
        except FileNotFoundError:
            self.logger.error(f"配置文件不存在: {self.config_file}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"配置文件JSON格式错误: {e}")
            return None
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
            return None
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        保存配置文件
        
        Args:
            config (Dict[str, Any]): 配置字典
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 更新最后修改时间
            config["last_updated"] = datetime.now().isoformat()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"配置文件保存成功: {self.config_file}")
            return True
        except Exception as e:
            self.logger.error(f"保存配置文件失败: {e}")
            return False
    
    def update_config_section(self, section: str, updates: Dict[str, Any]) -> bool:
        """
        更新配置文件的特定部分
        
        Args:
            section (str): 配置部分名称
            updates (Dict[str, Any]): 更新的配置项
            
        Returns:
            bool: 更新是否成功
        """
        config = self.load_config()
        if config is None:
            return False
        
        if section not in config:
            config[section] = {}
        
        # 更新配置项
        config[section].update(updates)
        
        return self.save_config(config)
    
    def get_config_section(self, section: str) -> Optional[Dict[str, Any]]:
        """
        获取配置文件的特定部分
        
        Args:
            section (str): 配置部分名称
            
        Returns:
            Optional[Dict[str, Any]]: 配置部分，不存在返回None
        """
        config = self.load_config()
        if config is None:
            return None
        
        return config.get(section)
    
    def backup_config(self, backup_suffix: str = None) -> bool:
        """
        备份配置文件
        
        Args:
            backup_suffix (str): 备份文件后缀，默认使用时间戳
            
        Returns:
            bool: 备份是否成功
        """
        try:
            if backup_suffix is None:
                backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            backup_file = f"{self.config_file}.backup_{backup_suffix}"
            
            config = self.load_config()
            if config is None:
                return False
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"配置文件备份成功: {backup_file}")
            return True
        except Exception as e:
            self.logger.error(f"备份配置文件失败: {e}")
            return False