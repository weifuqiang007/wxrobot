import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layout/index.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表盘', icon: 'Monitor' }
      },
      {
        path: '/status',
        name: 'Status',
        component: () => import('@/views/Status.vue'),
        meta: { title: '系统状态', icon: 'CircleCheck' }
      },
      {
        path: '/message',
        name: 'Message',
        component: () => import('@/views/Message.vue'),
        meta: { title: '消息管理', icon: 'ChatDotRound' }
      },
      {
        path: '/contacts',
        name: 'Contacts',
        component: () => import('@/views/Contact.vue'),
        meta: { title: '联系人管理' }
      },
      {
        path: '/welcome',
        name: 'Welcome',
        component: () => import('@/views/Welcome.vue'),
        meta: { title: '新成员欢迎', icon: 'UserFilled' }
      },
      {
        path: '/news',
        name: 'News',
        component: () => import('@/views/News.vue'),
        meta: { title: '新闻推送', icon: 'Notification' }
      },
      {
        path: '/config',
        name: 'Config',
        component: () => import('@/views/Config.vue'),
        meta: { title: '系统配置', icon: 'Setting' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router