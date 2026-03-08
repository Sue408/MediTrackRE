import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

// 定义页面路由
const routes: Array<RouteRecordRaw> = [
  // 主页
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
    meta: {
      requiresAuth: true
    },
    children: [
      // 今日用药（默认首页）
      {
        path: '',
        name: 'TodayMedicine',
        component: () => import('@/pages/Home/TodayMedicine.vue'),
        meta: {
          requiresAuth: true
        }
      },
      // 药品管理
      {
        path: 'medicine',
        name: 'MedicineManagement',
        component: () => import('@/pages/Home/MedicineManagement.vue'),
        meta: {
          requiresAuth: true
        }
      },
      // 计划管理
      {
        path: 'plan',
        name: 'PlanManagement',
        component: () => import('@/pages/Home/PlanManagement.vue'),
        meta: {
          requiresAuth: true
        }
      },
      // 关系管理
      {
        path: 'relationship',
        name: 'RelationshipManagement',
        component: () => import('@/pages/Home/RelationshipManagement.vue'),
        meta: {
          requiresAuth: true
        }
      },
      // 个人中心
      {
        path: 'userCenter',
        name: 'UserCenter',
        component: () => import('@/pages/Home/userCenter.vue'),
        meta: {
          requiresAuth: true
        }
      }
    ]
  },
  // 登录页
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('@/pages/Auth.vue')
  }
]

// 创建路由对象
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 设置路由守卫
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()

  // 判断目标路由是否需要登录
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    // 未登录则跳转到登录页
    next('/auth')
  } else if (to.path === '/auth' && authStore.isLoggedIn) {
    // 已登录访问登录页则跳转到主页
    next('/')
  } else {
    next()
  }
})

// 导出路由对象
export default router
