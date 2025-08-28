from .WechatAuto import (Messages, Files, Contacts, FriendSettings, GroupSettings, AutoReply, Call, Moments,
                         WechatSettings)


class WechatAuto:
    """
    微信自动化主类
    包装所有微信自动化功能
    """

    def __init__(self):
        self.messages = Messages()
        self.files = Files()
        self.contacts = Contacts()
        self.friend_settings = FriendSettings()
        self.group_settings = GroupSettings()
        self.auto_reply = AutoReply()
        self.call = Call()
        self.moments = Moments()
        self.wechat_settings = WechatSettings()

    def send_message_to_friend(self, friend_name: str, message: str) -> bool:
        """
        发送单条消息给好友
        """
        try:
            self.messages.send_message_to_friend(friend_name, message)
            return True
        except Exception:
            return False

    def send_message_to_group(self, group_name: str, message: str) -> bool:
        """
        发送单条消息给群组
        """
        print("发送群组消息:", group_name)
        print("neirong ", message)
        try:
            self.messages.send_message_to_friend(friend=group_name, message=message)
            return True
        except Exception:
            return False

    def send_messages_to_friend(self, friend_name: str, messages: list) -> bool:
        """
        发送多条消息给好友
        """
        try:
            self.messages.send_messages_to_friend(friend_name, messages)
            return True
        except Exception:
            return False

    def send_messages_to_group(self, group_name: str, messages: list) -> bool:
        """
        发送多条消息给群组
        """
        try:
            self.messages.send_messages_to_friend(group_name, messages)
            return True
        except Exception:
            return False

    def check_new_message(self, duration: str = "10s") -> list:
        """
        检查新消息
        """
        try:
            # 这里需要根据实际的API来实现
            # 暂时返回空列表
            return []
        except Exception:
            return []
