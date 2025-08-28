<template>
  <div class="contact-page">
    <div class="page-header">
      <h1 class="page-title">联系人管理</h1>
      <p class="page-description">管理微信好友和群聊</p>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon friend-icon">
            <el-icon><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ friends.length }}</div>
            <div class="stat-label">好友总数</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon group-icon">
            <el-icon><UserFilled /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ groups.length }}</div>
            <div class="stat-label">群聊总数</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon online-icon">
            <el-icon><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ onlineFriends }}</div>
            <div class="stat-label">在线好友</div>
          </div>
        </div>
      </el-card>
      
      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon active-icon">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ activeGroups }}</div>
            <div class="stat-label">活跃群聊</div>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 联系人列表 -->
    <el-card class="contacts-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon><Notebook /></el-icon>
            <span>联系人列表</span>
          </div>
          <div class="header-right">
            <el-button type="primary" @click="refreshContacts" :loading="loading">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
            <el-button type="success" @click="syncContacts" :loading="syncing">
              <el-icon><Download /></el-icon>
              同步联系人
            </el-button>
          </div>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="filters-section">
        <div class="search-bar">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索联系人姓名、备注或群名"
            @input="handleSearch"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        
        <div class="filter-tabs">
          <el-radio-group v-model="activeTab" @change="handleTabChange">
            <el-radio-button label="all">全部 ({{ allContacts.length }})</el-radio-button>
            <el-radio-button label="friends">好友 ({{ friends.length }})</el-radio-button>
            <el-radio-button label="groups">群聊 ({{ groups.length }})</el-radio-button>
          </el-radio-group>
        </div>
        
        <div class="filter-options">
          <el-select
            v-model="sortBy"
            placeholder="排序方式"
            style="width: 120px"
            @change="handleSort"
          >
            <el-option label="姓名" value="name" />
            <el-option label="最近联系" value="lastContact" />
            <el-option label="添加时间" value="addTime" />
          </el-select>
          
          <el-select
            v-model="filterStatus"
            placeholder="状态筛选"
            style="width: 120px"
            @change="handleFilter"
          >
            <el-option label="全部" value="" />
            <el-option label="在线" value="online" />
            <el-option label="离线" value="offline" />
          </el-select>
        </div>
      </div>
      
      <!-- 联系人表格 -->
      <el-table
        :data="filteredContacts"
        style="width: 100%"
        :loading="loading"
        empty-text="暂无联系人数据"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="头像" width="80">
          <template #default="{ row }">
            <el-avatar :size="40" :src="row.avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
          </template>
        </el-table-column>
        
        <el-table-column prop="name" label="姓名/群名" min-width="150">
          <template #default="{ row }">
            <div class="contact-name-cell">
              <span class="contact-name">{{ row.name }}</span>
              <el-tag v-if="row.type === 'group'" type="success" size="small">群聊</el-tag>
              <el-tag v-else type="primary" size="small">好友</el-tag>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="remark" label="备注" width="150">
          <template #default="{ row }">
            <span v-if="row.remark">{{ row.remark }}</span>
            <span v-else class="no-remark">-</span>
          </template>
        </el-table-column>
        
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag
              :type="row.status === 'online' ? 'success' : 'info'"
              size="small"
            >
              {{ row.status === 'online' ? '在线' : '离线' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="memberCount" label="成员数" width="100">
          <template #default="{ row }">
            <span v-if="row.type === 'group'">{{ row.memberCount || 0 }}人</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="lastContact" label="最近联系" width="160">
          <template #default="{ row }">
            <span v-if="row.lastContact">{{ formatTime(row.lastContact) }}</span>
            <span v-else class="no-contact">从未联系</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="text" size="small" @click="sendMessage(row)">
              <el-icon><ChatDotRound /></el-icon>
              发消息
            </el-button>
            
            <el-button type="text" size="small" @click="viewDetails(row)">
              <el-icon><View /></el-icon>
              详情
            </el-button>
            
            <el-dropdown @command="handleCommand">
              <el-button type="text" size="small">
                更多<el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="{ action: 'edit', row }">编辑备注</el-dropdown-item>
                  <el-dropdown-item :command="{ action: 'block', row }" v-if="row.type === 'friend'">拉黑</el-dropdown-item>
                  <el-dropdown-item :command="{ action: 'leave', row }" v-if="row.type === 'group'">退出群聊</el-dropdown-item>
                  <el-dropdown-item :command="{ action: 'delete', row }" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 批量操作 -->
      <div v-if="selectedContacts.length > 0" class="batch-actions">
        <div class="batch-info">
          已选择 {{ selectedContacts.length }} 个联系人
        </div>
        <div class="batch-buttons">
          <el-button type="primary" @click="batchSendMessage">
            <el-icon><ChatDotRound /></el-icon>
            批量发消息
          </el-button>
          <el-button @click="batchExport">
            <el-icon><Download /></el-icon>
            导出联系人
          </el-button>
          <el-button type="danger" @click="batchDelete">
            <el-icon><Delete /></el-icon>
            批量删除
          </el-button>
        </div>
      </div>
      
      <!-- 分页 -->
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
    
    <!-- 联系人详情对话框 -->
    <el-dialog
      v-model="detailDialog.visible"
      :title="detailDialog.contact?.name || '联系人详情'"
      width="600px"
    >
      <div v-if="detailDialog.contact" class="contact-detail">
        <div class="detail-header">
          <el-avatar :size="80" :src="detailDialog.contact.avatar">
            <el-icon><User /></el-icon>
          </el-avatar>
          <div class="detail-info">
            <h3>{{ detailDialog.contact.name }}</h3>
            <p v-if="detailDialog.contact.remark" class="remark">备注：{{ detailDialog.contact.remark }}</p>
            <el-tag :type="detailDialog.contact.type === 'group' ? 'success' : 'primary'">
              {{ detailDialog.contact.type === 'group' ? '群聊' : '好友' }}
            </el-tag>
          </div>
        </div>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="微信号">
            {{ detailDialog.contact.wxid || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="detailDialog.contact.status === 'online' ? 'success' : 'info'" size="small">
              {{ detailDialog.contact.status === 'online' ? '在线' : '离线' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="添加时间">
            {{ formatTime(detailDialog.contact.addTime) }}
          </el-descriptions-item>
          <el-descriptions-item label="最近联系">
            {{ detailDialog.contact.lastContact ? formatTime(detailDialog.contact.lastContact) : '从未联系' }}
          </el-descriptions-item>
          <el-descriptions-item v-if="detailDialog.contact.type === 'group'" label="群成员数">
            {{ detailDialog.contact.memberCount || 0 }}人
          </el-descriptions-item>
          <el-descriptions-item v-if="detailDialog.contact.type === 'group'" label="群主">
            {{ detailDialog.contact.owner || '-' }}
          </el-descriptions-item>
        </el-descriptions>
        
        <div v-if="detailDialog.contact.type === 'group'" class="group-members">
          <h4>群成员</h4>
          <div class="members-grid">
            <div
              v-for="member in detailDialog.contact.members || []"
              :key="member.id"
              class="member-item"
            >
              <el-avatar :size="32" :src="member.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span class="member-name">{{ member.name }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="detailDialog.visible = false">关闭</el-button>
        <el-button type="primary" @click="sendMessage(detailDialog.contact)">
          <el-icon><ChatDotRound /></el-icon>
          发送消息
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 编辑备注对话框 -->
    <el-dialog
      v-model="remarkDialog.visible"
      title="编辑备注"
      width="400px"
    >
      <el-form :model="remarkDialog.form" label-width="80px">
        <el-form-item label="联系人">
          <span>{{ remarkDialog.contact?.name }}</span>
        </el-form-item>
        <el-form-item label="备注名称">
          <el-input
            v-model="remarkDialog.form.remark"
            placeholder="请输入备注名称"
            maxlength="20"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="remarkDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveRemark">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { contactAPI } from '@/api'

const router = useRouter()

const loading = ref(false)
const syncing = ref(false)
const searchKeyword = ref('')
const activeTab = ref('all')
const sortBy = ref('name')
const filterStatus = ref('')
const selectedContacts = ref([])

const friends = ref([
  {
    id: 1,
    type: 'friend',
    name: '张三',
    remark: '同事',
    avatar: '',
    status: 'online',
    wxid: 'zhangsan123',
    addTime: '2024-01-15T10:30:00Z',
    lastContact: '2024-01-20T14:20:00Z'
  },
  {
    id: 2,
    type: 'friend',
    name: '李四',
    remark: '朋友',
    avatar: '',
    status: 'offline',
    wxid: 'lisi456',
    addTime: '2024-01-10T09:15:00Z',
    lastContact: '2024-01-18T16:45:00Z'
  },
  {
    id: 3,
    type: 'friend',
    name: '王五',
    remark: '',
    avatar: '',
    status: 'online',
    wxid: 'wangwu789',
    addTime: '2024-01-12T11:20:00Z',
    lastContact: null
  }
])

const groups = ref([
  {
    id: 4,
    type: 'group',
    name: '工作群',
    remark: '',
    avatar: '',
    status: 'online',
    memberCount: 25,
    owner: '张三',
    addTime: '2024-01-08T08:00:00Z',
    lastContact: '2024-01-20T15:30:00Z',
    members: [
      { id: 1, name: '张三', avatar: '' },
      { id: 2, name: '李四', avatar: '' },
      { id: 3, name: '王五', avatar: '' }
    ]
  },
  {
    id: 5,
    type: 'group',
    name: '朋友圈',
    remark: '',
    avatar: '',
    status: 'online',
    memberCount: 12,
    owner: '李四',
    addTime: '2024-01-05T19:30:00Z',
    lastContact: '2024-01-19T20:15:00Z',
    members: [
      { id: 2, name: '李四', avatar: '' },
      { id: 3, name: '王五', avatar: '' }
    ]
  }
])

const allContacts = computed(() => {
  return [...friends.value, ...groups.value]
})

const onlineFriends = computed(() => {
  return friends.value.filter(f => f.status === 'online').length
})

const activeGroups = computed(() => {
  return groups.value.filter(g => g.status === 'online').length
})

const filteredContacts = computed(() => {
  let contacts = []
  
  // 根据标签页筛选
  switch (activeTab.value) {
    case 'friends':
      contacts = friends.value
      break
    case 'groups':
      contacts = groups.value
      break
    default:
      contacts = allContacts.value
  }
  
  // 搜索过滤
  if (searchKeyword.value) {
    contacts = contacts.filter(contact => 
      contact.name.includes(searchKeyword.value) ||
      (contact.remark && contact.remark.includes(searchKeyword.value))
    )
  }
  
  // 状态过滤
  if (filterStatus.value) {
    contacts = contacts.filter(contact => contact.status === filterStatus.value)
  }
  
  // 排序
  contacts.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'lastContact':
        return new Date(b.lastContact || 0) - new Date(a.lastContact || 0)
      case 'addTime':
        return new Date(b.addTime) - new Date(a.addTime)
      default:
        return 0
    }
  })
  
  return contacts
})

const pagination = reactive({
  current: 1,
  size: 20,
  total: 0
})

const detailDialog = reactive({
  visible: false,
  contact: null
})

const remarkDialog = reactive({
  visible: false,
  contact: null,
  form: {
    remark: ''
  }
})

const formatTime = (timestamp) => {
  if (!timestamp) return '-'
  return new Date(timestamp).toLocaleString('zh-CN')
}

const handleSearch = () => {
  // 搜索逻辑已在computed中实现
}

const handleTabChange = () => {
  pagination.current = 1
}

const handleSort = () => {
  // 排序逻辑已在computed中实现
}

const handleFilter = () => {
  // 过滤逻辑已在computed中实现
}

const handleSelectionChange = (selection) => {
  selectedContacts.value = selection
}

const refreshContacts = async () => {
  loading.value = true
  try {
    // 模拟刷新数据
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('联系人列表刷新成功')
  } catch (error) {
    ElMessage.error('刷新失败')
  } finally {
    loading.value = false
  }
}

const syncContacts = async () => {
  syncing.value = true
  try {
    // 模拟同步联系人
    await new Promise(resolve => setTimeout(resolve, 2000))
    ElMessage.success('联系人同步成功')
  } catch (error) {
    ElMessage.error('同步失败')
  } finally {
    syncing.value = false
  }
}

const sendMessage = (contact) => {
  // 跳转到消息页面并预填联系人
  router.push({
    name: 'Message',
    query: {
      type: contact.type,
      target: contact.name
    }
  })
}

const viewDetails = (contact) => {
  detailDialog.contact = contact
  detailDialog.visible = true
}

const handleCommand = ({ action, row }) => {
  switch (action) {
    case 'edit':
      editRemark(row)
      break
    case 'block':
      blockContact(row)
      break
    case 'leave':
      leaveGroup(row)
      break
    case 'delete':
      deleteContact(row)
      break
  }
}

const editRemark = (contact) => {
  remarkDialog.contact = contact
  remarkDialog.form.remark = contact.remark || ''
  remarkDialog.visible = true
}

const saveRemark = async () => {
  try {
    // 保存备注
    remarkDialog.contact.remark = remarkDialog.form.remark
    ElMessage.success('备注保存成功')
    remarkDialog.visible = false
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const blockContact = async (contact) => {
  try {
    await ElMessageBox.confirm(`确定要拉黑 ${contact.name} 吗？`, '确认拉黑', {
      type: 'warning'
    })
    
    // 执行拉黑操作
    ElMessage.success('已拉黑该联系人')
  } catch {
    // 用户取消
  }
}

const leaveGroup = async (group) => {
  try {
    await ElMessageBox.confirm(`确定要退出群聊 ${group.name} 吗？`, '确认退群', {
      type: 'warning'
    })
    
    // 执行退群操作
    const index = groups.value.findIndex(g => g.id === group.id)
    if (index !== -1) {
      groups.value.splice(index, 1)
    }
    ElMessage.success('已退出群聊')
  } catch {
    // 用户取消
  }
}

const deleteContact = async (contact) => {
  try {
    await ElMessageBox.confirm(`确定要删除 ${contact.name} 吗？`, '确认删除', {
      type: 'warning'
    })
    
    // 执行删除操作
    if (contact.type === 'friend') {
      const index = friends.value.findIndex(f => f.id === contact.id)
      if (index !== -1) {
        friends.value.splice(index, 1)
      }
    } else {
      const index = groups.value.findIndex(g => g.id === contact.id)
      if (index !== -1) {
        groups.value.splice(index, 1)
      }
    }
    ElMessage.success('删除成功')
  } catch {
    // 用户取消
  }
}

const batchSendMessage = () => {
  if (selectedContacts.value.length === 0) {
    ElMessage.warning('请先选择联系人')
    return
  }
  
  // 跳转到消息页面进行批量发送
  router.push({
    name: 'Message',
    query: {
      batch: 'true',
      targets: selectedContacts.value.map(c => c.name).join(',')
    }
  })
}

const batchExport = () => {
  if (selectedContacts.value.length === 0) {
    ElMessage.warning('请先选择联系人')
    return
  }
  
  // 导出联系人数据
  const data = selectedContacts.value.map(contact => ({
    姓名: contact.name,
    备注: contact.remark || '',
    类型: contact.type === 'friend' ? '好友' : '群聊',
    状态: contact.status === 'online' ? '在线' : '离线',
    添加时间: formatTime(contact.addTime),
    最近联系: formatTime(contact.lastContact)
  }))
  
  // 这里可以实现实际的导出功能
  ElMessage.success(`已导出 ${data.length} 个联系人`)
}

const batchDelete = async () => {
  if (selectedContacts.value.length === 0) {
    ElMessage.warning('请先选择联系人')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedContacts.value.length} 个联系人吗？`,
      '批量删除',
      { type: 'warning' }
    )
    
    // 执行批量删除
    selectedContacts.value.forEach(contact => {
      if (contact.type === 'friend') {
        const index = friends.value.findIndex(f => f.id === contact.id)
        if (index !== -1) {
          friends.value.splice(index, 1)
        }
      } else {
        const index = groups.value.findIndex(g => g.id === contact.id)
        if (index !== -1) {
          groups.value.splice(index, 1)
        }
      }
    })
    
    selectedContacts.value = []
    ElMessage.success('批量删除成功')
  } catch {
    // 用户取消
  }
}

const handleSizeChange = (size) => {
  pagination.size = size
  pagination.current = 1
}

const handleCurrentChange = (current) => {
  pagination.current = current
}

onMounted(() => {
  pagination.total = allContacts.value.length
})
</script>

<style scoped>
.contact-page {
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  border: none;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.friend-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.group-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.online-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.active-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stat-label {
  color: #7f8c8d;
  font-size: 14px;
}

.contacts-card {
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

.filters-section {
  margin-bottom: 16px;
}

.search-bar {
  margin-bottom: 16px;
}

.filter-tabs {
  margin-bottom: 16px;
}

.filter-options {
  display: flex;
  gap: 12px;
}

.contact-name-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-name {
  font-weight: 500;
}

.no-remark,
.no-contact {
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

.pagination-wrapper {
  margin-top: 16px;
  text-align: right;
}

.contact-detail {
  padding: 16px 0;
}

.detail-header {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.detail-info h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.detail-info .remark {
  color: #7f8c8d;
  margin: 8px 0;
}

.group-members {
  margin-top: 24px;
}

.group-members h4 {
  margin: 0 0 16px 0;
  color: #2c3e50;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border: 1px solid #ebeef5;
  border-radius: 6px;
}

.member-name {
  font-size: 12px;
  color: #606266;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .filter-options {
    flex-direction: column;
  }
  
  .batch-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .pagination-wrapper {
    text-align: center;
  }
  
  .members-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>