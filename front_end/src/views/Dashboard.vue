<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1 class="page-title">仪表盘</h1>
      <p class="page-description">微信后端自动化系统运行概览</p>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <el-icon size="32" color="#67C23A">
            <CircleCheck />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ systemStatus.running ? '运行中' : '已停止' }}</div>
          <div class="stat-label">系统状态</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <el-icon size="32" color="#409EFF">
            <ChatDotRound />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ messageStats.today }}</div>
          <div class="stat-label">今日消息</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <el-icon size="32" color="#E6A23C">
            <User />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ contactStats.friends }}</div>
          <div class="stat-label">好友数量</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <el-icon size="32" color="#F56C6C">
            <Notification />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ newsStats.groups }}</div>
          <div class="stat-label">推送群组</div>
        </div>
      </div>
    </div>
    
    <!-- 功能区域 -->
    <div class="content-grid">
      <!-- 系统状态 -->
      <el-card class="status-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Monitor /></el-icon>
            <span>系统状态</span>
            <el-button 
              type="text" 
              size="small" 
              @click="checkBackendStatus"
              :loading="checking"
            >
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </template>
        
        <div class="status-list">
          <div class="status-item">
            <span class="status-label">后端API服务</span>
            <el-tag :type="backendStatus.connected ? 'success' : 'danger'" size="small">
              {{ backendStatus.connected ? '正常' : '离线' }}
            </el-tag>
            <el-button 
              v-if="!backendStatus.connected"
              type="primary"
              size="small"
              @click="startBackendService"
              :loading="starting"
              style="margin-left: 8px;"
            >
              启动服务
            </el-button>
          </div>
          
          <div class="status-item">
            <span class="status-label">微信服务</span>
            <el-tag :type="systemStatus.wechat_service ? 'success' : 'danger'" size="small">
              {{ systemStatus.wechat_service ? '正常' : '异常' }}
            </el-tag>
          </div>
          
          <div class="status-item">
            <span class="status-label">新闻推送</span>
            <el-tag :type="newsStats.enabled ? 'success' : 'info'" size="small">
              {{ newsStats.enabled ? '已启用' : '未启用' }}
            </el-tag>
          </div>
          
          <div class="status-item">
            <span class="status-label">最后检查</span>
            <span class="status-time">{{ formatTime(backendStatus.lastCheck) }}</span>
          </div>
        </div>
      </el-card>
      
      <!-- 快速操作 -->
      <el-card class="actions-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Operation /></el-icon>
            <span>快速操作</span>
          </div>
        </template>
        
        <div class="actions-grid">
          <el-button
            type="primary"
            size="large"
            class="action-btn"
            @click="$router.push('/message')"
          >
            <el-icon><ChatDotRound /></el-icon>
            发送消息
          </el-button>
          
          <el-button
            type="success"
            size="large"
            class="action-btn"
            @click="$router.push('/news')"
          >
            <el-icon><Notification /></el-icon>
            新闻推送
          </el-button>
          
          <el-button
            type="warning"
            size="large"
            class="action-btn"
            @click="$router.push('/contacts')"
          >
            <el-icon><User /></el-icon>
            联系人
          </el-button>
          
          <el-button
            type="info"
            size="large"
            class="action-btn"
            @click="$router.push('/config')"
          >
            <el-icon><Setting /></el-icon>
            系统配置
          </el-button>
        </div>
      </el-card>
      
      <!-- 最近活动 -->
      <el-card class="activity-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Clock /></el-icon>
            <span>最近活动</span>
          </div>
        </template>
        
        <div class="activity-list">
          <div
            v-for="activity in recentActivities"
            :key="activity.id"
            class="activity-item"
          >
            <div class="activity-icon">
              <el-icon :color="activity.color">
                <component :is="activity.icon" />
              </el-icon>
            </div>
            <div class="activity-content">
              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-time">{{ activity.time }}</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import {
  CircleCheck,
  ChatDotRound,
  User,
  Notification,
  Monitor,
  Operation,
  Setting,
  Refresh,
  Clock
} from '@element-plus/icons-vue'

const systemStatus = ref({
  running: true,
  wechat_service: true,
  timestamp: new Date().toISOString()
})

const messageStats = ref({
  today: 0,
  total: 0
})

const contactStats = ref({
  friends: 0,
  groups: 0
})

const newsStats = ref({
  groups: 0,
  enabled: false
})

const backendStatus = ref({
  connected: false,
  lastCheck: null
})

const checking = ref(false)
const starting = ref(false)

const checkBackendStatus = async () => {
  checking.value = true
  try {
    const response = await axios.get('http://localhost:5000/api/health')
    backendStatus.value.connected = true
    backendStatus.value.lastCheck = new Date().toISOString()
    ElMessage.success('后端服务连接正常')
  } catch (error) {
    backendStatus.value.connected = false
    backendStatus.value.lastCheck = new Date().toISOString()
    ElMessage.error('后端服务连接失败')
  } finally {
    checking.value = false
  }
}

const startBackendService = async () => {
  starting.value = true
  try {
    ElMessage.info('正在启动后端服务，请稍候...')
    
    // 调用启动脚本的API端点
    // 注意：这需要一个中间服务来执行Python脚本
    // 或者可以通过Electron等方式直接执行系统命令
    
    // 这里先模拟启动过程，等待30秒后检查状态
    let attempts = 0
    const maxAttempts = 30
    
    const checkInterval = setInterval(async () => {
      attempts++
      try {
        const response = await axios.get('http://localhost:5000/api/health')
        if (response.status === 200) {
          clearInterval(checkInterval)
          backendStatus.value.connected = true
          backendStatus.value.lastCheck = new Date().toISOString()
          ElMessage.success('后端服务启动成功！')
          starting.value = false
          return
        }
      } catch (error) {
        // 继续等待
      }
      
      if (attempts >= maxAttempts) {
        clearInterval(checkInterval)
        ElMessage.error('后端服务启动超时，请手动启动服务')
        starting.value = false
      }
    }, 1000)
    
  } catch (error) {
    ElMessage.error('后端服务启动失败')
    starting.value = false
  }
}

const recentActivities = ref([
  {
    id: 1,
    title: '系统启动成功',
    time: '2分钟前',
    icon: 'CircleCheck',
    color: '#67C23A'
  },
  {
    id: 2,
    title: '发送消息给张三',
    time: '5分钟前',
    icon: 'ChatDotRound',
    color: '#409EFF'
  },
  {
    id: 3,
    title: '新闻推送完成',
    time: '1小时前',
    icon: 'Notification',
    color: '#E6A23C'
  },
  {
    id: 4,
    title: '配置更新',
    time: '2小时前',
    icon: 'Setting',
    color: '#909399'
  }
])

const formatTime = (timestamp) => {
  if (!timestamp) return '--'
  return new Date(timestamp).toLocaleString('zh-CN')
}

const loadDashboardData = async () => {
  try {
    // 模拟数据，实际应该调用API
    messageStats.value = {
      today: Math.floor(Math.random() * 100),
      total: Math.floor(Math.random() * 1000)
    }
    
    contactStats.value = {
      friends: Math.floor(Math.random() * 200) + 50,
      groups: Math.floor(Math.random() * 20) + 5
    }
    
    newsStats.value = {
      groups: Math.floor(Math.random() * 10) + 2,
      enabled: Math.random() > 0.5
    }
    
    // 获取系统状态
    // const status = await statusAPI.getStatus()
    // systemStatus.value = status.data
  } catch (error) {
    ElMessage.error('加载数据失败')
  }
}

onMounted(() => {
  loadDashboardData()
  checkBackendStatus()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.dashboard-header {
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: rgba(64, 158, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.card-header .el-button {
  margin-left: auto;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-label {
  font-size: 14px;
  color: #606266;
}

.status-time {
  font-size: 14px;
  color: #909399;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.action-btn {
  height: 60px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 14px;
  color: #2c3e50;
  margin-bottom: 2px;
}

.activity-time {
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>