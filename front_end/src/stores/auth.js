import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')

  // 初始化认证状态
  const initAuth = () => {
    const savedToken = localStorage.getItem('token')
    if (savedToken) {
      token.value = savedToken
      isAuthenticated.value = true
      // 这里可以验证token有效性
    }
  }

  // 登录
  const login = async (credentials) => {
    try {
      // 简单的模拟登录，实际项目中应该调用真实的登录API
      if (credentials.username === 'admin' && credentials.password === 'admin123') {
        const mockToken = 'mock-jwt-token-' + Date.now()
        token.value = mockToken
        isAuthenticated.value = true
        user.value = {
          id: 1,
          username: credentials.username,
          name: '管理员'
        }
        localStorage.setItem('token', mockToken)
        return { success: true }
      } else {
        throw new Error('用户名或密码错误')
      }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  // 登出
  const logout = () => {
    token.value = ''
    isAuthenticated.value = false
    user.value = null
    localStorage.removeItem('token')
  }

  // 检查认证状态
  const checkAuth = async () => {
    try {
      if (!token.value) {
        return false
      }
      // 这里可以调用API验证token
      return true
    } catch (error) {
      logout()
      return false
    }
  }

  return {
    isAuthenticated,
    user,
    token,
    initAuth,
    login,
    logout,
    checkAuth
  }
})