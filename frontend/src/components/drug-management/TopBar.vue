<template>
    <div class="top-bar-container">
        <!-- 返回按钮 -->
        <button class="back-btn" @click="backHome">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M15.41 7.41L14 6L8 12L14 18L15.41 16.59L10.83 12L15.41 7.41Z" fill="currentColor"/>
            </svg>
        </button>

        <!-- 标题 -->
        <div class="page-title">
            <h3>药品管理</h3>
            <span class="drug-count">共 {{ total }} 种药品</span>
        </div>

        <!-- 添加药品按钮 -->
         <button class="add-btn" @click="$emit('addDrug')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
            </svg>
            <span>添加药品</span>
        </button>
    </div>
</template>

<script setup lang="ts">
    import { useRouter } from 'vue-router'

    const router = useRouter()

    const props = defineProps<{
        total: number
    }>()

    // 返回主页面
    const backHome = () => {
        router.replace('/')
    }

    
</script>

<style scoped>
    .top-bar-container {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 24px;
    }

    .back-btn {
        width: 42px;
        height: 42px;
        border: none;
        background: linear-gradient(135deg, #7494ec 0%, #5a7de0 100%);
        color: #fff;
        border-radius: 14px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(116, 148, 236, 0.3);
    }

    .back-btn:hover {
        transform: scale(1.1) rotate(-10deg);
        box-shadow: 0 6px 20px rgba(116, 148, 236, 0.4);
    }

    .page-title {
        flex: 1;
    }

    .page-title h3 {
        margin: 0;
        font-size: 20px;
        font-weight: 600;
        color: #333;
    }

    .drug-count {
        font-size: 13px;
        color: #999;
    }

    .add-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 22px;
        border: none;
        border-radius: 20px;
        background: linear-gradient(135deg, #7494ec 0%, #5a7de0 100%);
        color: #fff;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(116, 148, 236, 0.3);
    }

    .add-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(116, 148, 236, 0.4);
    }

    .add-btn:active {
        transform: translateY(-1px);
    }
</style>