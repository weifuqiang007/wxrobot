import time
import signal
import sys
from typing import Optional
import logging
from datetime import datetime

from config import ConfigManager
from wechat_service_simple import WechatService
from news_service import NewsService

class WechatBackendApp:
    """
    微信后端应用主类（修复版本）
    使用简化的WechatService避免pywechat语法错误
    """
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化应用
        
        Args:
            config_file: 配置文件路径
        """
        # 初始化配置管理器
        self.config_manager = ConfigManager(config_file)
        
        # 初始化服务
        self.wechat_service = WechatService(self.config_manager)
        self.news_service = NewsService(self.config_manager.news_config)
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # 运行状态
        self.is_running = False
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("微信后端应用初始化完成")
    
    def start(self):
        """
        启动应用
        """
        if self.is_running:
            self.logger.warning("应用已在运行")
            return
        
        self.logger.info("启动微信后端应用...")
        
        try:
            # 启动微信服务
            self.wechat_service.start_service()
            
            self.is_running = True
            self.logger.info("微信后端应用启动成功")
            
            # 主循环
            self._main_loop()
            
        except Exception as e:
            self.logger.error(f"启动应用时出错: {e}")
            self.stop()
    
    def stop(self):
        """
        停止应用
        """
        if not self.is_running:
            return
        
        self.logger.info("正在停止微信后端应用...")
        
        self.is_running = False
        
        # 停止微信服务
        if hasattr(self, 'wechat_service'):
            self.wechat_service.stop_service()
        
        self.logger.info("微信后端应用已停止")
    
    def _main_loop(self):
        """
        主循环
        """
        self.logger.info("进入主循环")
        
        try:
            while self.is_running:
                # 检查服务状态
                self._check_services()
                
                # 等待一段时间
                time.sleep(10)
                
        except KeyboardInterrupt:
            self.logger.info("收到中断信号")
        except Exception as e:
            self.logger.error(f"主循环出错: {e}")
        finally:
            self.stop()
    
    def _check_services(self):
        """
        检查服务状态
        """
        # 这里可以添加服务健康检查逻辑
        pass
    
    def _signal_handler(self, signum, frame):
        """
        信号处理器
        
        Args:
            signum: 信号编号
            frame: 当前栈帧
        """
        self.logger.info(f"收到信号 {signum}，准备退出")
        self.stop()
        sys.exit(0)
    
    # API接口方法
    def get_status(self) -> dict:
        """
        获取应用状态
        
        Returns:
            dict: 状态信息
        """
        return {
            "running": self.is_running,
            "wechat_service": self.wechat_service.is_running if hasattr(self.wechat_service, 'is_running') else False,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    
    def send_message(self, target: str, message: str, target_type: str = "friend") -> bool:
        """
        发送消息
        
        Args:
            target: 目标名称
            message: 消息内容
            target_type: 目标类型（friend/group）
            
        Returns:
            bool: 发送是否成功
        """
        try:
            if target_type == "group":
                return self.wechat_service.send_message_to_group(target, message)
            else:
                return self.wechat_service.send_message_to_friend(target, message)
        except Exception as e:
            self.logger.error(f"发送消息失败: {e}")
            return False
    
    def get_friends(self) -> list:
        """
        获取好友列表
        
        Returns:
            list: 好友列表
        """
        try:
            return self.wechat_service.get_friend_list()
        except Exception as e:
            self.logger.error(f"获取好友列表失败: {e}")
            return []
    
    def get_groups(self) -> list:
        """
        获取群聊列表
        
        Returns:
            list: 群聊列表
        """
        try:
            return self.wechat_service.get_group_list()
        except Exception as e:
            self.logger.error(f"获取群聊列表失败: {e}")
            return []
    
    def add_news_group(self, group_name: str) -> bool:
        """
        添加新闻推送群组
        
        Args:
            group_name: 群组名称
            
        Returns:
            bool: 添加是否成功
        """
        try:
            self.config_manager.add_news_group(group_name)
            return True
        except Exception as e:
            self.logger.error(f"添加新闻群组失败: {e}")
            return False
    
    def remove_news_group(self, group_name: str) -> bool:
        """
        移除新闻推送群组
        
        Args:
            group_name: 群组名称
            
        Returns:
            bool: 移除是否成功
        """
        try:
            self.config_manager.remove_news_group(group_name)
            return True
        except Exception as e:
            self.logger.error(f"移除新闻群组失败: {e}")
            return False
    
    def set_news_push_time(self, push_time: str) -> bool:
        """
        设置新闻推送时间
        
        Args:
            push_time: 推送时间（HH:MM格式）
            
        Returns:
            bool: 设置是否成功
        """
        try:
            self.config_manager.update_news_config(push_time=push_time)
            return True
        except Exception as e:
            self.logger.error(f"设置新闻推送时间失败: {e}")
            return False
    
    def test_news_fetch(self) -> str:
        """
        测试新闻获取
        
        Returns:
            str: 新闻内容
        """
        try:
            return self.news_service.get_daily_news()
        except Exception as e:
            self.logger.error(f"测试新闻获取失败: {e}")
            return f"新闻获取失败: {e}"
    
    def update_config(self, config_type: str, **kwargs) -> bool:
        """
        更新配置
        
        Args:
            config_type: 配置类型（wechat/news/reply）
            **kwargs: 配置参数
            
        Returns:
            bool: 更新是否成功
        """
        try:
            if config_type == "wechat":
                self.config_manager.update_wechat_config(**kwargs)
            elif config_type == "news":
                self.config_manager.update_news_config(**kwargs)
            elif config_type == "reply":
                self.config_manager.update_reply_config(**kwargs)
            else:
                raise ValueError(f"未知的配置类型: {config_type}")
            
            return True
        except Exception as e:
            self.logger.error(f"更新配置失败: {e}")
            return False
    
    def get_config(self) -> dict:
        """
        获取当前配置
        
        Returns:
            dict: 配置信息
        """
        try:
            return self.config_manager.get_all_config()
        except Exception as e:
            self.logger.error(f"获取配置失败: {e}")
            return {}


def main():
    """
    主函数
    """
    print("🤖 微信后端自动化系统 v1.0.0")
    print("=" * 50)
    
    try:
        # 创建应用实例
        app = WechatBackendApp()
        
        # 启动应用
        app.start()
        
    except KeyboardInterrupt:
        print("\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()