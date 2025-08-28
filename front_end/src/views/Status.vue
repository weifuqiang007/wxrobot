<template>
  <div class="status-page">
    <div class="page-header">
      <h1 class="page-title">系统状态</h1>
      <div class="header-actions">
        <el-button type="primary" @click="refreshStatus" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新状态
        </el-button>
      </div>
    </div>
    
    <!-- 系统概览 -->
    <el-card class="overview-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Monitor /></el-icon>
          <span>系统概览</span>
          <el-tag :type="systemStatus.running ? 'success' : 'danger'" class="status-tag">
            {{ systemStatus.running ? '运行中' : '已停止' }}
          </el-tag>
        </div>
      </template>
      
      <div class="overview-grid">
        <div class="overview-item">
          <div class="item-icon success">
            <el-icon><CircleCheck /></el-icon>
          </div>
          <div class="item-content">
            <div class="item-title">系统运行时间</div>
            <div class="item-value">{{ formatUptime(systemStatus.uptime) }}</div>
          </div>
        </div>
        
        <div class="overview-item">
          <div class="item-icon info">
            <el-icon><Cpu /></el-icon>
          </div>
          <div class="item-content">
            <div class="item-title">CPU 使用率</div>
            <div class="item-value">{{ systemStatus.cpu_usage }}%</div>
          </div>
        </div>
        
        <div class="overview-item">
          <div class="item-icon warning">
            <el-icon><MemoryCard /></el-icon>
          </div>
          <div class="item-content">
            <div class="item-title">内存使用</div>
            <div class="item-value">{{ systemStatus.memory_usage }}%</div>
          </div>
        </div>
        
        <div class="overview-item">
          <div class="item-icon primary">
            <el-icon><Connection /></el-icon>
          </div>
          <div class="item-content">
            <div class="item-title">网络状态</div>
            <div class="item-value">正常</div>
          </div>
        </div>
      </div>
    </el-card>
    
    <!-- 服务状态 -->
    <div class="services-grid">
      <el-card class="service-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><ChatDotRound /></el-icon>
            <span>微信服务</span>
          </div>
        </template>
        
        <div class="service-status">
          <div class="status-indicator">
            <div :class="['status-dot', systemStatus.wechat_service ? 'success' : 'error']"></div>
            <span class="status-text">
              {{ systemStatus.wechat_service ? '运行正常' : '服务异常' }}
            </span>
          </div>
          
          <div class="service-details">
            <div class="detail-item">
              <span class="detail-label">版本</span>
              <span class="detail-value">{{ systemStatus.version || 'v1.0.0' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">最后检查</span>
              <span class="detail-value">{{ formatTime(systemStatus.timestamp) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">连接状态</span>
              <span class="detail-value">{{ systemStatus.wechat_service ? '已连接' : '未连接' }}</span>
            </div>
          </div>
          
          <div class="service-actions">
            <el-button
              v-if="!systemStatus.wechat_service"
              type="primary"
              size="small"
              @click="startWechatService"
            >
              启动服务
            </el-button>
            <el-button
              v-else
              type="danger"
              size="small"
              @click="stopWechatService"
            >
              停止服务
            </el-button>
          </div>
        </div>
      </el-card>
      
      <el-card class="service-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Globe /></el-icon>
            <span>API 服务</span>
          </div>
        </template>
        
        <div class="service-status">
          <div class="status-indicator">
            <div class="status-dot success"></div>
            <span class="status-text">运行正常</span>
          </div>
          
          <div class="service-details">
            <div class="detail-item">
              <span class="detail-label">端口</span>
              <span class="detail-value">5000</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">请求数</span>
              <span class="detail-value">{{ apiStats.requests }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">响应时间</span>
              <span class="detail-value">{{ apiStats.response_time }}ms</span>
            </div>
          </div>
        </div>
      </el-card>
      
      <el-card class="service-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Notification /></el-icon>
            <span>新闻推送</span>
          </div>
        </template>
        
        <div class="service-status">
          <div class="status-indicator">
            <div :class="['status-dot', newsService.enabled ? 'success' : 'warning']"></div>
            <span class="status-text">
              {{ newsService.enabled ? '已启用' : '未启用' }}
            </span>
          </div>
          
          <div class="service-details">
            <div class="detail-item">
              <span class="detail-label">推送群组</span>
              <span class="detail-value">{{ newsService.groups }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">推送时间</span>
              <span class="detail-value">{{ newsService.schedule || '09:00' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">最后推送</span>
              <span class="detail-value">{{ formatTime(newsService.last_push) }}</span>
            </div>
          </div>
          
          <div class="service-actions">
            <el-button
              type="primary"
              size="small"
              @click="testNewsPush"
            >
              测试推送
            </el-button>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 系统日志 -->
    <el-card class="logs-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Document /></el-icon>
          <span>系统日志</span>
          <el-button type="text" size="small" @click="clearLogs">
            清空日志
          </el-button>
        </div>
      </template>
      
      <div class="logs-container">
        <div
          v-for="log in systemLogs"
          :key="log.id"
          :class="['log-item', log.level]"
        >
          <div class="log-time">{{ formatTime(log.timestamp) }}</div>
          <div class="log-level">{{ log.level.toUpperCase() }}</div>
          <div class="log-message">{{ log.message }}</div>
        </div>
        
        <div v-if="systemLogs.length === 0" class="empty-logs">
          <el-empty description="暂无日志" :image-size="80" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { statusAPI } from '@/api'

const loading = ref(false)

const systemStatus = ref({
  running: true,
  wechat_service: true,
  version: 'v1.0.0',
  timestamp: new Date().toISOString(),
  uptime: 3600000, // 毫秒
  cpu_usage: 15.6,
  memory_usage: 42.3
})

const apiStats = ref({
  requests: 1234,
  response_time: 85
})

const newsService = ref({
  enabled: true,
  groups: 3,
  schedule: '09:00',
  last_push: new Date().toISOString()
})

const systemLogs = ref([
  {
    id: 1,
    timestamp: new Date().toISOString(),
    level: 'info',
    message: '系统启动成功'
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 60000).toISOString(),
    level: 'success',
    message: '微信服务连接成功'
  },
  {
    id: 3,
    timestamp: new Date(Date.now() - 120000).toISOString(),
    level: 'warning',
    message: 'API请求频率较高，建议优化'
  },
  {
    id: 4,
    timestamp: new Date(Date.now() - 180000).toISOString(),
    level: 'error',
    message: '新闻推送失败，网络连接异常'
  }
])

let statusInterval = null

const formatTime = (timestamp) => {
  if (!timestamp) return '--'
  return new Date(timestamp).toLocaleString('zh-CN')
}

const formatUptime = (uptime) => {
  if (!uptime) return '--'
  const hours = Math.floor(uptime / 3600000)
  const minutes = Math.floor((uptime % 3600000) / 60000)
  return `${hours}小时${minutes}分钟`
}

const refreshStatus = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 更新状态数据
    systemStatus.value.timestamp = new Date().toISOString()
    systemStatus.value.cpu_usage = (Math.random() * 30 + 10).toFixed(1)
    systemStatus.value.memory_usage = (Math.random() * 20 + 30).toFixed(1)
    
    ElMessage.success('状态刷新成功')
  } catch (error) {
    ElMessage.error('刷新失败')
  } finally {
    loading.value = false
  }
}

const startWechatService = async () => {
  try {
    await ElMessageBox.confirm('确定要启动微信服务吗？', '确认操作')
    // 调用启动API
    systemStatus.value.wechat_service = true
    ElMessage.success('微信服务启动成功')
  } catch {
    // 用户取消
  }
}

const stopWechatService = async () => {
  try {
    await ElMessageBox.confirm('确定要停止微信服务吗？', '确认操作', {
      type: 'warning'
    })
    // 调用停止API
    systemStatus.value.wechat_service = false
    ElMessage.success('微信服务已停止')
  } catch {
    // 用户取消
  }
}

const testNewsPush = async () => {
  try {
    ElMessage.info('正在测试新闻推送...')
    // 调用测试API
    await new Promise(resolve => setTimeout(resolve, 2000))
    ElMessage.success('新闻推送测试成功')
  } catch (error) {
    ElMessage.error('新闻推送测试失败')
  }
}

const clearLogs = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有日志吗？', '确认操作', {
      type: 'warning'
    })
    systemLogs.value = []
    ElMessage.success('日志已清空')
  } catch {
    // 用户取消
  }
}

onMounted(() => {
  refreshStatus()
  // 定时刷新状态
  statusInterval = setInterval(() => {
    systemStatus.value.uptime += 60000 // 增加1分钟
  }, 60000)
})

onUnmounted(() => {
  if (statusInterval) {
    clearInterval(statusInterval)
  }
})
</script>

<style scoped>
.status-page {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.status-tag {
  margin-left: auto;
}

.overview-card {
  margin-bottom: 24px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.overview-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.item-icon.success {
  background: rgba(103, 194, 58, 0.1);
  color: #67C23A;
}

.item-icon.info {
  background: rgba(64, 158, 255, 0.1);
  color: #409EFF;
}

.item-icon.warning {
  background: rgba(230, 162, 60, 0.1);
  color: #E6A23C;
}

.item-icon.primary {
  background: rgba(64, 158, 255, 0.1);
  color: #409EFF;
}

.item-content {
  flex: 1;
}

.item-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 4px;
}

.item-value {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.service-status {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.success {
  background: #67C23A;
}

.status-dot.warning {
  background: #E6A23C;
}

.status-dot.error {
  background: #F56C6C;
}

.status-text {
  font-weight: 500;
  color: #2c3e50;
}

.service-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  font-size: 14px;
  color: #909399;
}

.detail-value {
  font-size: 14px;
  color: #2c3e50;
  font-weight: 500;
}

.service-actions {
  display: flex;
  gap: 8px;
}

.logs-container {
  max-height: 400px;
  overflow-y: auto;
}

.log-item {
  display: grid;
  grid-template-columns: 140px 60px 1fr;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 13px;
}

.log-item:last-child {
  border-bottom: none;
}

.log-time {
  color: #909399;
}

.log-level {
  font-weight: 500;
  padding: 2px 6px;
  border-radius: 4px;
  text-align: center;
  font-size: 11px;
}

.log-item.info .log-level {
  background: rgba(64, 158, 255, 0.1);
  color: #409EFF;
}

.log-item.success .log-level {
  background: rgba(103, 194, 58, 0.1);
  color: #67C23A;
}

.log-item.warning .log-level {
  background: rgba(230, 162, 60, 0.1);
  color: #E6A23C;
}

.log-item.error .log-level {
  background: rgba(245, 108, 108, 0.1);
  color: #F56C6C;
}

.log-message {
  color: #2c3e50;
}

.empty-logs {
  padding: 40px 0;
  text-align: center;
}

@media (max-width: 768px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .log-item {
    grid-template-columns: 1fr;
    gap: 4px;
  }
}
</style>