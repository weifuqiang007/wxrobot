<template>
  <div class="config-page">
    <div class="page-header">
      <h1 class="page-title">系统配置</h1>
      <p class="page-description">管理系统的各项配置参数</p>
    </div>
    
    <!-- 配置分类标签 -->
    <el-tabs v-model="activeTab" class="config-tabs">
      <!-- 基础配置 -->
      <el-tab-pane label="基础配置" name="basic">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Setting /></el-icon>
              <span>基础配置</span>
            </div>
          </template>
          
          <el-form
            ref="basicFormRef"
            :model="basicConfig"
            :rules="basicRules"
            label-width="120px"
            class="config-form"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="系统名称" prop="systemName">
                  <el-input v-model="basicConfig.systemName" placeholder="请输入系统名称" />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="系统版本" prop="version">
                  <el-input v-model="basicConfig.version" placeholder="请输入系统版本" readonly />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="管理员邮箱" prop="adminEmail">
                  <el-input v-model="basicConfig.adminEmail" placeholder="请输入管理员邮箱" />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="系统语言" prop="language">
                  <el-select v-model="basicConfig.language" placeholder="选择系统语言" style="width: 100%">
                    <el-option label="简体中文" value="zh-CN" />
                    <el-option label="English" value="en-US" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="时区设置" prop="timezone">
                  <el-select v-model="basicConfig.timezone" placeholder="选择时区" style="width: 100%">
                    <el-option label="北京时间 (UTC+8)" value="Asia/Shanghai" />
                    <el-option label="东京时间 (UTC+9)" value="Asia/Tokyo" />
                    <el-option label="纽约时间 (UTC-5)" value="America/New_York" />
                  </el-select>
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="日志级别" prop="logLevel">
                  <el-select v-model="basicConfig.logLevel" placeholder="选择日志级别" style="width: 100%">
                    <el-option label="DEBUG" value="debug" />
                    <el-option label="INFO" value="info" />
                    <el-option label="WARNING" value="warning" />
                    <el-option label="ERROR" value="error" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="系统描述" prop="description">
              <el-input
                v-model="basicConfig.description"
                type="textarea"
                :rows="3"
                placeholder="请输入系统描述"
                maxlength="200"
                show-word-limit
              />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveBasicConfig" :loading="saving.basic">
                <el-icon><Check /></el-icon>
                保存配置
              </el-button>
              <el-button @click="resetBasicConfig">
                <el-icon><RefreshLeft /></el-icon>
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <!-- 微信配置 -->
      <el-tab-pane label="微信配置" name="wechat">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><ChatDotRound /></el-icon>
              <span>微信配置</span>
            </div>
          </template>
          
          <el-form
            ref="wechatFormRef"
            :model="wechatConfig"
            :rules="wechatRules"
            label-width="120px"
            class="config-form"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="微信路径" prop="wechatPath">
                  <el-input v-model="wechatConfig.wechatPath" placeholder="微信安装路径">
                    <template #append>
                      <el-button @click="selectWechatPath">
                        <el-icon><Folder /></el-icon>
                        浏览
                      </el-button>
                    </template>
                  </el-input>
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="自动登录" prop="autoLogin">
                  <el-switch
                    v-model="wechatConfig.autoLogin"
                    active-text="启用"
                    inactive-text="禁用"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="消息延迟" prop="messageDelay">
                  <el-input-number
                    v-model="wechatConfig.messageDelay"
                    :min="100"
                    :max="5000"
                    :step="100"
                    placeholder="消息发送延迟(毫秒)"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="重试次数" prop="retryCount">
                  <el-input-number
                    v-model="wechatConfig.retryCount"
                    :min="0"
                    :max="10"
                    placeholder="失败重试次数"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="监听端口" prop="listenPort">
                  <el-input-number
                    v-model="wechatConfig.listenPort"
                    :min="1000"
                    :max="65535"
                    placeholder="微信监听端口"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="心跳间隔" prop="heartbeatInterval">
                  <el-input-number
                    v-model="wechatConfig.heartbeatInterval"
                    :min="5"
                    :max="300"
                    placeholder="心跳检测间隔(秒)"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="启用功能" prop="enabledFeatures">
              <el-checkbox-group v-model="wechatConfig.enabledFeatures">
                <el-checkbox label="auto_reply">自动回复</el-checkbox>
                <el-checkbox label="message_log">消息记录</el-checkbox>
                <el-checkbox label="friend_verify">好友验证</el-checkbox>
                <el-checkbox label="group_manage">群管理</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveWechatConfig" :loading="saving.wechat">
                <el-icon><Check /></el-icon>
                保存配置
              </el-button>
              <el-button @click="resetWechatConfig">
                <el-icon><RefreshLeft /></el-icon>
                重置
              </el-button>
              <el-button type="success" @click="testWechatConnection">
                <el-icon><Connection /></el-icon>
                测试连接
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <!-- 数据库配置 -->
      <el-tab-pane label="数据库配置" name="database">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Coin /></el-icon>
              <span>数据库配置</span>
            </div>
          </template>
          
          <el-form
            ref="databaseFormRef"
            :model="databaseConfig"
            :rules="databaseRules"
            label-width="120px"
            class="config-form"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="数据库类型" prop="type">
                  <el-select v-model="databaseConfig.type" placeholder="选择数据库类型" style="width: 100%">
                    <el-option label="SQLite" value="sqlite" />
                    <el-option label="MySQL" value="mysql" />
                    <el-option label="PostgreSQL" value="postgresql" />
                  </el-select>
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="数据库名称" prop="database">
                  <el-input v-model="databaseConfig.database" placeholder="数据库名称" />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20" v-if="databaseConfig.type !== 'sqlite'">
              <el-col :span="12">
                <el-form-item label="主机地址" prop="host">
                  <el-input v-model="databaseConfig.host" placeholder="数据库主机地址" />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="端口" prop="port">
                  <el-input-number
                    v-model="databaseConfig.port"
                    :min="1"
                    :max="65535"
                    placeholder="数据库端口"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20" v-if="databaseConfig.type !== 'sqlite'">
              <el-col :span="12">
                <el-form-item label="用户名" prop="username">
                  <el-input v-model="databaseConfig.username" placeholder="数据库用户名" />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="密码" prop="password">
                  <el-input
                    v-model="databaseConfig.password"
                    type="password"
                    placeholder="数据库密码"
                    show-password
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="连接池大小" prop="poolSize">
                  <el-input-number
                    v-model="databaseConfig.poolSize"
                    :min="1"
                    :max="100"
                    placeholder="连接池大小"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="连接超时" prop="timeout">
                  <el-input-number
                    v-model="databaseConfig.timeout"
                    :min="1000"
                    :max="60000"
                    :step="1000"
                    placeholder="连接超时(毫秒)"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item>
              <el-button type="primary" @click="saveDatabaseConfig" :loading="saving.database">
                <el-icon><Check /></el-icon>
                保存配置
              </el-button>
              <el-button @click="resetDatabaseConfig">
                <el-icon><RefreshLeft /></el-icon>
                重置
              </el-button>
              <el-button type="success" @click="testDatabaseConnection">
                <el-icon><Connection /></el-icon>
                测试连接
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <!-- 安全配置 -->
      <el-tab-pane label="安全配置" name="security">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Lock /></el-icon>
              <span>安全配置</span>
            </div>
          </template>
          
          <el-form
            ref="securityFormRef"
            :model="securityConfig"
            :rules="securityRules"
            label-width="120px"
            class="config-form"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="JWT密钥" prop="jwtSecret">
                  <el-input
                    v-model="securityConfig.jwtSecret"
                    type="password"
                    placeholder="JWT签名密钥"
                    show-password
                  >
                    <template #append>
                      <el-button @click="generateJwtSecret">
                        <el-icon><Refresh /></el-icon>
                        生成
                      </el-button>
                    </template>
                  </el-input>
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="Token过期时间" prop="tokenExpiry">
                  <el-input-number
                    v-model="securityConfig.tokenExpiry"
                    :min="1"
                    :max="168"
                    placeholder="Token过期时间(小时)"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="登录失败限制" prop="maxLoginAttempts">
                  <el-input-number
                    v-model="securityConfig.maxLoginAttempts"
                    :min="3"
                    :max="10"
                    placeholder="最大登录失败次数"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="锁定时间" prop="lockoutDuration">
                  <el-input-number
                    v-model="securityConfig.lockoutDuration"
                    :min="5"
                    :max="1440"
                    placeholder="账户锁定时间(分钟)"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="密码最小长度" prop="minPasswordLength">
                  <el-input-number
                    v-model="securityConfig.minPasswordLength"
                    :min="6"
                    :max="20"
                    placeholder="密码最小长度"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              
              <el-col :span="12">
                <el-form-item label="会话超时" prop="sessionTimeout">
                  <el-input-number
                    v-model="securityConfig.sessionTimeout"
                    :min="10"
                    :max="480"
                    placeholder="会话超时时间(分钟)"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="安全选项" prop="securityOptions">
              <el-checkbox-group v-model="securityConfig.securityOptions">
                <el-checkbox label="force_https">强制HTTPS</el-checkbox>
                <el-checkbox label="enable_2fa">启用双因子认证</el-checkbox>
                <el-checkbox label="password_complexity">密码复杂度要求</el-checkbox>
                <el-checkbox label="ip_whitelist">IP白名单</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            
            <el-form-item label="IP白名单" prop="ipWhitelist" v-if="securityConfig.securityOptions.includes('ip_whitelist')">
              <el-input
                v-model="securityConfig.ipWhitelist"
                type="textarea"
                :rows="3"
                placeholder="每行一个IP地址或IP段，例如：192.168.1.1 或 192.168.1.0/24"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveSecurityConfig" :loading="saving.security">
                <el-icon><Check /></el-icon>
                保存配置
              </el-button>
              <el-button @click="resetSecurityConfig">
                <el-icon><RefreshLeft /></el-icon>
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <!-- 备份恢复 -->
      <el-tab-pane label="备份恢复" name="backup">
        <div class="backup-section">
          <!-- 数据备份 -->
          <el-card shadow="hover" class="backup-card">
            <template #header>
              <div class="card-header">
                <el-icon><Download /></el-icon>
                <span>数据备份</span>
              </div>
            </template>
            
            <div class="backup-content">
              <p class="backup-description">
                定期备份系统数据，包括配置信息、用户数据、消息记录等。
              </p>
              
              <div class="backup-options">
                <el-checkbox-group v-model="backupOptions">
                  <el-checkbox label="config">系统配置</el-checkbox>
                  <el-checkbox label="users">用户数据</el-checkbox>
                  <el-checkbox label="messages">消息记录</el-checkbox>
                  <el-checkbox label="contacts">联系人信息</el-checkbox>
                  <el-checkbox label="logs">系统日志</el-checkbox>
                </el-checkbox-group>
              </div>
              
              <div class="backup-actions">
                <el-button type="primary" @click="createBackup" :loading="backupLoading">
                  <el-icon><Download /></el-icon>
                  立即备份
                </el-button>
                
                <el-button @click="scheduleBackup">
                  <el-icon><Timer /></el-icon>
                  定时备份设置
                </el-button>
              </div>
            </div>
          </el-card>
          
          <!-- 数据恢复 -->
          <el-card shadow="hover" class="backup-card">
            <template #header>
              <div class="card-header">
                <el-icon><Upload /></el-icon>
                <span>数据恢复</span>
              </div>
            </template>
            
            <div class="backup-content">
              <p class="backup-description">
                从备份文件恢复系统数据，请谨慎操作。
              </p>
              
              <div class="restore-upload">
                <el-upload
                  ref="uploadRef"
                  :auto-upload="false"
                  :show-file-list="true"
                  :limit="1"
                  accept=".zip,.tar.gz"
                  @change="handleFileChange"
                >
                  <el-button type="primary">
                    <el-icon><Upload /></el-icon>
                    选择备份文件
                  </el-button>
                  <template #tip>
                    <div class="el-upload__tip">
                      支持 .zip 和 .tar.gz 格式的备份文件
                    </div>
                  </template>
                </el-upload>
              </div>
              
              <div class="restore-actions">
                <el-button
                  type="danger"
                  @click="restoreBackup"
                  :loading="restoreLoading"
                  :disabled="!selectedBackupFile"
                >
                  <el-icon><Upload /></el-icon>
                  开始恢复
                </el-button>
                
                <el-button @click="validateBackup" :disabled="!selectedBackupFile">
                  <el-icon><View /></el-icon>
                  验证备份文件
                </el-button>
              </div>
            </div>
          </el-card>
          
          <!-- 备份历史 -->
          <el-card shadow="hover" class="backup-card">
            <template #header>
              <div class="card-header">
                <el-icon><Clock /></el-icon>
                <span>备份历史</span>
                <el-button type="text" size="small" @click="refreshBackupHistory">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
              </div>
            </template>
            
            <el-table
              :data="backupHistory"
              style="width: 100%"
              :loading="historyLoading"
              empty-text="暂无备份记录"
            >
              <el-table-column prop="filename" label="备份文件" min-width="200" />
              
              <el-table-column prop="size" label="文件大小" width="100">
                <template #default="{ row }">
                  {{ formatFileSize(row.size) }}
                </template>
              </el-table-column>
              
              <el-table-column prop="type" label="备份类型" width="120">
                <template #default="{ row }">
                  <el-tag :type="row.type === 'auto' ? 'success' : 'primary'" size="small">
                    {{ row.type === 'auto' ? '自动' : '手动' }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column prop="createTime" label="创建时间" width="160">
                <template #default="{ row }">
                  {{ formatTime(row.createTime) }}
                </template>
              </el-table-column>
              
              <el-table-column label="操作" width="150">
                <template #default="{ row }">
                  <el-button type="text" size="small" @click="downloadBackup(row)">
                    <el-icon><Download /></el-icon>
                    下载
                  </el-button>
                  
                  <el-button type="text" size="small" @click="deleteBackup(row)">
                    <el-icon><Delete /></el-icon>
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { configAPI } from '@/api'

const activeTab = ref('basic')

const basicFormRef = ref()
const wechatFormRef = ref()
const databaseFormRef = ref()
const securityFormRef = ref()
const uploadRef = ref()

const saving = reactive({
  basic: false,
  wechat: false,
  database: false,
  security: false
})

const backupLoading = ref(false)
const restoreLoading = ref(false)
const historyLoading = ref(false)

// 基础配置
const basicConfig = reactive({
  systemName: 'WeChat Robot',
  version: '1.0.0',
  adminEmail: 'admin@example.com',
  language: 'zh-CN',
  timezone: 'Asia/Shanghai',
  logLevel: 'info',
  description: '微信机器人自动化系统'
})

const basicRules = {
  systemName: [{ required: true, message: '请输入系统名称', trigger: 'blur' }],
  adminEmail: [
    { required: true, message: '请输入管理员邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  language: [{ required: true, message: '请选择系统语言', trigger: 'change' }],
  timezone: [{ required: true, message: '请选择时区', trigger: 'change' }],
  logLevel: [{ required: true, message: '请选择日志级别', trigger: 'change' }]
}

// 微信配置
const wechatConfig = reactive({
  wechatPath: 'C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe',
  autoLogin: true,
  messageDelay: 1000,
  retryCount: 3,
  listenPort: 8080,
  heartbeatInterval: 30,
  enabledFeatures: ['auto_reply', 'message_log']
})

const wechatRules = {
  wechatPath: [{ required: true, message: '请输入微信路径', trigger: 'blur' }],
  messageDelay: [{ required: true, message: '请输入消息延迟', trigger: 'blur' }],
  retryCount: [{ required: true, message: '请输入重试次数', trigger: 'blur' }],
  listenPort: [{ required: true, message: '请输入监听端口', trigger: 'blur' }],
  heartbeatInterval: [{ required: true, message: '请输入心跳间隔', trigger: 'blur' }]
}

// 数据库配置
const databaseConfig = reactive({
  type: 'sqlite',
  database: 'wechat_robot.db',
  host: 'localhost',
  port: 3306,
  username: 'root',
  password: '',
  poolSize: 10,
  timeout: 5000
})

const databaseRules = {
  type: [{ required: true, message: '请选择数据库类型', trigger: 'change' }],
  database: [{ required: true, message: '请输入数据库名称', trigger: 'blur' }],
  host: [{ required: true, message: '请输入主机地址', trigger: 'blur' }],
  port: [{ required: true, message: '请输入端口', trigger: 'blur' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  poolSize: [{ required: true, message: '请输入连接池大小', trigger: 'blur' }],
  timeout: [{ required: true, message: '请输入连接超时时间', trigger: 'blur' }]
}

// 安全配置
const securityConfig = reactive({
  jwtSecret: 'your-secret-key-here',
  tokenExpiry: 24,
  maxLoginAttempts: 5,
  lockoutDuration: 30,
  minPasswordLength: 8,
  sessionTimeout: 120,
  securityOptions: ['force_https', 'password_complexity'],
  ipWhitelist: ''
})

const securityRules = {
  jwtSecret: [{ required: true, message: '请输入JWT密钥', trigger: 'blur' }],
  tokenExpiry: [{ required: true, message: '请输入Token过期时间', trigger: 'blur' }],
  maxLoginAttempts: [{ required: true, message: '请输入最大登录失败次数', trigger: 'blur' }],
  lockoutDuration: [{ required: true, message: '请输入锁定时间', trigger: 'blur' }],
  minPasswordLength: [{ required: true, message: '请输入密码最小长度', trigger: 'blur' }],
  sessionTimeout: [{ required: true, message: '请输入会话超时时间', trigger: 'blur' }]
}

// 备份相关
const backupOptions = ref(['config', 'users', 'messages'])
const selectedBackupFile = ref(null)

const backupHistory = ref([
  {
    id: 1,
    filename: 'backup_20240120_090000.zip',
    size: 1024000,
    type: 'auto',
    createTime: '2024-01-20T09:00:00Z'
  },
  {
    id: 2,
    filename: 'backup_20240119_180000.zip',
    size: 856000,
    type: 'manual',
    createTime: '2024-01-19T18:00:00Z'
  }
])

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString('zh-CN')
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 保存配置方法
const saveBasicConfig = async () => {
  if (!basicFormRef.value) return
  
  try {
    const valid = await basicFormRef.value.validate()
    if (!valid) return
    
    saving.basic = true
    
    // 调用保存API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('基础配置保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.basic = false
  }
}

const saveWechatConfig = async () => {
  if (!wechatFormRef.value) return
  
  try {
    const valid = await wechatFormRef.value.validate()
    if (!valid) return
    
    saving.wechat = true
    
    // 调用保存API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('微信配置保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.wechat = false
  }
}

const saveDatabaseConfig = async () => {
  if (!databaseFormRef.value) return
  
  try {
    const valid = await databaseFormRef.value.validate()
    if (!valid) return
    
    saving.database = true
    
    // 调用保存API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('数据库配置保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.database = false
  }
}

const saveSecurityConfig = async () => {
  if (!securityFormRef.value) return
  
  try {
    const valid = await securityFormRef.value.validate()
    if (!valid) return
    
    saving.security = true
    
    // 调用保存API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('安全配置保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.security = false
  }
}

// 重置配置方法
const resetBasicConfig = () => {
  if (basicFormRef.value) {
    basicFormRef.value.resetFields()
  }
}

const resetWechatConfig = () => {
  if (wechatFormRef.value) {
    wechatFormRef.value.resetFields()
  }
}

const resetDatabaseConfig = () => {
  if (databaseFormRef.value) {
    databaseFormRef.value.resetFields()
  }
}

const resetSecurityConfig = () => {
  if (securityFormRef.value) {
    securityFormRef.value.resetFields()
  }
}

// 其他功能方法
const selectWechatPath = () => {
  // 这里可以调用文件选择对话框
  ElMessage.info('请手动输入微信安装路径')
}

const testWechatConnection = async () => {
  try {
    // 模拟测试微信连接
    await new Promise(resolve => setTimeout(resolve, 2000))
    ElMessage.success('微信连接测试成功')
  } catch (error) {
    ElMessage.error('微信连接测试失败')
  }
}

const testDatabaseConnection = async () => {
  try {
    // 模拟测试数据库连接
    await new Promise(resolve => setTimeout(resolve, 2000))
    ElMessage.success('数据库连接测试成功')
  } catch (error) {
    ElMessage.error('数据库连接测试失败')
  }
}

const generateJwtSecret = () => {
  // 生成随机JWT密钥
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < 32; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  securityConfig.jwtSecret = result
  ElMessage.success('JWT密钥已生成')
}

// 备份相关方法
const createBackup = async () => {
  if (backupOptions.value.length === 0) {
    ElMessage.warning('请选择要备份的数据类型')
    return
  }
  
  backupLoading.value = true
  try {
    // 模拟创建备份
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    const filename = `backup_${new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5)}.zip`
    backupHistory.value.unshift({
      id: Date.now(),
      filename,
      size: Math.floor(Math.random() * 2000000) + 500000,
      type: 'manual',
      createTime: new Date().toISOString()
    })
    
    ElMessage.success('备份创建成功')
  } catch (error) {
    ElMessage.error('备份创建失败')
  } finally {
    backupLoading.value = false
  }
}

const scheduleBackup = () => {
  ElMessage.info('定时备份功能开发中')
}

const handleFileChange = (file) => {
  selectedBackupFile.value = file
}

const restoreBackup = async () => {
  try {
    await ElMessageBox.confirm(
      '恢复备份将覆盖当前数据，此操作不可逆，确定要继续吗？',
      '确认恢复',
      { type: 'warning' }
    )
    
    restoreLoading.value = true
    
    // 模拟恢复备份
    await new Promise(resolve => setTimeout(resolve, 5000))
    
    ElMessage.success('数据恢复成功')
    selectedBackupFile.value = null
    if (uploadRef.value) {
      uploadRef.value.clearFiles()
    }
  } catch {
    // 用户取消
  } finally {
    restoreLoading.value = false
  }
}

const validateBackup = async () => {
  try {
    // 模拟验证备份文件
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('备份文件验证通过')
  } catch (error) {
    ElMessage.error('备份文件验证失败')
  }
}

const refreshBackupHistory = async () => {
  historyLoading.value = true
  try {
    // 模拟刷新备份历史
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('备份历史刷新成功')
  } catch (error) {
    ElMessage.error('刷新失败')
  } finally {
    historyLoading.value = false
  }
}

const downloadBackup = (backup) => {
  // 模拟下载备份文件
  ElMessage.success(`开始下载 ${backup.filename}`)
}

const deleteBackup = async (backup) => {
  try {
    await ElMessageBox.confirm(`确定要删除备份文件 ${backup.filename} 吗？`, '确认删除', {
      type: 'warning'
    })
    
    const index = backupHistory.value.findIndex(b => b.id === backup.id)
    if (index !== -1) {
      backupHistory.value.splice(index, 1)
    }
    
    ElMessage.success('备份文件删除成功')
  } catch {
    // 用户取消
  }
}

onMounted(() => {
  // 初始化时加载配置
})
</script>

<style scoped>
.config-page {
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.page-description {
  color: #7f8c8d;
  margin: 0;
}

.config-tabs {
  margin-top: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header .header-left,
.card-header > div:first-child {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.config-form {
  max-width: 800px;
}

.backup-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.backup-card {
  margin-bottom: 0;
}

.backup-content {
  padding: 16px 0;
}

.backup-description {
  color: #606266;
  margin-bottom: 16px;
  line-height: 1.6;
}

.backup-options {
  margin-bottom: 20px;
}

.backup-actions,
.restore-actions {
  display: flex;
  gap: 12px;
}

.restore-upload {
  margin-bottom: 20px;
}

.el-upload__tip {
  color: #909399;
  font-size: 12px;
  margin-top: 8px;
}

@media (max-width: 768px) {
  .config-form {
    max-width: 100%;
  }
  
  .backup-actions,
  .restore-actions {
    flex-direction: column;
  }
}
</style>