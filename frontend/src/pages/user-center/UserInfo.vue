<template>
    <div class="user-info-container">
        <!-- 标题区域 -->
        <div class="header-section">
            <h3>个人信息</h3>
            <p>显示您的个人信息</p>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <span>加载中...</span>
        </div>

        <!-- 内容区域 -->
        <div v-else class="content-section">
            <!-- 用户信息卡片 -->
            <div class="card">
            <UserCard />
            </div>

            <!-- 统计信息卡片 -->
            <div>
                <Statistics />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue'
    import UserCard from '@/components/user-center/UserCard.vue';
    import Statistics from '@/components/user-center/Statistics.vue'

    const loading = ref<boolean>(false)
</script>

<style scoped>
    .user-info-container {
        height: 100%;
        width: 100%;
        overflow-y: auto;
        padding: 20px;
    }

    .user-info-container::-webkit-scrollbar {
        width: 0;
    }

    .header-section {
        margin-bottom: 25px;
    }

    .header-section h3 {
        margin: 0 0 8px 0;
        color: #333;
        font-size: 20px;
    }

    .header-section p {
        margin: 0;
        color: #999;
        font-size: 14px;
    }

    .loading-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px;
        color: #999;
    }

    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top-color: #7494ec;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 15px;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .content-section {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .card {
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        overflow: hidden;
        padding: 15px;
    }
</style>