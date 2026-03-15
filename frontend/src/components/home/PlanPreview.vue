<template>
    <div class="plan-preview-container">
        <!-- 左侧圆弧背景 -->
        <div class="left-bg-arc"></div>
        
        <!-- 左侧：图标和标题 -->
        <div class="left-section">
            <!-- 图标区域 -->
            <div class="icon-section">
                <div class="icon-ring">
                    <svg  xmlns="http://www.w3.org/2000/svg" width="32" height="32"  
                    fill="currentColor" viewBox="0 0 24 24" >
                    <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                    <path d="M20 3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2M4 19V5h16v14z"></path><path d="M13 8h5v2h-5zm-5 .59L6.96 7.54 5.54 8.96 8 11.41l3.46-3.45-1.42-1.42zM13 14h5v2h-5zm-5 .59-1.04-1.05-1.42 1.42L8 17.41l3.46-3.45-1.42-1.42z"></path>
                    </svg>
                </div>
            </div>
            <div class="title-section">
                <h3>计划管理</h3>
                <p class="subtitle">规划用药提醒</p>
            </div>
        </div>

        <!-- 右侧：统计和快捷操作 -->
        <div class="right-section">
            <!-- 统计信息 -->
            <div class="stats-section">
                <div class="stat-item">
                    <span class="stat-value">{{ planStore.activeCount }}</span>
                    <span class="stat-label">进行中</span>
                </div>
                <div class="stat-divider"></div>
                <div class="stat-item">
                    <span class="stat-value">{{ planStore.planCount }}</span>
                    <span class="stat-label">总计划</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { onMounted } from 'vue'
    import { usePlanStore } from '@/stores/planStore'

    // 使用计划 store
    const planStore = usePlanStore()

    // 挂载时获取计划数据
    onMounted(() => {
        planStore.fetchPlans()
    })
</script>

<style scoped>
    .plan-preview-container {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        gap: 90px;
        padding: 12px 15px;
        position: relative;
        border-radius: 30px;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    /* 左侧圆弧背景 */
    .left-bg-arc {
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 55%;
        background: linear-gradient(135deg, 
            #8fa8ff 0%,      /* 稍浅的蓝紫色 */
            #7494ec 50%,     /* 核心主题色 */
            #5f7fd9 100%     /* 稍深的蓝紫色 */
        );
        border-top-left-radius: 30px;
        border-bottom-left-radius: 30px;
        /* 创建右侧圆弧边界 */
        border-top-right-radius: 100px 150%;
        border-bottom-right-radius: 100px 150%;
        z-index: 1;
    }

    /* 左侧区域 */
    .left-section {
        display: flex;
        align-items: center;
        gap: 12px;
        position: relative;
        z-index: 2;
    }

    /* 图标区域 */
    .icon-section {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .icon-ring {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(116, 148, 236, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .icon-ring svg {
        color: #fff;
    }

    /* 标题区域 */
    .title-section {
        display: flex;
        flex-direction: column;
    }

    .title-section h3 {
        font-size: 16px;
        font-weight: 700;
        color: #fff;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .subtitle {
        font-size: 11px;
        color: rgba(255, 255, 255, 0.9);
        margin: 2px 0 0 0;
    }

    /* 右侧区域 */
    .right-section {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 6px;
        position: relative;
        z-index: 2;
    }

    /* 统计信息 */
    .stats-section {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 6px 12px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .stat-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .stat-value {
        font-size: 16px;
        font-weight: 700;
        color: #5f7fd9;
    }

    .stat-label {
        font-size: 9px;
        color: #8fa8ff;
    }

    .stat-divider {
        width: 1px;
        height: 20px;
        background: #b8c8ff;
    }

    /* 快捷操作 */
    .quick-actions {
        display: flex;
        gap: 5px;
    }

    .plan-tag {
        padding: 3px 8px;
        background: rgba(255, 255, 255, 0.9);
        color: #5f7fd9;
        border-radius: 8px;
        font-size: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
</style>