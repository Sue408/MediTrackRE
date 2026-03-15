import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

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
      {
        path: 'today-medicine',
        name: 'TodayMedicine',
        component: () => import('@/pages/home/TodayDrugTasks.vue'),
      },
      {
        path: 'user-center',
        name: 'UserCenter',
        component: () => import('@/pages/home/UserCenter.vue'),
        children: [
          {
            path: '',
            name: 'UserCenterRoot',
            redirect: { name: 'UserInfo' }
          },
          {
            path: 'user-info',
            name: 'UserInfo',
            component: () => import('@/pages/user-center/UserInfo.vue')
          },
          {
            path: 'health-records',
            name: 'HealthRecords',
            component: () => import('@/pages/user-center/HealthRecord.vue')
          },
          {
            path: 'security-center',
            name: 'SecurityCenter',
            component: () => import('@/pages/user-center/SecurityCenter.vue')
          }
        ]
      },
      {
        path: 'medicine-management',
        name: 'MedicineManagement',
        component: () => import('@/pages/home/DrugManagement.vue')
      },
      {
        path: 'plan-management',
        name: 'PlanManagement',
        component: () => import('@/pages/home/PlanManagement.vue')
      },
      {
        path: 'relationship-management',
        name: 'RelationshipManagement',
        component: () => import('@/pages/home/FriendManagement.vue')
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
router.beforeEach(async (to) => {
  const authStore = useUserStore()

  // 判断目标路由是否需要登录
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    // 尝试刷新token
    const refreshSuccess = await authStore.refresh()

    if (!refreshSuccess) {
      // 刷新失败，登出并跳转到登录页
      authStore.logout()
      return {path: '/auth', replace: true}
    }
  } else if (to.path === '/auth' && authStore.isLoggedIn) {
    // 已登录访问登录页则跳转到主页
    return {path: '/', replace: true}
  }

  return true
})

// 导出路由对象
export default router
