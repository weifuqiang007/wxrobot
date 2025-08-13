'''
WechatAuto
-------
模块:\n
---------------
Messages: 5种类型的发送消息功能包括:单人单条,单人多条,多人单条,多人多条,转发消息:多人同一条消息\n
Files: 5种类型的发送文件功能包括:单人单个,单人多个,多人单个,多人多个,转发文件:多人同一个文件\n
Call: 给某个好友打视频或语音电话\n
----------------------------------
函数:\n
函数为上述模块内的所有方法\n
--------------------------------------
使用该pywechat时,你可以导入模块,使用模块内的方法:\n
```
from pywechat.WechatAuto import Messages
Messages.send_messages_to_friend()
```
或者直接导入与方法名一致的函数\n
```
from pywechat import send_messages_to_friend
send_messages_to_friend()
```
或者将模块重命名后,使用别名.函数名的方式\n
```
from pywechat import WechatAuto as wechat
wechat.send_messages_to_friend()来进行使用
```
'''

#########################################依赖环境#####################################
import re
import time
import pyautogui
from warnings import warn
from .Warnings import LongTextWarning
from .WechatTools import Tools
from .WinSettings import Systemsettings
from .Errors import EmptyFileError
from .Errors import EmptyFolderError
from .Errors import NotFileError
from .Errors import NotFolderError
from .Errors import CantSendEmptyMessageError
from .Uielements import (Main_window,SideBar,Independent_window,Buttons,
Edits,Texts,TabItems,Lists,Panes,Windows,CheckBoxes,MenuItems,Menus)
#######################################################################################
Main_window=Main_window()#主界面UI
SideBar=SideBar()#侧边栏UI
Independent_window=Independent_window()#独立主界面UI
Buttons=Buttons()#所有Button类型UI
Edits=Edits()#所有Edit类型UI
Texts=Texts()#所有Text类型UI
TabItems=TabItems()#所有TabIem类型UI
Lists=Lists()#所有列表类型UI
Panes=Panes()#所有Pane类型UI
Windows=Windows()#所有Window类型UI
CheckBoxes=CheckBoxes()#所有CheckBox类型UI
MenuItems=MenuItems()#所有MenuItem类型UI
Menus=Menus()#所有Menu类型UI
pyautogui.FAILSAFE=False#防止鼠标在屏幕边缘处造成的误触

class Messages():
    @staticmethod
    def send_message_to_friend(friend:str,message:str,delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用于给单个好友或群聊发送单条信息\n
        Args:
            friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
            message:\t待发送消息。格式:message="消息"\n
            weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
            delay:\t发送单条消息延迟,单位:秒/s,默认0.2s。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if len(message)==0:
            raise CantSendEmptyMessageError
        #先使用open_dialog_window打开对话框
        chat,main_window=Tools.open_dialog_window(friend=friend,weixin_path=weixin_path,is_maximize=is_maximize)
        if is_maximize:
            main_window.maximize()
        chat.click_input()
        #字数超过2000字直接发txt
        if len(message)<2000:
            Systemsettings.copy_text_to_windowsclipboard(message)
            pyautogui.hotkey('ctrl','v')
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        elif len(message)>2000:
            Systemsettings.convert_long_text_to_txt(message)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
        if close_wechat:
            main_window.close()

    @staticmethod
    def send_messages_to_friend(friend:str,messages:list[str],delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用于给单个好友或群聊发送多条信息\n
        Args:
            friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
            message:\t待发送消息列表。格式:message=["发给好友的消息1","发给好友的消息2"]\n
            weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
            delay\t:发送单条消息延迟,单位:秒/s,默认1s。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if not messages:
            raise CantSendEmptyMessageError
        #先使用open_dialog_window打开对话框
        chat,main_window=Tools.open_dialog_window(friend=friend,weixin_path=weixin_path,is_maximize=is_maximize)
        chat.click_input()
        for message in messages:
            if len(message)==0:
                main_window.close()
                raise CantSendEmptyMessageError
            if len(message)<2000:
                Systemsettings.copy_text_to_windowsclipboard(message)
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            elif len(message)>2000:#字数超过200字发送txt文件
                Systemsettings.convert_long_text_to_txt(message)
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
        if close_wechat:
            main_window.close()

    @staticmethod
    def send_messages_to_friends(friends:list[str],messages:list[list[str]],delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用于给多个好友或群聊发送多条信息\n
        Args:
            friends:\t好友或群聊备注列表,格式:firends=["好友1","好友2","好友3"]。\n
            messages:\t待发送消息,格式: message=[[发给好友1的多条消息],[发给好友2的多条消息],[发给好友3的多条信息]]。\n
            weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
            delay:\t发送单条消息延迟,单位:秒/s,默认0.2s。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        注意!messages与friends长度需一致,并且messages内每一个列表顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
        '''
        #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
        Chats=dict(zip(friends,messages))
        main_window=Tools.open_weixin(weixin_path=weixin_path,is_maximize=is_maximize)
        for friend in Chats:
            search=main_window.descendants(**Main_window.Search)[0]
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(1)
            pyautogui.press('enter')
            chat=main_window.descendants(**Main_window.EditArea)[0]
            chat.click_input()
            #字数在50字以内打字发送,超过50字复制粘贴发送,超过2000字直接发word
            for message in Chats.get(friend):
                if len(message)==0:
                    main_window.close()
                    raise CantSendEmptyMessageError
                if len(message)<2000:
                    Systemsettings.copy_text_to_windowsclipboard(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                elif len(message)>2000:
                    Systemsettings.convert_long_text_to_txt(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
        if close_wechat:
            main_window.close()

    @staticmethod
    def send_message_to_friends(friends:list[str],message:list[str],delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用于给每friends中的一个好友或群聊发送message中对应的单条信息\n
        Args:
            friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
            message:\t待发送消息,格式: message=[发给好友1的多条消息,发给好友2的多条消息,发给好友3的多条消息]。\n
            weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        注意!message与friends长度需一致,并且messages内每一条消息顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
        '''
        #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
        Chats=dict(zip(friends,message))
        main_window=Tools.open_weixin(weixin_path=weixin_path,is_maximize=is_maximize)
        for friend in Chats:
            search=main_window.descendants(**Main_window.Search)[0]
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(1)
            pyautogui.press('enter')
            chat=main_window.descendants(**Main_window.EditArea)[0]
            chat.click_input()
            #字数在50字以内打字发送,超过50字复制粘贴发送,超过2000字直接发word
            if len(Chats.get(friend))==0:
                main_window.close()
                raise CantSendEmptyMessageError
            if len(Chats.get(friend))<2000:
                Systemsettings.copy_text_to_windowsclipboard(Chats.get(friend))
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            elif len(Chats.get(friend))>2000:
                Systemsettings.convert_long_text_to_docx(Chats.get(friend))
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
        if close_wechat:
            main_window.close()


        
class Files():
    @staticmethod
    def send_file_to_friend(friend:str,file_path:str,with_messages:bool=False,messages:list=[],messages_first:bool=False,delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用于给单个好友或群聊发送单个文件\n
        Args:
            friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
            file_path:\t待发送文件绝对路径。\n
            with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
            messages:\t与文件一同发送的消息。格式:message=["消息1","消息2","消息3"]\n
            weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
            delay:\t发送单条信息或文件的延迟,单位:秒/s,默认0.2s。\n
            messages_first:\t默认先发送文件后发送消息,messages_first设置为True,先发送消息,后发送文件,\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if len(file_path)==0:
            raise NotFileError
        if not Systemsettings.is_file(file_path):
            raise NotFileError
        if Systemsettings.is_dirctory(file_path):
            raise NotFileError
        if Systemsettings.is_empty_file(file_path):
            raise EmptyFileError
        chat,main_window=Tools.open_dialog_window(friend=friend,weixin_path=weixin_path,is_maximize=is_maximize)
        chat.click_input()
        if with_messages and messages:
            if messages_first:
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)   
            else:
                Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:#超过2000字发txt
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
        else:
            Systemsettings.copy_file_to_windowsclipboard(file_path)
            pyautogui.hotkey("ctrl","v")
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        if close_wechat:
            main_window.close()

        
    @staticmethod
    def send_files_to_friend(friend:str,folder_path:str,with_messages:bool=False,messages:list=[str],messages_first:bool=False,delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用于给单个好友或群聊发送多个文件\n
        Args:
            friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
            folder_path:\t所有待发送文件所处的文件夹的地址。\n
            with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False。\n
            messages:\t与文件一同发送的消息。格式:message=["消息1","消息2","消息3"]\n
            weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认不全屏。\n
            delay:\t发送单条信息或文件的延迟,单位:秒/s,默认0.2s。\n
            messages_first:\t默认先发送文件后发送消息,messages_first设置为True,先发送消息,后发送文件,\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n
        '''
        if len(folder_path)==0:
            raise NotFolderError
        if not Systemsettings.is_dirctory(folder_path):
            raise NotFolderError
        files_in_folder=Systemsettings.get_files_in_folder(folder_path=folder_path)
        if not files_in_folder:
            raise EmptyFolderError
        def send_files():#发送文件单次上限为9,需要9个9个分批发送
            if len(files_in_folder)<=9:
                Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder)
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            else:
                files_num=len(files_in_folder)
                rem=len(files_in_folder)%9
                for i in range(0,files_num,9):
                    if i+9<files_num:
                        Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[i:i+9])
                        pyautogui.hotkey("ctrl","v")
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                if rem:
                    Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[files_num-rem:files_num])
                    pyautogui.hotkey("ctrl","v")
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
        chat,main_window=Tools.open_dialog_window(friend=friend,weixin_path=weixin_path,is_maximize=is_maximize)
        chat.click_input()
        if with_messages and messages:
            if messages_first:
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
                send_files()
            else:
                send_files()
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
        else:
            send_files()      
        if close_wechat:
            main_window.close()

    @staticmethod
    def send_file_to_friends(friends:list[str],file_paths:list[str],with_messages:bool=False,messages:list[list[str]]=[],messages_first:bool=False,delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用于给每个好友或群聊发送单个不同的文件以及多条消息\n
        Args:
            friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
            file_paths:\t待发送文件,格式: file=[发给好友1的单个文件,发给好友2的文件,发给好友3的文件]。\n
            with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
            messages:\t待发送消息,格式:messages=["发给好友1的单条消息","发给好友2的单条消息","发给好友3的单条消息"]\n
            messages_first:\t先发送消息还是先发送文件.默认先发送文件\n
            delay:\t发送单条消息延迟,单位:秒/s,默认0.2s。\n
            weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n
        注意!messages,filepaths与friends长度需一致,并且messages内每一条消息顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
        '''
        for file_path in file_paths:
            file_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',file_path)
            if len(file_path)==0:
                raise NotFileError
            if not Systemsettings.is_file(file_path):
                raise NotFileError
            if Systemsettings.is_dirctory(file_path):
                raise NotFileError
            if Systemsettings.is_empty_file(file_path):
                raise EmptyFileError  
        Files=dict(zip(friends,file_paths))#临时便量用来使用字典来存储好友名称与对于文件路径
        main_window=Tools.open_weixin(weixin_path=weixin_path,is_maximize=is_maximize)
         #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
        if with_messages and messages:
            Chats=dict(zip(friends,messages))
            for friend in Files:
                search=main_window.child_window(**Main_window.Search)
                search.click_input()
                Systemsettings.copy_text_to_windowsclipboard(friend)
                pyautogui.hotkey('ctrl','v')
                time.sleep(0.5)
                pyautogui.press('enter')
                chat=main_window.child_window(title=friend,control_type='Edit')
                chat.click_input()
                if messages_first:
                    messages=Chats.get(friend)
                    for message in messages:
                        if len(message)==0:
                            main_window.close()
                            raise CantSendEmptyMessageError
                        if len(message)<2000:
                            Systemsettings.copy_text_to_windowsclipboard(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                        elif len(message)>2000:
                            Systemsettings.convert_long_text_to_txt(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                    Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                else:
                    Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    messages=Chats.get(friend)
                    for message in messages:
                        if len(message)==0:
                            main_window.close()
                            raise CantSendEmptyMessageError
                        if len(message)<2000:
                            Systemsettings.copy_text_to_windowsclipboard(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                        elif len(message)>2000:
                            Systemsettings.convert_long_text_to_txt(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
        else:
            for friend in Files:
                search=main_window.child_window(**Main_window.Search)
                search.click_input()
                Systemsettings.copy_text_to_windowsclipboard(friend)
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(1)
                pyautogui.press('enter')
                chat=main_window.child_window(title=friend,control_type='Edit')
                chat.click_input()
                Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
        if close_wechat:
            main_window.close()

    @staticmethod
    def send_files_to_friends(friends:list[str],folder_paths:list[str],with_messages:bool=False,messages:list[list[str]]=[],messages_first:bool=False,delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用于给多个好友或群聊发送多个不同或相同的文件夹内的所有文件\n
        Args:
            friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
            folder_paths:\t待发送文件夹路径列表,每个文件夹内可以存放多个文件,格式: FolderPath_list=["","",""]\n
            with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
            message_list:\t待发送消息,格式:message=[[""],[""],[""]]\n
            messages_first:\t先发送消息还是先发送文件,默认先发送文件\n
            delay:\t发送单条消息延迟,单位:秒/s,默认0.2s。\n
            weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        注意! messages,folder_paths与friends长度需一致,并且messages内每一条消息FolderPath_list每一个文件\n
        顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
        '''
        for folder_path in folder_paths:
            folder_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path)
            if len(folder_path)==0:
                raise NotFolderError
            if not Systemsettings.is_dirctory(folder_path):
                raise NotFolderError
        def send_files(folder_path):
            files_in_folder=Systemsettings.get_files_in_folder(folder_path=folder_path)
            if len(files_in_folder)<=9:
                Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder)
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            else:
                files_num=len(files_in_folder)
                rem=len(files_in_folder)%9
                for i in range(0,files_num,9):
                    if i+9<files_num:
                        Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[i:i+9])
                        pyautogui.hotkey("ctrl","v")
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                if rem:
                    Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[files_num-rem:files_num])
                    pyautogui.hotkey("ctrl","v")
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
        folder_paths=[re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path) for folder_path in folder_paths]
        Files=dict(zip(friends,folder_paths))
        main_window=Tools.open_weixin(weixin_path=weixin_path,is_maximize=is_maximize)
        if with_messages and messages:
            Chats=dict(zip(friends,messages))
            for friend in Files:
                search=main_window.child_window(**Main_window.Search)
                search.click_input()
                Systemsettings.copy_text_to_windowsclipboard(friend)
                pyautogui.hotkey('ctrl','v')
                time.sleep(0.5)
                pyautogui.press('enter')
                chat=main_window.child_window(title=friend,control_type='Edit')
                chat.click_input()
                if messages_first:
                    messages=Chats.get(friend)
                    for message in messages:
                        if len(message)==0:
                            main_window.close()
                            raise CantSendEmptyMessageError
                        if len(message)<2000:
                            Systemsettings.copy_text_to_windowsclipboard(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                        elif len(message)>2000:
                            Systemsettings.convert_long_text_to_txt(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                    folder_path=Files.get(friend)
                    send_files(folder_path)
                else:
                    folder_path=Files.get(friend)
                    send_files(folder_path)
                    messages=Chats.get(friend)
                    for message in messages:
                        if len(message)==0:
                            main_window.close()
                            raise CantSendEmptyMessageError
                        if len(message)<2000:
                            Systemsettings.copy_text_to_windowsclipboard(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                        elif len(message)>2000:
                            Systemsettings.convert_long_text_to_txt(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
        else:
            for friend in Files:
                search=main_window.child_window(**Main_window.Search)
                search.click_input()
                Systemsettings.copy_text_to_windowsclipboard(friend)
                time.sleep(0.5)
                pyautogui.hotkey('ctrl','v')
                pyautogui.press('enter')
                chat=main_window.child_window(title=friend,control_type='Edit')
                chat.click_input()
                folder_path=Files.get(friend)
                send_files(folder_path)
        if close_wechat:
            main_window.close()


class Call():
    @staticmethod
    def voice_call(friend:str,weixin_path=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用来给好友拨打语音电话\n
        Args:
            friend:好友备注\n
            weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_dialog_window(friend,weixin_path,is_maximize=is_maximize)[1]  
        Tool_bar=main_window.child_window(**Main_window.ChatToolBar)
        voice_call_button=Tool_bar.children(**Buttons.VoiceCallButton)[0]
        time.sleep(1)
        voice_call_button.click_input()
        if close_wechat:
            main_window.close()

    @staticmethod
    def video_call(friend:str,weixin_path=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用来给好友拨打视频电话\n
        Args:
            friend:\t好友备注.\n
            weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_dialog_window(friend,weixin_path,is_maximize=is_maximize)[1]  
        Tool_bar=main_window.child_window(**Main_window.ChatToolBar)
        voice_call_button=Tool_bar.children(**Buttons.VideoCallButton)[0]
        time.sleep(1)
        voice_call_button.click_input()
        if close_wechat:
            main_window.close()


def send_message_to_friend(friend:str,message:str,delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
    '''
    该函数用于给单个好友或群聊发送单条信息\n
    Args:
        friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
        message:\t待发送消息。格式:message="消息"\n
        weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
        delay:\t发送单条消息延迟,单位:秒/s,默认0.2s。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    if len(message)==0:
        raise CantSendEmptyMessageError
    #先使用open_dialog_window打开对话框
    chat,main_window=Tools.open_dialog_window(friend=friend,weixin_path=weixin_path,is_maximize=is_maximize)
    if is_maximize:
        main_window.maximize()
    chat.click_input()
    #字数超过2000字直接发txt
    if len(message)<2000:
        Systemsettings.copy_text_to_windowsclipboard(message)
        pyautogui.hotkey('ctrl','v')
        time.sleep(delay)
        pyautogui.hotkey('alt','s',_pause=False)
    elif len(message)>2000:
        Systemsettings.convert_long_text_to_txt(message)
        pyautogui.hotkey('ctrl','v',_pause=False)
        time.sleep(delay)
        pyautogui.hotkey('alt','s',_pause=False)
        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
    time.sleep(1)
    if close_wechat:
        main_window.close()

def send_messages_to_friend(friend:str,messages:list[str],delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
    '''
    该函数用于给单个好友或群聊发送多条信息\n
    Args:
        friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
        message:\t待发送消息列表。格式:message=["发给好友的消息1","发给好友的消息2"]\n
        weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
        delay\t:发送单条消息延迟,单位:秒/s,默认1s。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    if not messages:
        raise CantSendEmptyMessageError
    #先使用open_dialog_window打开对话框
    chat,main_window=Tools.open_dialog_window(friend=friend,weixin_path=weixin_path,is_maximize=is_maximize)
    chat.click_input()
    for message in messages:
        if len(message)==0:
            main_window.close()
            raise CantSendEmptyMessageError
        if len(message)<2000:
            Systemsettings.copy_text_to_windowsclipboard(message)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        elif len(message)>2000:#字数超过200字发送txt文件
            Systemsettings.convert_long_text_to_txt(message)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
    if close_wechat:
        main_window.close()

def send_message_to_friends(friends:list[str],message:list[str],delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
    '''
    该函数用于给每friends中的一个好友或群聊发送message中对应的单条信息\n
    Args:
        friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
        message:\t待发送消息,格式: message=[发给好友1的多条消息,发给好友2的多条消息,发给好友3的多条消息]。\n
        weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    注意!message与friends长度需一致,并且messages内每一条消息顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
    '''
    #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
    Chats=dict(zip(friends,message))
    main_window=Tools.open_weixin(weixin_path=weixin_path,is_maximize=is_maximize)
    for friend in Chats:
        search=main_window.descendants(**Main_window.Search)[0]
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(friend)
        pyautogui.hotkey('ctrl','v',_pause=False)
        time.sleep(1)
        pyautogui.press('enter')
        chat=main_window.descendants(**Main_window.EditArea)[0]
        chat.click_input()
        #字数在50字以内打字发送,超过50字复制粘贴发送,超过2000字直接发word
        if len(Chats.get(friend))==0:
            main_window.close()
            raise CantSendEmptyMessageError
        if len(Chats.get(friend))<2000:
            Systemsettings.copy_text_to_windowsclipboard(Chats.get(friend))
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        elif len(Chats.get(friend))>2000:
            Systemsettings.convert_long_text_to_docx(Chats.get(friend))
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
    if close_wechat:
        main_window.close()

def send_messages_to_friends(friends:list[str],messages:list[list[str]],delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
    '''
    该函数用于给多个好友或群聊发送多条信息\n
    Args:
        friends:\t好友或群聊备注列表,格式:firends=["好友1","好友2","好友3"]。\n
        messages:\t待发送消息,格式: message=[[发给好友1的多条消息],[发给好友2的多条消息],[发给好友3的多条信息]]。\n
        weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
        delay:\t发送单条消息延迟,单位:秒/s,默认0.2s。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    注意!messages与friends长度需一致,并且messages内每一个列表顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
    '''
    #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
    Chats=dict(zip(friends,messages))
    main_window=Tools.open_weixin(weixin_path=weixin_path,is_maximize=is_maximize)
    for friend in Chats:
        search=main_window.descendants(**Main_window.Search)[0]
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(friend)
        pyautogui.hotkey('ctrl','v',_pause=False)
        time.sleep(1)
        pyautogui.press('enter')
        chat=main_window.descendants(**Main_window.EditArea)[0]
        chat.click_input()
        #字数在50字以内打字发送,超过50字复制粘贴发送,超过2000字直接发word
        for message in Chats.get(friend):
            if len(message)==0:
                main_window.close()
                raise CantSendEmptyMessageError
            if len(message)<2000:
                Systemsettings.copy_text_to_windowsclipboard(message)
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            elif len(message)>2000:
                Systemsettings.convert_long_text_to_txt(message)
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
    if close_wechat:
        main_window.close()

        
def send_file_to_friend(friend:str,file_path:str,with_messages:bool=False,messages:list=[],messages_first:bool=False,delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
    '''
    该函数用于给单个好友或群聊发送单个文件\n
    Args:
        friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
        file_path:\t待发送文件绝对路径。\n
        with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
        messages:\t与文件一同发送的消息。格式:message=["消息1","消息2","消息3"]\n
        weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
        delay:\t发送单条信息或文件的延迟,单位:秒/s,默认0.2s。\n
        messages_first:\t默认先发送文件后发送消息,messages_first设置为True,先发送消息,后发送文件,\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    if len(file_path)==0:
        raise NotFileError
    if not Systemsettings.is_file(file_path):
        raise NotFileError
    if Systemsettings.is_dirctory(file_path):
        raise NotFileError
    if Systemsettings.is_empty_file(file_path):
        raise EmptyFileError
    chat,main_window=Tools.open_dialog_window(friend=friend,weixin_path=weixin_path,is_maximize=is_maximize)
    chat.click_input()
    if with_messages and messages:
        if messages_first:
            for message in messages:
                if len(message)==0:
                    main_window.close()
                    raise CantSendEmptyMessageError
                if len(message)<2000:
                    Systemsettings.copy_text_to_windowsclipboard(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                elif len(message)>2000:
                    Systemsettings.convert_long_text_to_txt(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
            Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
            pyautogui.hotkey("ctrl","v")
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)   
        else:
            Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
            pyautogui.hotkey("ctrl","v")
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
            for message in messages:
                if len(message)==0:
                    main_window.close()
                    raise CantSendEmptyMessageError
                if len(message)<2000:
                    Systemsettings.copy_text_to_windowsclipboard(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                elif len(message)>2000:#超过2000字发txt
                    Systemsettings.convert_long_text_to_txt(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
    else:
        Systemsettings.copy_file_to_windowsclipboard(file_path)
        pyautogui.hotkey("ctrl","v")
        time.sleep(delay)
        pyautogui.hotkey('alt','s',_pause=False)
    if close_wechat:
        main_window.close()

def send_files_to_friend(friend:str,folder_path:str,with_messages:bool=False,messages:list=[str],messages_first:bool=False,delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
    '''
    该函数用于给单个好友或群聊发送多个文件\n
    Args:
        friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
        folder_path:\t所有待发送文件所处的文件夹的地址。\n
        with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False。\n
        messages:\t与文件一同发送的消息。格式:message=["消息1","消息2","消息3"]\n
        weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认不全屏。\n
        delay:\t发送单条信息或文件的延迟,单位:秒/s,默认0.2s。\n
        messages_first:\t默认先发送文件后发送消息,messages_first设置为True,先发送消息,后发送文件,\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
    '''
    if len(folder_path)==0:
        raise NotFolderError
    if not Systemsettings.is_dirctory(folder_path):
        raise NotFolderError
    files_in_folder=Systemsettings.get_files_in_folder(folder_path=folder_path)
    if not files_in_folder:
        raise EmptyFolderError
    def send_files():
        if len(files_in_folder)<=9:
            Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder)
            pyautogui.hotkey("ctrl","v")
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        else:
            files_num=len(files_in_folder)
            rem=len(files_in_folder)%9
            for i in range(0,files_num,9):
                if i+9<files_num:
                    Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[i:i+9])
                    pyautogui.hotkey("ctrl","v")
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
            if rem:
                Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[files_num-rem:files_num])
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
    chat,main_window=Tools.open_dialog_window(friend=friend,weixin_path=weixin_path,is_maximize=is_maximize)
    chat.click_input()
    if with_messages and messages:
        if messages_first:
            for message in messages:
                if len(message)==0:
                    main_window.close()
                    raise CantSendEmptyMessageError
                if len(message)<2000:
                    Systemsettings.copy_text_to_windowsclipboard(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                elif len(message)>2000:
                    Systemsettings.convert_long_text_to_txt(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
            send_files()
        else:
            send_files()
            for message in messages:
                if len(message)==0:
                    main_window.close()
                    raise CantSendEmptyMessageError
                if len(message)<2000:
                    Systemsettings.copy_text_to_windowsclipboard(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                elif len(message)>2000:
                    Systemsettings.convert_long_text_to_txt(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
    else:
        send_files()       
    if close_wechat:
        main_window.close()

def send_file_to_friends(friends:list[str],file_paths:list[str],with_messages:bool=False,messages:list[list[str]]=[],messages_first:bool=False,delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
    '''
    该函数用于给每个好友或群聊发送单个不同的文件以及多条消息\n
    Args:
        friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
        file_paths:\t待发送文件,格式: file=[发给好友1的单个文件,发给好友2的文件,发给好友3的文件]。\n
        with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
        messages:\t待发送消息,格式:messages=["发给好友1的单条消息","发给好友2的单条消息","发给好友3的单条消息"]\n
        messages_first:\t先发送消息还是先发送文件.默认先发送文件\n
        delay:\t发送单条消息延迟,单位:秒/s,默认0.2s。\n
        weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
    注意!messages,filepaths与friends长度需一致,并且messages内每一条消息顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
    '''
    for file_path in file_paths:
        file_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',file_path)
        if len(file_path)==0:
            raise NotFileError
        if not Systemsettings.is_file(file_path):
            raise NotFileError
        if Systemsettings.is_dirctory(file_path):
            raise NotFileError
        if Systemsettings.is_empty_file(file_path):
            raise EmptyFileError  
    Files=dict(zip(friends,file_paths))#临时便量用来使用字典来存储好友名称与对于文件路径
    main_window=Tools.open_weixin(weixin_path=weixin_path,is_maximize=is_maximize)
        #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
    if with_messages and messages:
        Chats=dict(zip(friends,messages))
        for friend in Files:
            search=main_window.child_window(**Main_window.Search)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.5)
            pyautogui.press('enter')
            chat=main_window.child_window(title=friend,control_type='Edit')
            chat.click_input()
            if messages_first:
                messages=Chats.get(friend)
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            else:
                Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                messages=Chats.get(friend)
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
    else:
        for friend in Files:
            search=main_window.child_window(**Main_window.Search)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(1)
            pyautogui.press('enter')
            chat=main_window.child_window(title=friend,control_type='Edit')
            chat.click_input()
            Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
    if close_wechat:
        main_window.close()

def send_files_to_friends(friends:list[str],folder_paths:list[str],with_messages:bool=False,messages:list[list[str]]=[],messages_first:bool=False,delay:float=0.2,weixin_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
    '''
    该函数用于给多个好友或群聊发送多个不同或相同的文件夹内的所有文件\n
    Args:
        friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
        folder_paths:\t待发送文件夹路径列表,每个文件夹内可以存放多个文件,格式: FolderPath_list=["","",""]\n
        with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
        message_list:\t待发送消息,格式:message=[[""],[""],[""]]\n
        messages_first:\t先发送消息还是先发送文件,默认先发送文件\n
        delay:\t发送单条消息延迟,单位:秒/s,默认0.2s。\n
        weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    注意! messages,folder_paths与friends长度需一致,并且messages内每一条消息FolderPath_list每一个文件\n
    顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
    '''
    for folder_path in folder_paths:
        folder_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path)
        if len(folder_path)==0:
            raise NotFolderError
        if not Systemsettings.is_dirctory(folder_path):
            raise NotFolderError
    def send_files(folder_path):
        files_in_folder=Systemsettings.get_files_in_folder(folder_path=folder_path)
        if len(files_in_folder)<=9:
            Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder)
            pyautogui.hotkey("ctrl","v")
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        else:
            files_num=len(files_in_folder)
            rem=len(files_in_folder)%9
            for i in range(0,files_num,9):
                if i+9<files_num:
                    Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[i:i+9])
                    pyautogui.hotkey("ctrl","v")
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
            if rem:
                Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[files_num-rem:files_num])
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
    folder_paths=[re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path) for folder_path in folder_paths]
    Files=dict(zip(friends,folder_paths))
    main_window=Tools.open_weixin(weixin_path=weixin_path,is_maximize=is_maximize)
    if with_messages and messages:
        Chats=dict(zip(friends,messages))
        for friend in Files:
            search=main_window.child_window(**Main_window.Search)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.5)
            pyautogui.press('enter')
            chat=main_window.child_window(title=friend,control_type='Edit')
            chat.click_input()
            if messages_first:
                messages=Chats.get(friend)
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                folder_path=Files.get(friend)
                send_files(folder_path)
            else:
                folder_path=Files.get(friend)
                send_files(folder_path)
                messages=Chats.get(friend)
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
    else:
        for friend in Files:
            search=main_window.child_window(**Main_window.Search)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            time.sleep(0.5)
            pyautogui.hotkey('ctrl','v')
            pyautogui.press('enter')
            chat=main_window.child_window(title=friend,control_type='Edit')
            chat.click_input()
            folder_path=Files.get(friend)
            send_files(folder_path)
    if close_wechat:
        main_window.close()


def voice_call(friend:str,weixin_path=None,is_maximize:bool=False,close_wechat:bool=True):
    '''
    该函数用来给好友拨打语音电话\n
    Args:
        friend:好友备注\n
        weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_dialog_window(friend,weixin_path,is_maximize=is_maximize)[1]  
    Tool_bar=main_window.child_window(**Main_window.ChatToolBar)
    voice_call_button=Tool_bar.children(**Buttons.VoiceCallButton)[0]
    time.sleep(1)
    voice_call_button.click_input()
    if close_wechat:
        main_window.close()

def video_call(friend:str,weixin_path=None,is_maximize:bool=False,close_wechat:bool=True):
    '''
    该函数用来给好友拨打视频电话\n
    Args:
        friend:\t好友备注.\n
        weixin_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认不全屏。\n\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_dialog_window(friend,weixin_path,is_maximize=is_maximize)[1]  
    Tool_bar=main_window.child_window(**Main_window.ChatToolBar)
    voice_call_button=Tool_bar.children(**Buttons.VideoCallButton)[0]
    time.sleep(1)
    voice_call_button.click_input()
    if close_wechat:
        main_window.close()

