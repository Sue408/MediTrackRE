<template>
  <div class="home-layout">
    <!-- 顶部栏 -->
    <header class="topbar">
      <div class="topbar-left">
        <div class="logo">
          <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L4 6V12C4 16.42 7.58 20.74 12 22C16.42 20.74 20 16.42 20 12V6L12 2Z" fill="currentColor"/>
            <path d="M12 6L16 8V12C16 14.21 14.21 16 12 16C9.79 16 8 14.21 8 12V8L12 6Z" fill="white" fill-opacity="0.5"/>
          </svg>
        </div>
        <span class="app-name">Meditrack</span>
      </div>
      <div class="topbar-right">
        <div class="user-info">
          <span class="user-nickname">{{ nickname || '用户' }}</span>
          <div class="user-avatar">
            <img v-if="imageUrl" :src="imageUrl" alt="用户头像" />
            <div v-else class="avatar-placeholder">
              {{ nickname ? nickname.charAt(0).toUpperCase() : 'U' }}
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="main-container">
      <!-- 侧边栏 -->
      <aside class="sidebar">
        <nav class="sidebar-nav">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: currentRoute === item.path }"
          >
            <span class="nav-icon" v-html="item.icon"></span>
            <span class="nav-label">{{ item.label }}</span>
          </router-link>
        </nav>
      </aside>

      <!-- 功能视图 -->
      <main class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const route = useRoute()
const authStore = useAuthStore()

const nickname = computed(() => authStore.nickname)
const imageUrl = computed(() => authStore.imageUrl)

const currentRoute = computed(() => route.path)

const menuItems = [
  {
    path: '/',
    label: '今日用药',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>'
  },
  {
    path: '/medicine',
    label: '药品管理',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.5 20.5L3.5 13.5C2.1 12.1 2.1 9.9 3.5 8.5L8.5 3.5C9.9 2.1 12.1 2.1 13.5 3.5L20.5 10.5C21.9 11.9 21.9 14.1 20.5 15.5L15.5 20.5C14.1 21.9 11.9 21.9 10.5 20.5Z"/><path d="M8 8L16 16"/></svg>'
  },
  {
    path: '/plan',
    label: '计划管理',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
  },
  {
    path: '/relationship',
    label: '关系管理',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
  },
  {
    path: '/userCenter',
    label: '个人中心',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
  }
]
</script>

<style scoped>
.home-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f7fa;
}

/* 顶部栏样式 */
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  padding: 0 24px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  z-index: 100;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 36px;
  height: 36px;
  color: #7494ec;
}

.logo-icon {
  width: 100%;
  height: 100%;
}

.app-name {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.topbar-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.user-nickname {
  font-size: 14px;
  color: #666;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #7494ec;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
}

/* 主容器样式 */
.main-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 侧边栏样式 */
.sidebar {
  width: 220px;
  background-color: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.04);
  padding: 20px 0;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  color: #666;
  text-decoration: none;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background-color: #f0f4ff;
  color: #7494ec;
}

.nav-item.active {
  background-color: #7494ec;
  color: #fff;
}

.nav-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon :deep(svg) {
  width: 100%;
  height: 100%;
}

.nav-label {
  font-size: 14px;
  font-weight: 500;
}

/* 功能视图样式 */
.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* 路由切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .sidebar {
    width: 60px;
  }

  .nav-label {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: 12px;
  }

  .user-nickname {
    display: none;
  }
}
</style>