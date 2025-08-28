import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '请求失败'
    ElMessage.error(message)
    
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      window.location.href = '/login'
    }
    
    return Promise.reject(error)
  }
)

// API接口定义
export const statusAPI = {
  // 获取系统状态
  getStatus: () => api.get('/status'),
}

export const configAPI = {
  // 获取配置
  getConfig: () => api.get('/config'),
  // 更新配置
  updateConfig: (data) => api.put('/config', data),
}

export const messageAPI = {
  // 发送消息
  sendMessage: (data) => api.post('/message/send', data),
  // 获取消息历史
  getMessageHistory: (params) => api.get('/message/history', { params }),
  // 启动消息监控
  startMonitoring: (data) => api.post('/start-monitoring', data),
  // 停止消息监控
  stopMonitoring: () => api.post('/stop-monitoring'),
  // 获取监控状态
  getMonitoringStatus: () => api.get('/monitoring-status'),
  // 设置自动回复
  setAutoReply: (data) => api.post('/set-auto-reply', data)
}

export const contactAPI = {
  // 获取联系人列表
  getContacts: () => api.get('/contacts'),
  // 获取群聊列表
  getGroups: () => api.get('/contacts/groups'),
}

export const newsAPI = {
  // 获取新闻推送配置
  getNewsConfig: () => api.get('/news/config'),
  // 更新新闻推送配置
  updateNewsConfig: (data) => api.put('/news/config', data),
  // 测试新闻推送
  testNews: () => api.post('/news/test'),
}

export default api