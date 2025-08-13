# 需要定义项目运行的根目录是在父级的父级目录。也就是在pywechat-main目录下

import os
import sys

# 添加pywechat-main目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# from pywechat.WechatAuto import Messages
# Messages.send_message_to_friend(friend='文件传输助手',message='你好',delay=0.2,tickle=False,search_pages=0)
#或者
import pywechat.WechatAuto as wechat
from pywechat.WechatAuto import Messages as message

message.send_message_to_friend(friend='文件传输助手',message='你好,大漂亮',tickle=False,search_pages=0, close_wechat=False)
