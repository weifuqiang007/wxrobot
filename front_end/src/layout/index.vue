<template>
  <div class="layout-container">
    <el-container class="layout-wrapper">
      <!-- 侧边栏 -->
      <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
        <div class="logo-container">
          <div class="logo">
            <el-icon size="24" color="#409EFF">
              <ChatDotRound />
            </el-icon>
            <span v-show="!isCollapse" class="logo-text">微信后端</span>
          </div>
        </div>
        
        <el-menu
          :default-active="$route.path"
          :collapse="isCollapse"
          :unique-opened="true"
          router
          class="sidebar-menu"
        >
          <el-menu-item
            v-for="route in menuRoutes"
            :key="route.path"
            :index="route.path"
          >
            <el-icon>
              <component :is="route.meta.icon" />
            </el-icon>
            <template #title>{{ route.meta.title }}</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container class="main-container">
        <!-- 顶部栏 -->
        <el-header class="header">
          <div class="header-left">
            <el-button
              type="text"
              size="large"
              @click="toggleCollapse"
            >
              <el-icon size="18">
                <Expand v-if="isCollapse" />
                <Fold v-else />
              </el-icon>
            </el-button>
            
            <el-breadcrumb separator="/" class="breadcrumb">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item v-if="currentRoute.meta.title">
                {{ currentRoute.meta.title }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <div class="user-info">
                <el-avatar size="small" icon="UserFilled" />
                <span class="username">{{ authStore.user?.name || '管理员' }}</span>
                <el-icon class="dropdown-icon">
                  <ArrowDown />
                </el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <!-- 内容区 -->
        <el-main class="main-content">
          <router-view v-slot="{ Component }">
            <transition name="fade-transform" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isCollapse = ref(false)

const currentRoute = computed(() => route)

const menuRoutes = computed(() => {
  return router.getRoutes()
    .find(r => r.name === 'Layout')
    ?.children?.filter(child => child.meta?.title) || []
})

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm(
        '确定要退出登录吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
      
      authStore.logout()
      ElMessage.success('已退出登录')
      router.push('/login')
    } catch {
      // 用户取消
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  overflow: hidden;
}

.layout-wrapper {
  height: 100%;
}

.sidebar {
  background: #001529;
  transition: width 0.3s;
  overflow: hidden;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #1f2937;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  white-space: nowrap;
}

.sidebar-menu {
  border: none;
  background: #001529;
}

.sidebar-menu :deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.8);
  border-radius: 0;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: #1890ff;
  color: #fff;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: #1890ff;
  color: #fff;
}

.main-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.header {
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.breadcrumb {
  font-size: 14px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.user-info:hover {
  background: #f5f5f5;
}

.username {
  font-size: 14px;
  color: #333;
}

.dropdown-icon {
  font-size: 12px;
  color: #999;
}

.main-content {
  flex: 1;
  background: #f5f5f5;
  padding: 20px;
  overflow-y: auto;
}

/* 页面切换动画 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>