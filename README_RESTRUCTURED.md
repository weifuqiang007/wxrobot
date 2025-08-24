# 微信后端自动化系统 - 重构版

## 🎯 项目概述

本项目是微信后端自动化系统的重构版本，采用现代化的MVC架构模式，实现了清晰的代码组织和职责分离。相比原版本，重构版具有更好的可维护性、可扩展性和可测试性。

## 🏗️ 架构特点

### ✨ 核心优势

- **🔧 MVC架构**: 采用经典的Model-View-Controller模式
- **📦 分层设计**: Routes → Controllers → Services → DAO → Models
- **🔌 模块化**: 每个功能模块独立，便于维护和扩展
- **🛡️ 错误处理**: 统一的错误处理和响应格式
- **📝 日志管理**: 完善的日志记录和管理
- **⚡ 性能优化**: 单例模式、连接池等优化策略

### 📁 目录结构

```
wechat_backend/
├── routes/                    # 🛣️ 路由层 - API端点定义
│   ├── health_routes.py       # 健康检查
│   ├── status_routes.py       # 状态管理
│   ├── config_routes.py       # 配置管理
│   ├── message_routes.py      # 消息管理
│   ├── news_routes.py         # 新闻管理
│   └── contact_routes.py      # 联系人管理
├── controllers/               # 🎮 控制层 - 业务逻辑控制
│   ├── status_controller.py   # 状态控制器
│   ├── config_controller.py   # 配置控制器
│   ├── message_controller.py  # 消息控制器
│   ├── news_controller.py     # 新闻控制器
│   └── contact_controller.py  # 联系人控制器
├── services/                  # ⚙️ 服务层 - 核心业务逻辑
│   └── app_service.py         # 应用服务
├── dao/                       # 💾 数据访问层 - 数据操作
│   ├── config_dao.py          # 配置数据访问
│   └── wechat_dao.py          # 微信数据访问
├── api_restructured.py        # 🚀 重构后的主API文件
├── start_restructured.py      # 🎯 重构版启动脚本
├── ARCHITECTURE.md            # 📊 架构文档
└── README_RESTRUCTURED.md     # 📖 重构版说明文档
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 检查配置文件
# 确保 config.json 存在且配置正确
```

### 2. 启动服务

#### 方式一：使用启动脚本（推荐）

```bash
python start_restructured.py
```

启动脚本提供了友好的菜单界面：
- 🚀 启动API服务器（生产/调试模式）
- 🔍 系统检查
- 📖 查看API文档
- ⚙️ 查看配置
- 📊 查看架构文档

#### 方式二：直接启动API

```bash
python api_restructured.py
```

### 3. 访问服务

启动成功后，可以通过以下地址访问：

- **API文档**: http://127.0.0.1:5000/api/docs
- **健康检查**: http://127.0.0.1:5000/api/health
- **服务状态**: http://127.0.0.1:5000/api/status

## 📚 API文档

### 🏥 健康检查

```http
GET /api/health
```

**响应示例：**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "2.0.0",
  "uptime": "1 hour 30 minutes"
}
```

### 📊 服务状态

```http
GET /api/status
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "wechat_connected": true,
    "auto_reply_enabled": true,
    "news_push_enabled": true,
    "last_activity": "2024-01-01T12:00:00"
  }
}
```

### ⚙️ 配置管理

#### 获取配置
```http
GET /api/config
```

#### 更新配置
```http
POST /api/config
Content-Type: application/json

{
  "auto_reply": {
    "enabled": true,
    "default_reply": "感谢您的消息，我会尽快回复！"
  }
}
```

### 💬 消息管理

#### 发送消息
```http
POST /api/send-message
Content-Type: application/json

{
  "target": "好友昵称或群名",
  "message": "要发送的消息内容",
  "type": "friend"  // 或 "group"
}
```

### 👥 联系人管理

#### 获取好友列表
```http
GET /api/friends
```

#### 获取群聊列表
```http
GET /api/groups
```

### 📰 新闻管理

#### 获取新闻推送群组
```http
GET /api/news/groups
```

#### 添加新闻推送群组
```http
POST /api/news/groups
Content-Type: application/json

{
  "group_name": "群聊名称"
}
```

#### 设置推送时间
```http
POST /api/news/schedule
Content-Type: application/json

{
  "time": "09:00"
}
```

## 🔧 开发指南

### 📝 代码规范

- 遵循PEP 8编码规范
- 使用类型注解
- 编写完整的文档字符串
- 统一的错误处理

### 🧪 测试

```bash
# 运行基础测试
python test_basic.py

# 运行系统测试
python test_system.py
```

### 🐛 调试

启用调试模式：
```bash
python start_restructured.py
# 选择 "2. 🔧 启动API服务器 (调试模式)"
```

调试模式特点：
- 详细的错误信息
- 自动重载
- 调试工具栏

## 🔄 从原版本迁移

### 主要变化

1. **文件结构**: 从单文件变为分层架构
2. **API入口**: 使用 `api_restructured.py` 替代 `api_fixed.py`
3. **启动方式**: 使用 `start_restructured.py` 替代 `start.py`
4. **配置管理**: 更强大的配置验证和管理

### 兼容性

- ✅ API接口完全兼容
- ✅ 配置文件格式兼容
- ✅ 功能特性完全保留
- ✅ 可与原版本并存

### 迁移步骤

1. 备份原有配置和数据
2. 使用新的启动脚本
3. 验证功能正常
4. 逐步迁移自定义代码

## 🛠️ 故障排除

### 常见问题

#### 1. 依赖包缺失
```bash
# 解决方案
pip install -r requirements.txt
```

#### 2. 配置文件错误
```bash
# 检查配置文件格式
python -c "import json; json.load(open('config.json'))"
```

#### 3. 微信服务连接失败
- 确保微信客户端已启动
- 检查微信版本兼容性
- 查看日志文件获取详细错误信息

#### 4. 端口占用
```bash
# 查看端口占用
netstat -ano | findstr :5000

# 修改端口（在启动脚本中）
# 或使用环境变量
set FLASK_PORT=5001
```

### 日志查看

```bash
# 查看实时日志
tail -f wechat_backend.log

# 查看错误日志
grep ERROR wechat_backend.log
```

## 🔮 未来规划

### 短期目标
- [ ] 添加更多单元测试
- [ ] 实现API认证机制
- [ ] 添加性能监控
- [ ] 支持配置热重载

### 长期目标
- [ ] 支持多微信账号
- [ ] 实现插件系统
- [ ] 添加Web管理界面
- [ ] 支持分布式部署

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

### 开发环境设置

```bash
# 克隆项目
git clone <repository-url>
cd wechat-backend

# 安装开发依赖
pip install -r requirements.txt
pip install pytest black flake8

# 运行测试
pytest

# 代码格式化
black .

# 代码检查
flake8 .
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如果您遇到问题或有建议，请：

1. 查看 [故障排除](#🛠️-故障排除) 部分
2. 查看 [架构文档](ARCHITECTURE.md)
3. 提交 Issue
4. 联系维护者

---

**🎉 感谢使用微信后端自动化系统重构版！**