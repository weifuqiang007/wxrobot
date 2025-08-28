<template>
  <div class="news-page">
    <div class="page-header">
      <h1 class="page-title">新闻推送管理</h1>
      <p class="page-description">管理新闻推送设置和推送群组</p>
    </div>
    
    <!-- 推送状态卡片 -->
    <div class="status-grid">
      <el-card class="status-card" shadow="hover">
        <div class="status-content">
          <div class="status-icon service-icon">
            <el-icon><Bell /></el-icon>
          </div>
          <div class="status-info">
            <div class="status-title">推送服务</div>
            <div class="status-value">
              <el-tag :type="newsService.status === 'running' ? 'success' : 'danger'">
                {{ newsService.status === 'running' ? '运行中' : '已停止' }}
              </el-tag>
            </div>
          </div>
          <div class="status-actions">
            <el-button
              :type="newsService.status === 'running' ? 'danger' : 'success'"
              size="small"
              @click="toggleNewsService"
              :loading="serviceLoading"
            >
              {{ newsService.status === 'running' ? '停止' : '启动' }}
            </el-button>
          </div>
        </div>
      </el-card>
      
      <el-card class="status-card" shadow="hover">
        <div class="status-content">
          <div class="status-icon groups-icon">
            <el-icon><UserFilled /></el-icon>
          </div>
          <div class="status-info">
            <div class="status-title">推送群组</div>
            <div class="status-value">{{ newsGroups.length }} 个</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="status-card" shadow="hover">
        <div class="status-content">
          <div class="status-icon time-icon">
            <el-icon><Clock /></el-icon>
          </div>
          <div class="status-info">
            <div class="status-title">推送时间</div>
            <div class="status-value">{{ newsSettings.pushTime || '未设置' }}</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="status-card" shadow="hover">
        <div class="status-content">
          <div class="status-icon count-icon">
            <el-icon><DataAnalysis /></el-icon>
          </div>
          <div class="status-info">
            <div class="status-title">今日推送</div>
            <div class="status-value">{{ todayPushCount }} 次</div>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 推送设置 -->
    <el-card class="settings-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Setting /></el-icon>
          <span>推送设置</span>
        </div>
      </template>
      
      <el-form
        ref="settingsFormRef"
        :model="newsSettings"
        :rules="settingsRules"
        label-width="120px"
        class="settings-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="推送时间" prop="pushTime">
              <el-time-picker
                v-model="newsSettings.pushTime"
                format="HH:mm"
                placeholder="选择推送时间"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="推送间隔" prop="interval">
              <el-select v-model="newsSettings.interval" placeholder="选择推送间隔" style="width: 100%">
                <el-option label="每天" value="daily" />
                <el-option label="每周" value="weekly" />
                <el-option label="工作日" value="weekdays" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="新闻源" prop="newsSource">
              <el-select v-model="newsSettings.newsSource" placeholder="选择新闻源" style="width: 100%">
                <el-option label="新华网" value="xinhua" />
                <el-option label="人民网" value="people" />
                <el-option label="央视新闻" value="cctv" />
                <el-option label="澎湃新闻" value="thepaper" />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="新闻数量" prop="newsCount">
              <el-input-number
                v-model="newsSettings.newsCount"
                :min="1"
                :max="10"
                placeholder="每次推送新闻数量"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="推送模板" prop="template">
          <el-input
            v-model="newsSettings.template"
            type="textarea"
            :rows="4"
            placeholder="推送消息模板，使用 {title}、{summary}、{url} 作为占位符"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="saveSettings" :loading="savingSettings">
            <el-icon><Check /></el-icon>
            保存设置
          </el-button>
          
          <el-button @click="resetSettings">
            <el-icon><RefreshLeft /></el-icon>
            重置
          </el-button>
          
          <el-button type="success" @click="testPush" :loading="testing">
            <el-icon><Promotion /></el-icon>
            测试推送
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 推送群组管理 -->
    <el-card class="groups-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon><UserFilled /></el-icon>
            <span>推送群组</span>
          </div>
          <div class="header-right">
            <el-button type="primary" @click="showAddGroup">
              <el-icon><Plus /></el-icon>
              添加群组
            </el-button>
            <el-button @click="refreshGroups" :loading="groupsLoading">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </template>
      
      <div class="groups-search">
        <el-input
          v-model="groupSearchKeyword"
          placeholder="搜索群组名称"
          @input="handleGroupSearch"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      
      <el-table
        :data="filteredGroups"
        style="width: 100%"
        :loading="groupsLoading"
        empty-text="暂无推送群组"
        @selection-change="handleGroupSelection"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="群头像" width="80">
          <template #default="{ row }">
            <el-avatar :size="40" :src="row.avatar">
              <el-icon><UserFilled /></el-icon>
            </el-avatar>
          </template>
        </el-table-column>
        
        <el-table-column prop="name" label="群名称" min-width="150" />
        
        <el-table-column prop="memberCount" label="成员数" width="100">
          <template #default="{ row }">
            {{ row.memberCount }}人
          </template>
        </el-table-column>
        
        <el-table-column label="推送状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.enabled"
              @change="toggleGroupStatus(row)"
              active-text="启用"
              inactive-text="禁用"
            />
          </template>
        </el-table-column>
        
        <el-table-column prop="addTime" label="添加时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.addTime) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="lastPush" label="最近推送" width="160">
          <template #default="{ row }">
            <span v-if="row.lastPush">{{ formatTime(row.lastPush) }}</span>
            <span v-else class="no-push">从未推送</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="text" size="small" @click="testGroupPush(row)">
              <el-icon><Promotion /></el-icon>
              测试
            </el-button>
            
            <el-button type="text" size="small" @click="removeGroup(row)">
              <el-icon><Delete /></el-icon>
              移除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 批量操作 -->
      <div v-if="selectedGroups.length > 0" class="batch-actions">
        <div class="batch-info">
          已选择 {{ selectedGroups.length }} 个群组
        </div>
        <div class="batch-buttons">
          <el-button type="success" @click="batchEnable">
            <el-icon><Check /></el-icon>
            批量启用
          </el-button>
          <el-button @click="batchDisable">
            <el-icon><Close /></el-icon>
            批量禁用
          </el-button>
          <el-button type="primary" @click="batchTest">
            <el-icon><Promotion /></el-icon>
            批量测试
          </el-button>
          <el-button type="danger" @click="batchRemove">
            <el-icon><Delete /></el-icon>
            批量移除
          </el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 推送历史 -->
    <el-card class="history-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Clock /></el-icon>
          <span>推送历史</span>
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
          v-model="historyFilters.status"
          placeholder="推送状态"
          size="small"
          style="width: 120px"
          @change="filterHistory"
        >
          <el-option label="全部" value="" />
          <el-option label="成功" value="success" />
          <el-option label="失败" value="failed" />
        </el-select>
        
        <el-input
          v-model="historyFilters.keyword"
          placeholder="搜索群组或内容"
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
        empty-text="暂无推送记录"
      >
        <el-table-column prop="timestamp" label="推送时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.timestamp) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="groupName" label="推送群组" width="150" />
        
        <el-table-column prop="newsTitle" label="新闻标题" min-width="200">
          <template #default="{ row }">
            <div class="news-title">
              {{ row.newsTitle }}
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
        
        <el-table-column prop="errorMsg" label="错误信息" width="150">
          <template #default="{ row }">
            <span v-if="row.errorMsg" class="error-msg">{{ row.errorMsg }}</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="text" size="small" @click="viewNewsDetail(row)">
              <el-icon><View /></el-icon>
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="historyPagination.current"
          v-model:page-size="historyPagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="historyPagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleHistorySizeChange"
          @current-change="handleHistoryCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 添加群组对话框 -->
    <el-dialog
      v-model="addGroupDialog.visible"
      title="添加推送群组"
      width="500px"
    >
      <div class="available-groups">
        <div class="search-groups">
          <el-input
            v-model="addGroupDialog.searchKeyword"
            placeholder="搜索可用群组"
            @input="searchAvailableGroups"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        
        <div class="groups-list">
          <div
            v-for="group in addGroupDialog.availableGroups"
            :key="group.id"
            class="group-item"
            :class="{ selected: addGroupDialog.selectedGroups.includes(group.id) }"
            @click="toggleGroupSelection(group)"
          >
            <el-avatar :size="32" :src="group.avatar">
              <el-icon><UserFilled /></el-icon>
            </el-avatar>
            <div class="group-info">
              <div class="group-name">{{ group.name }}</div>
              <div class="group-members">{{ group.memberCount }}人</div>
            </div>
            <el-icon v-if="addGroupDialog.selectedGroups.includes(group.id)" class="check-icon">
              <Check />
            </el-icon>
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="addGroupDialog.visible = false">取消</el-button>
        <el-button
          type="primary"
          @click="addSelectedGroups"
          :disabled="addGroupDialog.selectedGroups.length === 0"
        >
          添加 ({{ addGroupDialog.selectedGroups.length }})
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 新闻详情对话框 -->
    <el-dialog
      v-model="newsDetailDialog.visible"
      title="新闻详情"
      width="600px"
    >
      <div v-if="newsDetailDialog.news" class="news-detail">
        <h3>{{ newsDetailDialog.news.newsTitle }}</h3>
        <div class="news-meta">
          <span>推送时间：{{ formatTime(newsDetailDialog.news.timestamp) }}</span>
          <span>推送群组：{{ newsDetailDialog.news.groupName }}</span>
          <span>状态：
            <el-tag :type="newsDetailDialog.news.status === 'success' ? 'success' : 'danger'" size="small">
              {{ newsDetailDialog.news.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </span>
        </div>
        <div class="news-content">
          <p>{{ newsDetailDialog.news.content || '暂无内容' }}</p>
        </div>
        <div v-if="newsDetailDialog.news.url" class="news-link">
          <el-link :href="newsDetailDialog.news.url" target="_blank" type="primary">
            查看原文
          </el-link>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="newsDetailDialog.visible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { newsAPI } from '@/api'

const settingsFormRef = ref()

const serviceLoading = ref(false)
const savingSettings = ref(false)
const testing = ref(false)
const groupsLoading = ref(false)
const historyLoading = ref(false)

const newsService = reactive({
  status: 'running'
})

const newsSettings = reactive({
  pushTime: '09:00',
  interval: 'daily',
  newsSource: 'xinhua',
  newsCount: 3,
  template: '📰 今日新闻推送\n\n标题：{title}\n摘要：{summary}\n链接：{url}'
})

const settingsRules = {
  pushTime: [{ required: true, message: '请选择推送时间', trigger: 'change' }],
  interval: [{ required: true, message: '请选择推送间隔', trigger: 'change' }],
  newsSource: [{ required: true, message: '请选择新闻源', trigger: 'change' }],
  newsCount: [{ required: true, message: '请输入新闻数量', trigger: 'blur' }],
  template: [{ required: true, message: '请输入推送模板', trigger: 'blur' }]
}

const newsGroups = ref([
  {
    id: 1,
    name: '工作群',
    avatar: '',
    memberCount: 25,
    enabled: true,
    addTime: '2024-01-15T10:30:00Z',
    lastPush: '2024-01-20T09:00:00Z'
  },
  {
    id: 2,
    name: '朋友圈',
    avatar: '',
    memberCount: 12,
    enabled: false,
    addTime: '2024-01-10T14:20:00Z',
    lastPush: null
  }
])

const groupSearchKeyword = ref('')
const selectedGroups = ref([])

const filteredGroups = computed(() => {
  if (!groupSearchKeyword.value) {
    return newsGroups.value
  }
  return newsGroups.value.filter(group => 
    group.name.includes(groupSearchKeyword.value)
  )
})

const todayPushCount = ref(5)

const pushHistory = ref([
  {
    id: 1,
    timestamp: '2024-01-20T09:00:00Z',
    groupName: '工作群',
    newsTitle: '国内外重要新闻动态',
    content: '今日国内外重要新闻动态摘要...',
    url: 'https://example.com/news/1',
    status: 'success',
    errorMsg: null
  },
  {
    id: 2,
    timestamp: '2024-01-19T09:00:00Z',
    groupName: '朋友圈',
    newsTitle: '科技前沿资讯',
    content: '最新科技前沿资讯...',
    url: 'https://example.com/news/2',
    status: 'failed',
    errorMsg: '群组不存在'
  }
])

const historyFilters = reactive({
  dateRange: [],
  status: '',
  keyword: ''
})

const filteredHistory = computed(() => {
  let result = pushHistory.value
  
  if (historyFilters.status) {
    result = result.filter(item => item.status === historyFilters.status)
  }
  
  if (historyFilters.keyword) {
    result = result.filter(item => 
      item.groupName.includes(historyFilters.keyword) ||
      item.newsTitle.includes(historyFilters.keyword)
    )
  }
  
  return result
})

const historyPagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

const addGroupDialog = reactive({
  visible: false,
  searchKeyword: '',
  selectedGroups: [],
  availableGroups: [
    { id: 3, name: '技术交流群', avatar: '', memberCount: 30 },
    { id: 4, name: '产品讨论组', avatar: '', memberCount: 15 },
    { id: 5, name: '市场营销群', avatar: '', memberCount: 20 }
  ]
})

const newsDetailDialog = reactive({
  visible: false,
  news: null
})

const formatTime = (timestamp) => {
  if (!timestamp) return '-'
  return new Date(timestamp).toLocaleString('zh-CN')
}

const toggleNewsService = async () => {
  serviceLoading.value = true
  try {
    // 模拟切换服务状态
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    newsService.status = newsService.status === 'running' ? 'stopped' : 'running'
    ElMessage.success(`新闻推送服务已${newsService.status === 'running' ? '启动' : '停止'}`)
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    serviceLoading.value = false
  }
}

const saveSettings = async () => {
  if (!settingsFormRef.value) return
  
  try {
    const valid = await settingsFormRef.value.validate()
    if (!valid) return
    
    savingSettings.value = true
    
    // 调用保存设置API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('设置保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    savingSettings.value = false
  }
}

const resetSettings = () => {
  if (settingsFormRef.value) {
    settingsFormRef.value.resetFields()
  }
}

const testPush = async () => {
  testing.value = true
  try {
    // 模拟测试推送
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    ElMessage.success('测试推送成功')
  } catch (error) {
    ElMessage.error('测试推送失败')
  } finally {
    testing.value = false
  }
}

const handleGroupSearch = () => {
  // 搜索逻辑已在computed中实现
}

const handleGroupSelection = (selection) => {
  selectedGroups.value = selection
}

const toggleGroupStatus = async (group) => {
  try {
    // 模拟切换群组状态
    await new Promise(resolve => setTimeout(resolve, 500))
    
    ElMessage.success(`${group.name} 推送状态已${group.enabled ? '启用' : '禁用'}`)
  } catch (error) {
    // 恢复状态
    group.enabled = !group.enabled
    ElMessage.error('操作失败')
  }
}

const testGroupPush = async (group) => {
  try {
    // 模拟群组测试推送
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success(`${group.name} 测试推送成功`)
    
    // 更新最近推送时间
    group.lastPush = new Date().toISOString()
  } catch (error) {
    ElMessage.error('测试推送失败')
  }
}

const removeGroup = async (group) => {
  try {
    await ElMessageBox.confirm(`确定要移除群组 ${group.name} 吗？`, '确认移除', {
      type: 'warning'
    })
    
    const index = newsGroups.value.findIndex(g => g.id === group.id)
    if (index !== -1) {
      newsGroups.value.splice(index, 1)
    }
    
    ElMessage.success('群组移除成功')
  } catch {
    // 用户取消
  }
}

const refreshGroups = async () => {
  groupsLoading.value = true
  try {
    // 模拟刷新群组数据
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('群组列表刷新成功')
  } catch (error) {
    ElMessage.error('刷新失败')
  } finally {
    groupsLoading.value = false
  }
}

const showAddGroup = () => {
  addGroupDialog.visible = true
  addGroupDialog.selectedGroups = []
  addGroupDialog.searchKeyword = ''
}

const searchAvailableGroups = () => {
  // 搜索可用群组的逻辑
}

const toggleGroupSelection = (group) => {
  const index = addGroupDialog.selectedGroups.indexOf(group.id)
  if (index > -1) {
    addGroupDialog.selectedGroups.splice(index, 1)
  } else {
    addGroupDialog.selectedGroups.push(group.id)
  }
}

const addSelectedGroups = () => {
  const selectedGroupsData = addGroupDialog.availableGroups.filter(group => 
    addGroupDialog.selectedGroups.includes(group.id)
  )
  
  selectedGroupsData.forEach(group => {
    newsGroups.value.push({
      ...group,
      enabled: true,
      addTime: new Date().toISOString(),
      lastPush: null
    })
  })
  
  // 从可用群组中移除已添加的
  addGroupDialog.availableGroups = addGroupDialog.availableGroups.filter(group => 
    !addGroupDialog.selectedGroups.includes(group.id)
  )
  
  ElMessage.success(`成功添加 ${selectedGroupsData.length} 个群组`)
  addGroupDialog.visible = false
}

const batchEnable = () => {
  selectedGroups.value.forEach(group => {
    group.enabled = true
  })
  ElMessage.success(`已启用 ${selectedGroups.value.length} 个群组`)
}

const batchDisable = () => {
  selectedGroups.value.forEach(group => {
    group.enabled = false
  })
  ElMessage.success(`已禁用 ${selectedGroups.value.length} 个群组`)
}

const batchTest = async () => {
  try {
    // 模拟批量测试
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    selectedGroups.value.forEach(group => {
      group.lastPush = new Date().toISOString()
    })
    
    ElMessage.success(`${selectedGroups.value.length} 个群组测试推送完成`)
  } catch (error) {
    ElMessage.error('批量测试失败')
  }
}

const batchRemove = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要移除选中的 ${selectedGroups.value.length} 个群组吗？`,
      '批量移除',
      { type: 'warning' }
    )
    
    selectedGroups.value.forEach(group => {
      const index = newsGroups.value.findIndex(g => g.id === group.id)
      if (index !== -1) {
        newsGroups.value.splice(index, 1)
      }
    })
    
    selectedGroups.value = []
    ElMessage.success('批量移除成功')
  } catch {
    // 用户取消
  }
}

const refreshHistory = async () => {
  historyLoading.value = true
  try {
    // 模拟刷新历史数据
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('推送历史刷新成功')
  } catch (error) {
    ElMessage.error('刷新失败')
  } finally {
    historyLoading.value = false
  }
}

const filterHistory = () => {
  // 过滤逻辑已在computed中实现
}

const viewNewsDetail = (news) => {
  newsDetailDialog.news = news
  newsDetailDialog.visible = true
}

const handleHistorySizeChange = (size) => {
  historyPagination.size = size
  historyPagination.current = 1
}

const handleHistoryCurrentChange = (current) => {
  historyPagination.current = current
}

onMounted(() => {
  historyPagination.total = pushHistory.value.length
})
</script>

<style scoped>
.news-page {
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

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.status-card {
  border: none;
}

.status-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.service-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.groups-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.time-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.count-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.status-info {
  flex: 1;
}

.status-title {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 4px;
}

.status-value {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.status-actions {
  margin-left: auto;
}

.settings-card,
.groups-card,
.history-card {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.header-right {
  display: flex;
  gap: 8px;
}

.settings-form {
  max-width: 800px;
}

.groups-search {
  margin-bottom: 16px;
}

.no-push {
  color: #c0c4cc;
}

.batch-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 16px 0;
}

.batch-info {
  color: #606266;
  font-weight: 500;
}

.batch-buttons {
  display: flex;
  gap: 8px;
}

.history-filters {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.news-title {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.error-msg {
  color: #f56c6c;
  font-size: 12px;
}

.pagination-wrapper {
  margin-top: 16px;
  text-align: right;
}

.available-groups {
  max-height: 400px;
}

.search-groups {
  margin-bottom: 16px;
}

.groups-list {
  max-height: 300px;
  overflow-y: auto;
}

.group-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.group-item:hover {
  border-color: #409EFF;
  background: #f0f9ff;
}

.group-item.selected {
  border-color: #409EFF;
  background: #e6f7ff;
}

.group-info {
  flex: 1;
}

.group-name {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.group-members {
  color: #7f8c8d;
  font-size: 12px;
}

.check-icon {
  color: #409EFF;
  font-size: 18px;
}

.news-detail {
  padding: 16px 0;
}

.news-detail h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  line-height: 1.5;
}

.news-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  font-size: 14px;
  color: #606266;
}

.news-content {
  margin-bottom: 16px;
  line-height: 1.6;
  color: #2c3e50;
}

.news-link {
  text-align: center;
}

@media (max-width: 768px) {
  .status-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .history-filters {
    flex-direction: column;
  }
  
  .batch-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .pagination-wrapper {
    text-align: center;
  }
  
  .news-meta {
    font-size: 12px;
  }
}
</style>