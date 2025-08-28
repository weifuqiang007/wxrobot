# 后端服务启动说明

## 自动启动（推荐）

1. 在前端仪表盘页面，如果后端服务显示为"离线"状态
2. 点击"启动服务"按钮
3. 系统会自动尝试启动后端服务
4. 等待30秒左右，服务状态会自动更新

## 手动启动

### 方法一：使用启动脚本

```bash
# 在项目根目录下执行
python start_backend.py
```

### 方法二：直接启动API服务

```bash
# 在项目根目录下执行
python api_restructured.py
```

### 方法三：使用命令行

1. 打开命令提示符或PowerShell
2. 切换到项目目录：
   ```bash
   cd G:\wxrobot\myself
   ```
3. 安装依赖（如果还没安装）：
   ```bash
   pip install -r requirements.txt
   ```
4. 启动服务：
   ```bash
   python api_restructured.py
   ```

## 验证服务状态

服务启动后，可以通过以下方式验证：

1. **浏览器访问**：打开 http://localhost:5000/api/health
2. **命令行测试**：
   ```bash
   curl http://localhost:5000/api/health
   ```
3. **前端页面**：在仪表盘点击"刷新"按钮检查状态

## 常见问题

### 1. 端口被占用
如果5000端口被占用，可以：
- 查找占用进程：`netstat -ano | findstr :5000`
- 结束占用进程或修改配置文件中的端口

### 2. 依赖包缺失
如果出现模块导入错误：
```bash
pip install -r requirements.txt
```

### 3. 权限问题
在Windows上可能需要以管理员身份运行命令提示符

### 4. Python环境问题
确保使用正确的Python版本（建议Python 3.8+）：
```bash
python --version
```

## 服务配置

后端服务默认配置：
- **端口**：5000
- **主机**：localhost
- **调试模式**：开启
- **线程模式**：开启

如需修改配置，请编辑 `api_restructured.py` 文件中的相关参数。