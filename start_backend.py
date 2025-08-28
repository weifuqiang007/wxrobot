#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端服务启动脚本
用于从前端启动后端API服务
"""

import subprocess
import sys
import os
import time
import requests

def check_backend_running():
    """检查后端服务是否已经在运行"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def start_backend_service():
    """启动后端服务"""
    try:
        # 检查是否已经在运行
        if check_backend_running():
            print("后端服务已经在运行中")
            return True
        
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        api_file = os.path.join(current_dir, 'api_restructured.py')
        
        if not os.path.exists(api_file):
            print(f"错误: 找不到API文件 {api_file}")
            return False
        
        print("正在启动后端服务...")
        
        # 启动后端服务（非阻塞方式）
        process = subprocess.Popen(
            [sys.executable, api_file],
            cwd=current_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        # 等待服务启动
        max_wait = 30  # 最多等待30秒
        wait_time = 0
        
        while wait_time < max_wait:
            if check_backend_running():
                print("后端服务启动成功！")
                return True
            
            time.sleep(1)
            wait_time += 1
            print(f"等待服务启动... ({wait_time}/{max_wait})")
        
        print("后端服务启动超时")
        return False
        
    except Exception as e:
        print(f"启动后端服务失败: {str(e)}")
        return False

if __name__ == '__main__':
    success = start_backend_service()
    sys.exit(0 if success else 1)