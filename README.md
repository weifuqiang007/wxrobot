# 微信后端自动化系统

基于 pywechat 的微信自动化后端服务，提供消息自动回复、群成员欢迎和定时新闻推送功能。

## 功能特性

### 🤖 自动回复功能
- 自动回复用户发送的消息（默认回复："收到！"）
- 支持私聊和群聊消息处理
- 群聊支持@机器人触发回复
- 可自定义回复内容

### 👋 群成员欢迎
- 自动检测新成员加入群聊
- 发送个性化欢迎消息
- 支持自定义欢迎消息模板

### 📰 定时新闻推送
- 每日定时向指定群聊推送新闻
- 支持多个群聊同时推送
- 可自定义推送时间
- 集成天气信息和每日贴士
- 支持接入真实新闻API

### 🔧 管理功能
- 命令行管理工具
- Web API接口
- 配置文件管理
- 服务状态监控

## 系统架构

```
wechat_backend/
├── __init__.py          # 包初始化
├── app.py              # 主应用程序
├── wechat_service.py   # 微信服务封装
├── news_service.py     # 新闻服务
├── config.py           # 配置管理
├── cli.py              # 命令行工具
├── api.py              # Web API接口
├── requirements.txt    # 依赖包列表
└── README.md          # 项目文档
```

## 安装部署

### 1. 环境要求
- Python 3.8+
- Windows 操作系统
- 微信PC版客户端

### 2. 安装依赖
```bash
cd wechat_backend
pip install -r requirements.txt
```

### 3. 安装pywechat
```bash
# 如果还未安装pywechat
cd ..
pip install -e .
```

## 使用方法

### 命令行方式

#### 启动服务
```bash
python -m wechat_backend.cli start
```

#### 配置管理
```bash
# 添加新闻推送群
python -m wechat_backend.cli add-group "测试群"

# 设置推送时间
python -m wechat_backend.cli set-time "09:00"

# 查看配置
python -m wechat_backend.cli show-config

# 测试新闻获取
python -m wechat_backend.cli test-news

# 发送测试消息
python -m wechat_backend.cli send-test "好友名称" "测试消息"
```

#### 更多命令
```bash
# 查看所有可用命令
python -m wechat_backend.cli --help

# 列出新闻推送群
python -m wechat_backend.cli list-groups

# 移除新闻推送群
python -m wechat_backend.cli remove-group "群名称"

# 设置微信路径
python -m wechat_backend.cli set-wechat-path "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe"

# 设置默认回复消息
python -m wechat_backend.cli set-reply "您好，我已收到您的消息！"
```

### Web API方式

#### 启动API服务
```bash
python -m wechat_backend.api
```

默认服务地址：http://127.0.0.1:5000

#### API接口文档

**服务状态**
```http
GET /api/status
```

**微信服务控制**
```http
# 启动微信服务
POST /api/wechat/start

# 停止微信服务
POST /api/wechat/stop
```

**消息发送**
```http
POST /api/message/send
Content-Type: application/json

{
  "friend_name": "好友名称",
  "message": "消息内容"
}
```

**新闻推送管理**
```http
# 获取新闻推送群列表
GET /api/news/groups

# 添加新闻推送群
POST /api/news/groups
Content-Type: application/json

{
  "group_name": "群名称"
}

# 移除新闻推送群
DELETE /api/news/groups/{group_name}

# 设置推送时间
PUT /api/news/time
Content-Type: application/json

{
  "time": "09:00"
}

# 测试新闻获取
GET /api/news/test
```

**配置管理**
```http
# 获取所有配置
GET /api/config

# 更新微信配置
PUT /api/config/wechat
Content-Type: application/json

{
  "wechat_path": "C:\\Program Files\\Tencent\\WeChat\\WeChat.exe",
  "is_maximize": true
}

# 更新回复配置
PUT /api/config/reply
Content-Type: application/json

{
  "default_reply": "收到您的消息！",
  "welcome_message_template": "欢迎{name}加入我们的群聊！"
}
```

### Python代码方式

```python
from wechat_backend.app import WechatBackendApp

# 创建应用实例
app = WechatBackendApp()

# 添加新闻推送群
app.add_news_group("测试群")
app.add_news_group("工作群")

# 设置推送时间
app.set_news_time("09:00")

# 启动服务
app.start()
```

## 配置文件

系统会自动创建 `config.json` 配置文件：

```json
{
  "wechat": {
    "wechat_path": null,
    "is_maximize": true,
    "close_wechat": false
  },
  "news": {
    "enabled": true,
    "push_time": "09:00",
    "target_groups": [],
    "news_api_url": null,
    "news_api_key": null
  },
  "reply": {
    "enabled": true,
    "default_reply": "收到！",
    "welcome_message_template": "欢迎{name}用户加入群聊！",
    "reply_to_private": true,
    "reply_to_group_at_only": true
  }
}
```

## 扩展开发

### 接入真实新闻API

修改 `news_service.py` 中的 `_fetch_real_news` 方法，接入您选择的新闻API：

```python
# 在配置中设置API信息
config_manager.update_news_config(
    news_api_url="https://api.example.com/news",
    news_api_key="your_api_key"
)
```

### 自定义消息处理逻辑

修改 `wechat_service.py` 中的 `_handle_message` 方法，实现自定义的消息处理逻辑：

```python
def _handle_message(self, friend_name: str, friend_type: str, content: str, message_type: str):
    # 在这里添加您的自定义逻辑
    # 例如：接入RAG系统、调用AI模型等
    pass
```

### 添加新的API接口

在 `api.py` 中添加新的路由和处理函数：

```python
@self.app.route('/api/custom/endpoint', methods=['POST'])
def custom_endpoint():
    # 自定义API逻辑
    pass
```

## 注意事项

1. **微信版本兼容性**：确保使用的微信PC版本与pywechat兼容
2. **权限设置**：运行时可能需要管理员权限
3. **防火墙设置**：如使用Web API，确保端口未被防火墙阻止
4. **稳定性**：长时间运行建议配置日志轮转和异常重启机制
5. **安全性**：生产环境中请修改默认配置，设置访问控制

## 故障排除

### 常见问题

1. **微信无法启动**
   - 检查微信路径配置
   - 确认微信客户端已安装
   - 尝试手动启动微信

2. **消息发送失败**
   - 检查好友/群名称是否正确
   - 确认微信已登录
   - 查看日志文件获取详细错误信息

3. **新闻推送不工作**
   - 检查推送时间设置
   - 确认目标群聊已添加
   - 验证系统时间是否正确

### 日志查看

系统日志保存在 `wechat_backend.log` 文件中，可以通过查看日志来诊断问题：

```bash
tail -f wechat_backend.log
```

## 开发计划

- [ ] 支持更多消息类型（图片、文件等）
- [ ] 添加数据库支持
- [ ] 实现用户权限管理
- [ ] 支持多微信账号
- [ ] 添加监控和告警功能
- [ ] 集成更多第三方服务

## 许可证

本项目基于原pywechat项目的许可证发布。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！