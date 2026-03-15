<template>
  <div class="user-preview-container">

    <!-- 飘落的装饰元素 -->
    <div class="floating-elements">
      <span class="float-dot dot-1"></span>
      <span class="float-dot dot-2"></span>
      <span class="float-star star-1">★</span>
      <span class="float-star star-2">✦</span>
    </div>

    <!-- 主背景形状 -->
    <div class="background-shape"></div>

    <!-- 主体内容卡片 -->
    <div class="main-card">
      <!-- 头像区域 -->
      <div class="avatar-section">
        <div class="avatar-ring">
          <div class="avatar-wrapper">
            <img v-if="imageUrl" :src="imageUrl" alt="用户头像" class="avatar-img" />
            <div v-else class="avatar-placeholder">
              {{ nickname ? nickname.charAt(0).toUpperCase() : 'U' }}
            </div>
          </div>
        </div>
      </div>

      <!-- 用户信息区域 -->
      <div class="info-section">
        <div class="nickname">{{ nickname || '未设置昵称' }}</div>
        <div class="email">{{ email || '未绑定邮箱' }}</div>
      </div>

      <!-- 装饰线 -->
      <div class="divider">
        <span class="divider-dot"></span>
        <span class="divider-line"></span>
        <span class="divider-dot"></span>
      </div>

      <!-- 快捷操作按钮 -->
      <div class="quick-actions">
        <div class="action-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>个人</span>
        </div>
        <div class="action-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M9 12H15M9 16H15M17 21H7C5.89543 21 5 20.1046 5 19V5C5 3.89543 5.89543 3 7 3H12.5858C12.851 3 13.1054 3.10536 13.2929 3.29289L18.7071 8.70711C18.8946 8.89464 19 9.149 19 9.41421V19C19 20.1046 18.1046 21 17 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M13 3V8C13 8.55228 13.4477 9 14 9H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>档案</span>
        </div>
        <div class="action-item">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
            <path d="M7 11V7C7 5.67392 7.52678 4.40215 8.46447 3.46447C9.40215 2.52678 10.6739 2 12 2C13.3261 2 14.5979 2.52678 15.5355 3.46447C16.4732 4.40215 17 5.67392 17 7V11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span>安全</span>
        </div>
      </div>

      <!-- 底部提示 -->
      <div class="footer-hint">
        <span>进入中心</span>
        <svg class="arrow-icon" width="14" height="14" viewBox="0 0 24 24" fill="none">
          <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed } from 'vue'
  import { useUserStore } from '@/stores/userStore'

  const userStore = useUserStore()

  const nickname = computed(() => userStore.nickname)
  const email = computed(() => userStore.email)
  const imageUrl = computed(() => userStore.imageUrl)
</script>

<style scoped>
  .user-preview-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    background: #ffffff;
    border-radius: 30px;
    box-shadow: 0 0 30px rgba(116, 148, 236, 0.2);
    overflow: hidden;
  }

  /* 主背景形状 */
  .background-shape {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 45%;
    background: linear-gradient(135deg, #7494ec 0%, #8aa7f0 50%, #9bb3f0 100%);
    /* 使用clip-path创建斜切效果 */
    clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
    z-index: 1;
  }

  /* 飘落装饰元素 */
  .floating-elements {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    pointer-events: none;
    overflow: hidden;
    z-index: 2;
  }

  .float-dot {
    position: absolute;
    border-radius: 50%;
    animation: float-rotate 8s ease-in-out infinite;
  }

  .dot-1 {
    width: 8px;
    height: 8px;
    background: rgba(255, 255, 255, 0.8);
    top: 10%;
    left: 15%;
    animation-delay: 0s;
  }

  .dot-2 {
    width: 6px;
    height: 6px;
    background: rgba(255, 255, 255, 0.7);
    top: 20%;
    right: 20%;
    animation-delay: 1s;
  }

  .float-star {
    position: absolute;
    font-size: 14px;
    animation: float-rotate 6s ease-in-out infinite;
  }

  .star-1 {
    color: rgba(255, 255, 255, 0.9);
    top: 35%;
    left: 10%;
    animation-delay: 0.5s;
  }

  .star-2 {
    color: rgba(255, 255, 255, 0.8);
    top: 50%;
    right: 12%;
    animation-delay: 1.5s;
  }

  @keyframes float-rotate {
    0%, 100% {
      transform: translateY(0) rotate(0deg);
      opacity: 0.7;
    }
    50% {
      transform: translateY(-10px) rotate(180deg);
      opacity: 1;
    }
  }

  /* 主卡片 */
  .main-card {
    flex: 1;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 15px 10px;
    position: relative;
    z-index: 3;
  }

  /* 头像区域 */
  .avatar-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    margin-bottom: 12px;
  }

  .avatar-ring {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7494ec 0%, #9bb3f0 100%);
    padding: 4px;
    box-shadow: 0 4px 15px rgba(116, 148, 236, 0.4);
    animation: pulse-glow 3s ease-in-out infinite;
  }

  @keyframes pulse-glow {
    0%, 100% {
      box-shadow: 0 4px 15px rgba(116, 148, 236, 0.4);
    }
    50% {
      box-shadow: 0 4px 25px rgba(116, 148, 236, 0.7);
    }
  }

  .avatar-wrapper {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    overflow: hidden;
    border: 2px solid #fff;
    transition: transform 0.3s ease;
  }

  .avatar-wrapper:hover {
    transform: scale(1.05);
  }

  .avatar-img {
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
    background: linear-gradient(135deg, #7494ec 0%, #9bb3f0 100%);
    color: #fff;
    font-size: 28px;
    font-weight: 600;
  }

  /* 用户信息区域 */
  .info-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    
  }

  .nickname {
    font-size: 16px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 4px;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .email {
    font-size: 11px;
    color: #fff;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* 装饰线 */
  .divider {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 18px 0;
    width: 70%;
  }

  .divider-dot {
    width: 4px;
    height: 4px;
    background: #fff;
    border-radius: 50%;
  }

  .divider-line {
    flex: 1;
    height: 1px;
    background: #fff;
  }

  /* 快捷操作按钮 */
  .quick-actions {
    display: flex;
    gap: 10px;
    margin: 48px 0;
  }

  .action-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    color: rgba(116, 148, 236, 0.9);
    cursor: pointer;
    padding: 6px 10px;
    border-radius: 8px;
    transition: all 0.3s ease;
  }

  .action-item:hover {
    background: rgba(116, 148, 236, 0.2);
    border-color: rgba(116, 148, 236, 0.4);
    transform: translateY(-2px);
  }

  .action-item svg {
    transition: transform 0.3s ease;
  }

  .action-item:hover svg {
    transform: scale(1.1);
  }

  .action-item span {
    font-size: 10px;
  }

  /* 底部提示 */
  .footer-hint {
    display: flex;
    align-items: center;
    gap: 4px;
    color: rgba(116, 148, 236, 0.9);
    font-size: 11px;
    font-weight: 600;
    margin-top: auto;
    padding-bottom: 8px;
    animation: hint-pulse 2s ease-in-out infinite;
  }

  @keyframes hint-pulse {
    0%, 100% {
      opacity: 0.8;
    }
    50% {
      opacity: 1;
    }
  }

  .footer-hint .arrow-icon {
    animation: arrow-move 1.5s ease-in-out infinite;
  }

  @keyframes arrow-move {
    0%, 100% {
      transform: translateX(0);
    }
    50% {
      transform: translateX(4px);
    }
  }
</style>