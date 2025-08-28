<template>
  <div class="message-page">
    <div class="page-header">
      <h1 class="page-title">消息管理</h1>
      <p class="page-description">发送消息到好友或群聊</p>
    </div>
    
    <!-- 发送消息表单 -->
    <el-card class="send-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><ChatDotRound /></el-icon>
          <span>发送消息</span>
        </div>
      </template>
      
      <el-form
        ref="messageFormRef"
        :model="messageForm"
        :rules="messageRules"
        label-width="80px"
        class="message-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="消息类型" prop="type">
              <el-radio-group v-model="messageForm.type" @change="onTypeChange">
                <el-radio label="friend">好友</el-radio>
                <el-radio label="group">群聊</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item :label="messageForm.type === 'friend' ? '选择好友' : '选择群聊'" prop="target">
              <el-select
                v-model="messageForm.target"
                :placeholder="messageForm.type === 'friend' ? '请选择好友' : '请选择群聊'"
                filterable
                style="width: 100%"
                :loading="contactsLoading"
              >
                <el-option
                  v-for="contact in currentContacts"
                  :key="contact.id"
                  :label="contact.name"
                  :value="contact.name"
                >
                  <div class="contact-option">
                    <el-avatar :size="24" :src="contact.avatar">
                      <el-icon><User /></el-icon>
                    </el-avatar>
                    <span class="contact-name">{{ contact.name }}</span>
                    <span v-if="contact.remark" class="contact-remark">({{ contact.remark }})</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="消息内容" prop="message">
          <el-input
            v-model="messageForm.message"
            type="textarea"
            :rows="4"
            placeholder="请输入要发送的消息内容"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            @click="sendMessage"
            :loading="sending"
            size="large"
          >
            <el-icon><Promotion /></el-icon>
            {{ sending ? '发送中...' : '发送消息' }}
          </el-button>
          
          <el-button @click="resetForm" size="large">
            <el-icon><RefreshLeft /></el-icon>
            重置
          </el-button>
          
          <el-button type="success" @click="sendTestMessage" size="large">
            <el-icon><ChatDotRound /></el-icon>
            发送测试消息
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 快速消息模板 -->
    <el-card class="templates-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Document /></el-icon>
          <span>快速消息模板</span>
          <el-button type="text" size="small" @click="showAddTemplate">
            <el-icon><Plus /></el-icon>
            添加模板
          </el-button>
        </div>
      </template>
      
      <div class="templates-grid">
        <div
          v-for="template in messageTemplates"
          :key="template.id"
          class="template-item"
          @click="useTemplate(template)"
        >
          <div class="template-title">{{ template.title }}</div>
          <div class="template-content">{{ template.content }}</div>
          <div class="template-actions">
            <el-button type="text" size="small" @click.stop="editTemplate(template)">
              <el-icon><Edit /></el-icon>
            </el-button>
            <el-button type="text" size="small" @click.stop="deleteTemplate(template)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
    </el-card>
    
    <!-- 消息监控管理 -->
    <el-card class="monitoring-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Monitor /></el-icon>
          <span>消息监控</span>
          <div class="header-actions">
            <el-tag :type="monitoringStatus.isRunning ? 'success' : 'info'" size="small">
              {{ monitoringStatus.isRunning ? '监控中' : '已停止' }}
            </el-tag>
          </div>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form label-width="100px">
            <el-form-item label="监控时长">
              <el-select v-model="monitoringConfig.duration" style="width: 100%">
                <el-option label="30分钟" value="30m" />
                <el-option label="1小时" value="1h" />
                <el-option label="2小时" value="2h" />
                <el-option label="6小时" value="6h" />
                <el-option label="12小时" value="12h" />
                <el-option label="24小时" value="24h" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="自动回复">
              <el-input
                v-model="monitoringConfig.autoReplyMessage"
                placeholder="请输入自动回复内容"
                maxlength="200"
                show-word-limit
              />
            </el-form-item>
            
            <el-form-item>
              <el-button
                v-if="!monitoringStatus.isRunning"
                type="primary"
                @click="startMonitoring"
                :loading="monitoringLoading"
              >
                <el-icon><VideoPlay /></el-icon>
                开始监控
              </el-button>
              
              <el-button
                v-else
                type="danger"
                @click="stopMonitoring"
                :loading="monitoringLoading"
              >
                <el-icon><VideoPause /></el-icon>
                停止监控
              </el-button>
              
              <el-button @click="refreshMonitoringStatus">
                <el-icon><Refresh /></el-icon>
                刷新状态
              </el-button>
            </el-form-item>
          </el-form>
        </el-col>
        
        <el-col :span="12">
          <div class="monitoring-info">
            <h4>监控信息</h4>
            <div class="info-item">
              <span class="label">状态：</span>
              <span :class="monitoringStatus.isRunning ? 'status-running' : 'status-stopped'">
                {{ monitoringStatus.isRunning ? '运行中' : '已停止' }}
              </span>
            </div>
            <div class="info-item" v-if="monitoringStatus.startTime">
              <span class="label">开始时间：</span>
              <span>{{ formatTime(monitoringStatus.startTime) }}</span>
            </div>
            <div class="info-item" v-if="monitoringStatus.duration">
              <span class="label">监控时长：</span>
              <span>{{ monitoringStatus.duration }}</span>
            </div>
            <div class="info-item">
              <span class="label">处理消息数：</span>
              <span>{{ monitoringStatus.processedCount || 0 }}</span>
            </div>
            <div class="info-item">
              <span class="label">自动回复数：</span>
              <span>{{ monitoringStatus.replyCount || 0 }}</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 消息历史 -->
    <el-card class="history-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Clock /></el-icon>
          <span>消息历史</span>
          <el-button type="text" size="small" @click="refreshHistory">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>
      
      <div class="history-filters">
        <el-date-picker
          v-model="historyFilters.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          size="small"
          @change="filterHistory"
        />
        
        <el-select
          v-model="historyFilters.type"
          placeholder="消息类型"
          size="small"
          style="width: 120px"
          @change="filterHistory"
        >
          <el-option label="全部" value="" />
          <el-option label="好友" value="friend" />
          <el-option label="群聊" value="group" />
        </el-select>
        
        <el-input
          v-model="historyFilters.keyword"
          placeholder="搜索关键词"
          size="small"
          style="width: 200px"
          @input="filterHistory"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      
      <el-table
        :data="filteredHistory"
        style="width: 100%"
        :loading="historyLoading"
        empty-text="暂无消息记录"
      >
        <el-table-column prop="timestamp" label="时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.timestamp) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="type" label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="row.type === 'friend' ? 'primary' : 'success'" size="small">
              {{ row.type === 'friend' ? '好友' : '群聊' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="target" label="接收方" width="150" />
        
        <el-table-column prop="message" label="消息内容" min-width="200">
          <template #default="{ row }">
            <div class="message-content">
              {{ row.message }}
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 'success' ? 'success' : 'danger'" size="small">
              {{ row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="text" size="small" @click="resendMessage(row)">
              <el-icon><Refresh /></el-icon>
              重发
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 添加/编辑模板对话框 -->
    <el-dialog
      v-model="templateDialog.visible"
      :title="templateDialog.isEdit ? '编辑模板' : '添加模板'"
      width="500px"
    >
      <el-form
        ref="templateFormRef"
        :model="templateDialog.form"
        :rules="templateRules"
        label-width="80px"
      >
        <el-form-item label="模板名称" prop="title">
          <el-input v-model="templateDialog.form.title" placeholder="请输入模板名称" />
        </el-form-item>
        
        <el-form-item label="模板内容" prop="content">
          <el-input
            v-model="templateDialog.form.content"
            type="textarea"
            :rows="4"
            placeholder="请输入模板内容"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="templateDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveTemplate">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ChatDotRound,
  User,
  Promotion,
  RefreshLeft,
  Document,
  Plus,
  Edit,
  Delete,
  Clock,
  Refresh,
  Search,
  Monitor,
  VideoPlay,
  VideoPause
} from '@element-plus/icons-vue'
import { messageAPI, contactAPI } from '@/api'

const messageFormRef = ref()
const templateFormRef = ref()

const sending = ref(false)
const contactsLoading = ref(false)
const historyLoading = ref(false)

const messageForm = reactive({
  type: 'friend',
  target: '',
  message: ''
})

const messageRules = {
  type: [{ required: true, message: '请选择消息类型', trigger: 'change' }],
  target: [{ required: true, message: '请选择接收方', trigger: 'change' }],
  message: [{ required: true, message: '请输入消息内容', trigger: 'blur' }]
}

const friends = ref([
  { id: 1, name: '张三', remark: '同事', avatar: '' },
  { id: 2, name: '李四', remark: '朋友', avatar: '' },
  { id: 3, name: '王五', remark: '', avatar: '' }
])

const groups = ref([
  { id: 1, name: '工作群', avatar: '' },
  { id: 2, name: '朋友圈', avatar: '' },
  { id: 3, name: '家庭群', avatar: '' }
])

const currentContacts = computed(() => {
  return messageForm.type === 'friend' ? friends.value : groups.value
})

const messageTemplates = ref([
  { id: 1, title: '问候语', content: '你好！最近怎么样？' },
  { id: 2, title: '工作提醒', content: '请注意查收最新的工作安排，谢谢！' },
  { id: 3, title: '会议通知', content: '明天上午10点开会，请准时参加。' }
])

const messageHistory = ref([
  {
    id: 1,
    timestamp: new Date().toISOString(),
    type: 'friend',
    target: '张三',
    message: '你好，最近怎么样？',
    status: 'success'
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 3600000).toISOString(),
    type: 'group',
    target: '工作群',
    message: '大家好，今天的工作安排已经发布。',
    status: 'success'
  }
])

const historyFilters = reactive({
  dateRange: [],
  type: '',
  keyword: ''
})

const filteredHistory = computed(() => {
  let result = messageHistory.value
  
  if (historyFilters.type) {
    result = result.filter(item => item.type === historyFilters.type)
  }
  
  if (historyFilters.keyword) {
    result = result.filter(item => 
      item.target.includes(historyFilters.keyword) ||
      item.message.includes(historyFilters.keyword)
    )
  }
  
  return result
})

const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

const templateDialog = reactive({
  visible: false,
  isEdit: false,
  form: {
    id: null,
    title: '',
    content: ''
  }
})

const templateRules = {
  title: [{ required: true, message: '请输入模板名称', trigger: 'blur' }],
  content: [{ required: true, message: '请输入模板内容', trigger: 'blur' }]
}

// 监控相关数据
const monitoringLoading = ref(false)
const monitoringConfig = reactive({
  duration: '1h',
  autoReplyMessage: '恭喜发财'
})

const monitoringStatus = reactive({
  isRunning: false,
  startTime: null,
  duration: null,
  processedCount: 0,
  replyCount: 0
})

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString('zh-CN')
}

const onTypeChange = () => {
  messageForm.target = ''
}

const sendMessage = async () => {
  if (!messageFormRef.value) return
  
  try {
    const valid = await messageFormRef.value.validate()
    if (!valid) return
    
    sending.value = true
    
    // 调用发送消息API
    const result = await messageAPI.sendMessage({
      type: messageForm.type,
      target: messageForm.target,
      message: messageForm.message
    })
    
    ElMessage.success('消息发送成功')
    
    // 添加到历史记录
    messageHistory.value.unshift({
      id: Date.now(),
      timestamp: new Date().toISOString(),
      type: messageForm.type,
      target: messageForm.target,
      message: messageForm.message,
      status: 'success'
    })
    
    // 重置表单
    resetForm()
  } catch (error) {
    ElMessage.error('消息发送失败')
  } finally {
    sending.value = false
  }
}

const sendTestMessage = async () => {
  try {
    sending.value = true
    
    // 发送测试消息
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('测试消息发送成功')
  } catch (error) {
    ElMessage.error('测试消息发送失败')
  } finally {
    sending.value = false
  }
}

const resetForm = () => {
  if (messageFormRef.value) {
    messageFormRef.value.resetFields()
  }
}

const useTemplate = (template) => {
  messageForm.message = template.content
}

const showAddTemplate = () => {
  templateDialog.isEdit = false
  templateDialog.form = {
    id: null,
    title: '',
    content: ''
  }
  templateDialog.visible = true
}

const editTemplate = (template) => {
  templateDialog.isEdit = true
  templateDialog.form = { ...template }
  templateDialog.visible = true
}

const saveTemplate = async () => {
  if (!templateFormRef.value) return
  
  try {
    const valid = await templateFormRef.value.validate()
    if (!valid) return
    
    if (templateDialog.isEdit) {
      // 编辑模板
      const index = messageTemplates.value.findIndex(t => t.id === templateDialog.form.id)
      if (index !== -1) {
        messageTemplates.value[index] = { ...templateDialog.form }
      }
      ElMessage.success('模板更新成功')
    } else {
      // 添加模板
      messageTemplates.value.push({
        id: Date.now(),
        title: templateDialog.form.title,
        content: templateDialog.form.content
      })
      ElMessage.success('模板添加成功')
    }
    
    templateDialog.visible = false
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const deleteTemplate = async (template) => {
  try {
    await ElMessageBox.confirm('确定要删除这个模板吗？', '确认删除', {
      type: 'warning'
    })
    
    const index = messageTemplates.value.findIndex(t => t.id === template.id)
    if (index !== -1) {
      messageTemplates.value.splice(index, 1)
      ElMessage.success('模板删除成功')
    }
  } catch {
    // 用户取消
  }
}

// 监控相关方法
const startMonitoring = async () => {
  try {
    monitoringLoading.value = true
    
    // 先设置自动回复消息
    await messageAPI.setAutoReply({
      message: monitoringConfig.autoReplyMessage
    })
    
    // 启动监控
    const result = await messageAPI.startMonitoring({
      duration: monitoringConfig.duration
    })
    
    if (result.success) {
      monitoringStatus.isRunning = true
      monitoringStatus.startTime = new Date().toISOString()
      monitoringStatus.duration = monitoringConfig.duration
      ElMessage.success('消息监控已启动')
    } else {
      ElMessage.error(result.error || '启动监控失败')
    }
  } catch (error) {
    ElMessage.error('启动监控失败：' + error.message)
  } finally {
    monitoringLoading.value = false
  }
}

const stopMonitoring = async () => {
  try {
    monitoringLoading.value = true
    
    const result = await messageAPI.stopMonitoring()
    
    if (result.success) {
      monitoringStatus.isRunning = false
      monitoringStatus.startTime = null
      monitoringStatus.duration = null
      ElMessage.success('消息监控已停止')
    } else {
      ElMessage.error(result.error || '停止监控失败')
    }
  } catch (error) {
    ElMessage.error('停止监控失败：' + error.message)
  } finally {
    monitoringLoading.value = false
  }
}

const refreshMonitoringStatus = async () => {
  try {
    const result = await messageAPI.getMonitoringStatus()
    
    if (result.success) {
      Object.assign(monitoringStatus, result.data)
    } else {
      ElMessage.error('获取监控状态失败')
    }
  } catch (error) {
    ElMessage.error('获取监控状态失败：' + error.message)
  }
}

const refreshHistory = () => {
  historyLoading.value = true
  setTimeout(() => {
    historyLoading.value = false
    ElMessage.success('历史记录刷新成功')
  }, 1000)
}

const filterHistory = () => {
  // 过滤逻辑已在computed中实现
}

const resendMessage = async (row) => {
  try {
    await ElMessageBox.confirm('确定要重新发送这条消息吗？', '确认重发')
    
    // 重新发送消息
    messageForm.type = row.type
    messageForm.target = row.target
    messageForm.message = row.message
    
    await sendMessage()
  } catch {
    // 用户取消
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  // 重新加载数据
}

const handleCurrentChange = (current) => {
  pagination.current = current
  // 重新加载数据
}

const loadContacts = async () => {
  contactsLoading.value = true
  try {
    // 模拟加载联系人数据
    await new Promise(resolve => setTimeout(resolve, 500))
    // const result = await contactAPI.getContacts()
    // friends.value = result.friends
    // groups.value = result.groups
  } catch (error) {
    ElMessage.error('加载联系人失败')
  } finally {
    contactsLoading.value = false
  }
}

onMounted(() => {
  loadContacts()
  pagination.total = messageHistory.value.length
  
  // 检查监控状态
  refreshMonitoringStatus()
})
</script>

<style scoped>
.message-page {
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

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.send-card {
  margin-bottom: 24px;
}

.message-form {
  max-width: 800px;
}

.contact-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-name {
  font-weight: 500;
}

.contact-remark {
  color: #909399;
  font-size: 12px;
}

.templates-card {
  margin-bottom: 24px;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.template-item {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.template-item:hover {
  border-color: #409EFF;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
}

.template-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.template-content {
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 8px;
}

.template-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.3s;
}

.template-item:hover .template-actions {
  opacity: 1;
}

.history-card {
  margin-bottom: 24px;
}

.history-filters {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.message-content {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pagination-wrapper {
  margin-top: 16px;
  text-align: right;
}

@media (max-width: 768px) {
  .templates-grid {
    grid-template-columns: 1fr;
  }
  
  .history-filters {
    flex-direction: column;
  }
  
  .pagination-wrapper {
    text-align: center;
  }
}

/* 监控相关样式 */
.monitoring-card {
  margin-bottom: 24px;
}

.monitoring-info {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.monitoring-info h4 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 14px;
  font-weight: 600;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 13px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-item .label {
  color: #666;
  font-weight: 500;
}

.status-running {
  color: #67c23a;
  font-weight: 600;
}

.status-stopped {
  color: #909399;
  font-weight: 600;
}

.header-actions {
  margin-left: auto;
}
</style>