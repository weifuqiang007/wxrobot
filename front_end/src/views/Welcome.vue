<template>
  <div class="welcome-page">
    <div class="page-header">
      <h1 class="page-title">新成员欢迎</h1>
      <p class="page-description">自动监听群聊新成员加入并发送欢迎消息</p>
    </div>
    
    <!-- 监听控制面板 -->
    <el-card class="monitoring-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><UserFilled /></el-icon>
          <span>欢迎监听控制</span>
          <div class="header-actions">
            <el-tag :type="monitoringStatus.status === 'running' ? 'success' : 'info'" size="small">
              {{ monitoringStatus.status === 'running' ? '监听中' : '已停止' }}
            </el-tag>
          </div>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form label-width="100px">
            <el-form-item label="监听群组">
              <el-select
                v-model="selectedGroups"
                multiple
                placeholder="选择要监听的群组（不选则监听所有群组）"
                style="width: 100%"
                :loading="groupsLoading"
                collapse-tags
                collapse-tags-tooltip
              >
                <el-option
                  v-for="group in allGroups"
                  :key="group"
                  :label="group"
                  :value="group"
                />
              </el-select>
            </el-form-item>
            
            <el-form-item label="监听时长">
              <el-select v-model="monitoringDuration" style="width: 100%">
                <el-option label="30分钟" value="30m" />
                <el-option label="1小时" value="1h" />
                <el-option label="2小时" value="2h" />
                <el-option label="6小时" value="6h" />
                <el-option label="12小时" value="12h" />
                <el-option label="24小时" value="24h" />
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button
                v-if="monitoringStatus.status !== 'running'"
                type="primary"
                @click="startWelcomeMonitoring"
                :loading="operationLoading"
                size="large"
              >
                <el-icon><VideoPlay /></el-icon>
                开始监听
              </el-button>
              
              <el-button
                v-else
                type="danger"
                @click="stopWelcomeMonitoring"
                :loading="operationLoading"
                size="large"
              >
                <el-icon><VideoPause /></el-icon>
                停止监听
              </el-button>
              
              <el-button @click="refreshStatus" size="large">
                <el-icon><Refresh /></el-icon>
                刷新状态
              </el-button>
            </el-form-item>
          </el-form>
        </el-col>
        
        <el-col :span="12">
          <div class="monitoring-info">
            <h4>监听状态</h4>
            <div class="info-item">
              <span class="label">状态：</span>
              <el-tag :type="monitoringStatus.status === 'running' ? 'success' : 'info'" size="small">
                {{ monitoringStatus.status === 'running' ? '运行中' : '已停止' }}
              </el-tag>
            </div>
            <div class="info-item" v-if="monitoringStatus.status === 'running'">
              <span class="label">运行时长：</span>
              <span class="value">{{ formatDuration(monitoringStatus.running_duration) }}</span>
            </div>
            <div class="info-item">
              <span class="label">监听群组数：</span>
              <span class="value">{{ monitoringStatus.monitored_groups_count || 0 }}</span>
            </div>
            <div class="info-item">
              <span class="label">处理消息数：</span>
              <span class="value">{{ monitoringStatus.processed_count || 0 }}</span>
            </div>
            <div class="info-item" v-if="monitoringStatus.welcome_count !== undefined">
              <span class="label">发送欢迎数：</span>
              <span class="value">{{ monitoringStatus.welcome_count }}</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 欢迎消息模板 -->
    <el-card class="template-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><ChatDotRound /></el-icon>
          <span>欢迎消息模板</span>
        </div>
      </template>
      
      <el-form label-width="100px">
        <el-form-item label="消息模板">
          <el-input
            v-model="welcomeTemplate"
            type="textarea"
            :rows="4"
            placeholder="请输入欢迎消息模板，使用 @{member_name} 作为新成员名称占位符"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            @click="saveTemplate"
            :loading="templateLoading"
          >
            <el-icon><Check /></el-icon>
            保存模板
          </el-button>
          
          <el-button @click="resetTemplate">
            <el-icon><RefreshLeft /></el-icon>
            重置为默认
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="template-preview">
        <h4>预览效果：</h4>
        <div class="preview-message">
          {{ previewMessage }}
        </div>
      </div>
    </el-card>
    
    <!-- 监听群组列表 -->
    <el-card class="groups-card" shadow="hover" v-if="monitoringStatus.monitored_groups && monitoringStatus.monitored_groups.length > 0">
      <template #header>
        <div class="card-header">
          <el-icon><Grid /></el-icon>
          <span>当前监听群组</span>
        </div>
      </template>
      
      <div class="groups-list">
        <el-tag
          v-for="group in monitoringStatus.monitored_groups"
          :key="group"
          type="success"
          class="group-tag"
        >
          {{ group }}
        </el-tag>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  UserFilled,
  ChatDotRound,
  VideoPlay,
  VideoPause,
  Refresh,
  Check,
  RefreshLeft,
  Grid
} from '@element-plus/icons-vue'
import api from '@/api'

// 响应式数据
const allGroups = ref([])
const selectedGroups = ref([])
const monitoringDuration = ref('24h')
const welcomeTemplate = ref('')
const monitoringStatus = reactive({
  status: 'stopped',
  monitored_groups: [],
  monitored_groups_count: 0,
  processed_count: 0,
  running_duration: 0,
  welcome_count: 0
})

// 加载状态
const groupsLoading = ref(false)
const operationLoading = ref(false)
const templateLoading = ref(false)

// 计算属性
const previewMessage = computed(() => {
  return welcomeTemplate.value.replace('@{member_name}', '张三')
})

// 格式化时长
const formatDuration = (seconds) => {
  if (!seconds) return '0秒'
  
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  if (hours > 0) {
    return `${hours}小时${minutes}分钟${secs}秒`
  } else if (minutes > 0) {
    return `${minutes}分钟${secs}秒`
  } else {
    return `${secs}秒`
  }
}

// 获取群组列表
const fetchGroups = async () => {
  try {
    groupsLoading.value = true
    const response = await api.get('/api/welcome/groups')
    if (response.data.success) {
      allGroups.value = response.data.data.all_groups || []
      // 更新监听状态
      Object.assign(monitoringStatus, {
        status: response.data.data.monitoring_status ? 'running' : 'stopped',
        monitored_groups: response.data.data.monitored_groups || []
      })
    }
  } catch (error) {
    console.error('获取群组列表失败:', error)
    ElMessage.error('获取群组列表失败')
  } finally {
    groupsLoading.value = false
  }
}

// 获取欢迎消息模板
const fetchTemplate = async () => {
  try {
    const response = await api.get('/api/welcome/template')
    if (response.data.success) {
      welcomeTemplate.value = response.data.data.template
    }
  } catch (error) {
    console.error('获取欢迎模板失败:', error)
    ElMessage.error('获取欢迎模板失败')
  }
}

// 获取监听状态
const fetchMonitoringStatus = async () => {
  try {
    const response = await api.get('/api/welcome/monitoring/status')
    if (response.data.success) {
      Object.assign(monitoringStatus, response.data.data)
      monitoringStatus.status = response.data.data.status || 'stopped'
    }
  } catch (error) {
    console.error('获取监听状态失败:', error)
  }
}

// 开始监听
const startWelcomeMonitoring = async () => {
  try {
    operationLoading.value = true
    const requestData = {
      duration: monitoringDuration.value
    }
    
    if (selectedGroups.value.length > 0) {
      requestData.groups = selectedGroups.value
    }
    
    const response = await api.post('/api/welcome/monitoring/start', requestData)
    if (response.data.success) {
      ElMessage.success('开始监听新成员欢迎')
      await fetchMonitoringStatus()
    } else {
      ElMessage.error(response.data.message || '启动监听失败')
    }
  } catch (error) {
    console.error('启动监听失败:', error)
    ElMessage.error('启动监听失败')
  } finally {
    operationLoading.value = false
  }
}

// 停止监听
const stopWelcomeMonitoring = async () => {
  try {
    await ElMessageBox.confirm('确定要停止新成员欢迎监听吗？', '确认操作', {
      type: 'warning'
    })
    
    operationLoading.value = true
    const response = await api.post('/api/welcome/monitoring/stop')
    if (response.data.success) {
      ElMessage.success('已停止监听')
      await fetchMonitoringStatus()
    } else {
      ElMessage.error(response.data.message || '停止监听失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('停止监听失败:', error)
      ElMessage.error('停止监听失败')
    }
  } finally {
    operationLoading.value = false
  }
}

// 保存模板
const saveTemplate = async () => {
  if (!welcomeTemplate.value.trim()) {
    ElMessage.warning('请输入欢迎消息模板')
    return
  }
  
  try {
    templateLoading.value = true
    const response = await api.post('/api/welcome/template', {
      template: welcomeTemplate.value
    })
    if (response.data.success) {
      ElMessage.success('保存模板成功')
    } else {
      ElMessage.error(response.data.message || '保存模板失败')
    }
  } catch (error) {
    console.error('保存模板失败:', error)
    ElMessage.error('保存模板失败')
  } finally {
    templateLoading.value = false
  }
}

// 重置模板
const resetTemplate = () => {
  welcomeTemplate.value = '欢迎 @{member_name} 加入群聊！🎉'
}

// 刷新状态
const refreshStatus = async () => {
  await Promise.all([
    fetchGroups(),
    fetchMonitoringStatus()
  ])
}

// 组件挂载时初始化
onMounted(async () => {
  await Promise.all([
    fetchGroups(),
    fetchTemplate(),
    fetchMonitoringStatus()
  ])
  
  // 定时刷新状态（每30秒）
  setInterval(() => {
    if (monitoringStatus.status === 'running') {
      fetchMonitoringStatus()
    }
  }, 30000)
})
</script>

<style scoped>
.welcome-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.page-description {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 600;
}

.card-header > span {
  margin-left: 8px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.monitoring-card,
.template-card,
.groups-card {
  margin-bottom: 20px;
}

.monitoring-info {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
}

.monitoring-info h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  color: #303133;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-item .label {
  font-weight: 500;
  color: #606266;
  min-width: 80px;
}

.info-item .value {
  color: #303133;
  font-weight: 600;
}

.template-preview {
  margin-top: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.template-preview h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #606266;
}

.preview-message {
  padding: 12px;
  background: #e7f3ff;
  border: 1px solid #b3d8ff;
  border-radius: 6px;
  color: #0066cc;
  font-size: 14px;
}

.groups-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.group-tag {
  margin: 0;
}

.el-card {
  border-radius: 12px;
}

.el-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px 12px 0 0;
}

.el-card :deep(.el-card__header .card-header) {
  color: white;
}

.el-button {
  border-radius: 8px;
}

.el-form-item {
  margin-bottom: 18px;
}
</style>