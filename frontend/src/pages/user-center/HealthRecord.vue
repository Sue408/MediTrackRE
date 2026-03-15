<template>
    <div class="health-record-container">
        <!-- 标题区域 -->
        <div class="header-section">
            <h3>健康档案</h3>
            <p>管理您的健康信息，帮助我们更好地为您服务</p>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <span>加载中...</span>
        </div>

        <!-- 内容区域 -->
        <div v-else class="content-section">
            <!-- 基本健康档案 -->
            <transition name="fade-slide" mode="out-in">
                <BaseInfo :profile="profile" @refresh="loadProfile" :key="'base'" />
            </transition>

            <!-- 过敏史 -->
            <transition name="fade-slide" mode="out-in">
                <Allergies :profile="profile" @refresh="loadProfile" :key="'allergies'" />
            </transition>

            <!-- 疾病史 -->
            <transition name="fade-slide" mode="out-in">
                <Diseases :profile="profile" @refresh="loadProfile" :key="'diseases'" />
            </transition>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, onMounted } from 'vue'
    import { getProfile } from '@/api/user'
    import type { ProfileResponse } from '@/types/userTypes'
    import BaseInfo from '@/components/user-center/BaseInfo.vue'
    import Allergies from '@/components/user-center/Allergies.vue'
    import Diseases from '@/components/user-center/Diseases.vue'

    // 加载状态
    const loading = ref(true)

    // 档案数据
    const profile = reactive<ProfileResponse>({
        id: 0,
        user_id: 0,
        gender: 'unknown',
        height: null,
        weight: null,
        blood_type: 'unknown',
        allergies: [],
        diseases: [],
        special_status: null,
        created_at: '',
        updated_at: ''
    })

    // 加载档案
    const loadProfile = async () => {
        loading.value = true
        try {
            const data = await getProfile()
            Object.assign(profile, data)
        } catch (error) {
            console.error('加载健康档案失败:', error)
        } finally {
            loading.value = false
        }
    }

    onMounted(() => {
        loadProfile()
    })
</script>

<style scoped>
    .health-record-container {
        height: 100%;
        width: 100%;
        overflow-y: auto;
        padding: 20px;
    }

    /* 隐藏滚动条 */
    .health-record-container::-webkit-scrollbar {
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

    /* 动画 */
    .fade-slide-enter-active,
    .fade-slide-leave-active {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .fade-slide-enter-from {
        opacity: 0;
        transform: translateY(20px);
    }

    .fade-slide-leave-to {
        opacity: 0;
        transform: translateY(-20px);
    }
</style>
