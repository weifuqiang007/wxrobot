
'''
定时模块schedule:可以按照当天指定时刻或一段时间后运行指定函数或方法
---
使用方法:\n
在指定的一段时间后执行\n
```
from pywechat.Clock import schedule
schedule(funcs=[func1,func2],parameters=[{func1的参数字典},{func2的参数字典},waitPeriods=['20s','20min']]).execute()
```
在指定的时刻执行\n
```
from pywechat.clock import schedule\n
schedule(funcs=[func1,func2],parameters=[{func1的参数字典},{func2的参数字典},Time=['08:31:14','08:45']]).execute()
```
注:时刻可以精确到秒,若某个函数无需任何参数,那你在传入其对印的参数字典时,传入一个空字典即可\n
若给定的时间戳与当前时间戳之差为负数,定时任务将会立即执行\n

定时模块schtasks:可以按照当天指定时间运行指定python代码
----
使用方法:\n
在指定时刻执行\n
```
from pywechat.Clock import scntasks
scntasks.create_task(taskname='定时任务',start_time='08:31:14',pyfile_path='python文件地址')
```
注:运行上述代码后,名为定时任务的schtask将会被添加到windows系统下的定时任务中,并在指定时刻运行传入的python文件内的代码\n
若你不想传入一个python文件的路径,可以直接传入python代码的长字符串形式,例如:
```
from pywechat.Clock import scntasks
code='这是一段python代码'
scntasks.create(taskname='定时任务',start_time='08:31:14',code=code)
'''
import os
import sys
import re
import asyncio
import subprocess
from  datetime import datetime
from pyweixin.Errors import TaskNotBuildError
from pyweixin.WinSettings import Systemsettings
from pyweixin.WechatTools import match_duration
class schedule:#创建定时任务
    '''
    funcs:所有需要定时执行的函数名列表,注意函数名的类型为函数\n
    不是类型为字符串的函数的名字!\n
    parameters:所有需要定时执行的函数的参数\n
    Times:各个函数定时执行的时间点,Times=['08:31','08:45:54']可精确到秒\n
    waitPeriod:各个函数在指定的一段时间执行的等待时长,waitPeriod=['20s','1h']分别在20s后和1h后执行两个函数、\n
    比如:有两个函数分别为,test1(num:int,string:str),test2(num:int,string:str)\n
    那么传入funcs和parameters时应为:funcs=[test1,test2]\n
    parameters=[{'num':2,'string':'test1'},{{'num':3,'string':'test2'}}]\n
    这个类通过构建协程池来创建定时任务\n
    注意:运行代码后请勿关闭代码编辑器,否则定时任务无法完成
    --
    '''
    def __init__(self,funcs:list,parameters:list[dict],Times:list[str]=[],waitPeriods:list[str]=[]):
        self.Times=Times#指定时间点，'08:31','08:45:54'可精确到秒
        self.waitPeriods=waitPeriods#指定时长，20s,1min,1h
        self.funcs=funcs#所有需要定时执行的函数名
        self.parameters=parameters##所有需要定时执行的函数的参数[{},{}]，

    def calculate_time_difference(self,target_time_string):
        colons=re.findall(r':',target_time_string)
        current_time = datetime.now()
        target_date = current_time.date()  # 获取当前日期
        if len(colons)==2:
            target_time_format="%H:%M:%S"
        elif len(colons)==1:
            target_time_format="%H:%M"
        else:
            raise ValueError('输入的时间戳有误!请重新输入!')
        target_time = datetime.combine(target_date, datetime.strptime(target_time_string, target_time_format).time())
        # 计算时间差
        time_difference = target_time - current_time
        hours_difference = time_difference.seconds // 3600  # 整除3600得到小时数
        minutes_remainder = time_difference.seconds % 3600  # 求余得到剩余的秒数，再转换为分钟
        minutes_difference = minutes_remainder // 60  # 整除60得到分钟数
        seconds_difference = minutes_remainder % 60  # 再次求余得到秒数
        print(f"时间差：{hours_difference}小时 {minutes_difference}分钟 {seconds_difference}秒")
        time_difference=time_difference.total_seconds()
        return  time_difference
    
    async def async_task(self,func,parameter,Time:str=None,waitPeriod:str=None):
        if Time:
            print(f"函数{func.__name__}将会在{Time}时执行")
            await asyncio.sleep(self.calculate_time_difference(Time))
            result=func(**parameter)
            return result
        if waitPeriod:
            print(f"函数{func.__name__}将会在{waitPeriod}后执行")
            waitPeriod=match_duration(waitPeriod)
            await asyncio.sleep(waitPeriod)
            result=func(**parameter)
            return result
    async def main(self):
        #构建协程池实现异步定时任务
        self.tasks=[]
        if self.waitPeriods:
            for func,parameter,waitPeriod in zip(self.funcs,self.parameters,self.waitPeriods):
                self.tasks.append(self.async_task(func,parameter,waitPeriod=waitPeriod))
            results=await asyncio.gather(*self.tasks)
            return results
        if self.Times:
            for func,parameter,time in zip(self.funcs,self.parameters,self.Times):
                self.tasks.append(self.async_task(func,parameter,Time=time))
            results=await asyncio.gather(*self.tasks)
            return results
    def execute(self):
        #运行所有任务
        Systemsettings.open_listening_mode()
        results=asyncio.run(self.main())
        Systemsettings.close_listening_mode()
        return results


class schtasks():
    '''
    使用windows系统下的schtasks命令实现定时操作相较于schedule可以关闭代码编辑器
    --
    '''
    @staticmethod
    def code_to_py(code:str):
        '''将字符串代码写入py文件到当前目录下
        Args:
            code:字符串代码
        '''
        with open('code_to_be_executed.py','w',encoding='utf-8') as py:
            py.write(code)
        pyfile_path=os.path.abspath(os.path.join(os.getcwd(),'exec.py'))
        return pyfile_path
    @staticmethod
    def create_task(taskname:str,start_time:str,code:str=None,pyfile_path:str=None):
        '''
        创建一个Windows系统下的schtasks任务,该任务将在当天指定的start_time\n
        执行传入的python代码或python脚本\n
        Args:
            taskname:\tschtasks命令名称
            start_ime:\t执行任务的时间
            code:\tpython代码类型为长字符串
            pyfile_path:\tpython代码路径

        注意:pyfile_path与code二者有其一即可,若二者都传入,优先使用pyfile_path的py代码
        ----
        '''
        if not pyfile_path:
            pyfile_path=schtasks.code_to_py(code)
        # 创建一个schtasks命令来创建计划任务
        command=f'{sys.executable} {pyfile_path}'
        schtasks_command = (
            f'schtasks /create /tn {taskname} '
            f'/tr "{command}" /sc ONCE /st {start_time} /f'
        )
        subprocess.run(schtasks_command,text=True,shell=True)

    @staticmethod
    def change_task(taskname:str,start_time:str,code:str=None,pyfile_path:str=None):
        '''
        通过taskname修改一个已经设定的windows系统下的schtasks任务\n
        Args:
            taskname:\t已经设定的schtasks任务的名称
            start_ime:\t修改后执行任务的时间
            code:\t需要替换的python代码类型为长字符串
            pyfile_path:\t需要替换的py文件路径
        
        注意:pyfile_path与code二者有其一即可,若二者都传入,优先使用pyfile_path的py代码
        ----
        '''
        tasks=schtasks.get_all_created_tasks()
        if taskname in tasks.keys():
            if code:
                if not pyfile_path:
                    pyfile_path=schtasks.code_to_py(code)
                command=f'{sys.executable} {pyfile_path}'
                schtasks_command= (
                    f'schtasks /change /tn {taskname} '
                    f'/tr "{command}" /st {start_time} '
                )
                subprocess.run(schtasks_command,text=True,input='\n')
            else:
                schtasks_command=(
                    f'schtasks /change /tn {taskname} /st {start_time} '
                )
                subprocess.run(schtasks_command,text=True,input='\n')
        else:
            raise TaskNotBuildError(f'你还未创建过名为{taskname}的定时任务！')
        
    @staticmethod
    def cancel_task(taskname):
        '''
        通过已经设定的schtasks的taskname取消该任务\n

        Args:
            taskname:\t已经设定的schtasks任务的名称
        
        '''
        schtasks_command=(f'schtasks /delete /tn {taskname} /f')
        pyfile_path=os.path.abspath(os.path.join(os.getcwd(),'exec.py'))
        tasks=schtasks.get_all_created_tasks()
        if taskname in tasks.keys():
            if os.path.exists(pyfile_path):
                os.remove(pyfile_path)
            subprocess.run(schtasks_command)
        else:
            raise TaskNotBuildError(f'你还未创建过名为{taskname}的定时任务！')
    @staticmethod
    def get_all_created_tasks():
        '''
        获取所有已建立的schtasks任务名称与时间\n
        返回值为任务名称与执行时间构成的字典\n
        '''
        schtasks_command='schtasks /query /v /fo list'
        process=subprocess.run(schtasks_command,stdout=subprocess.PIPE,encoding='gbk')
        result=process.stdout
        tasknames=re.findall(r'任务名:(.*?)(\n|$)',result)
        tasknames=[name[0].strip() for name in tasknames]
        tasknames=[name.replace('\\','') for name in tasknames]
        start_times=re.findall(r'开始时间:(.*?)(\n|$)',result)
        start_times=[name[0].strip() for name in start_times]
        start_times=[name.replace('\\','') for name in start_times]
        tasks=dict(zip(tasknames,start_times))
        return tasks


