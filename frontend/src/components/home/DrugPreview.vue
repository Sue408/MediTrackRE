<template>
    <div class="drug-preview-container">
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
                        <path d="M18 6h-1V4c0-1.1-.9-2-2-2H9c-1.1 0-2 .9-2 2v2H6c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2M9 4h6v2H9zM6 20V8h12v12z"></path><path d="M13 10h-2v3H8v2h3v3h2v-3h3v-2h-3z"></path>
                    </svg>
                </div>
            </div>
            <div class="title-section">
                <h3>药品管理</h3>
                <p class="subtitle">管理我的药品库</p>
            </div>
        </div>

        <!-- 右侧：统计和快捷操作 -->
        <div class="right-section">
            <!-- 统计信息 -->
            <div class="stats-section">
                <div class="stat-item">
                    <span class="stat-value">{{ drugStore.drugCount }}</span>
                    <span class="stat-label">药品</span>
                </div>
                <div class="stat-divider"></div>
                <div class="stat-item">
                    <span class="stat-value">{{ drugStore.usageMethodCount }}</span>
                    <span class="stat-label">用法</span>
                </div>
            </div>
            <!-- 快捷操作 -->
            <div class="quick-actions">
                <span class="method-tag" v-for="method in drugStore.topMethods" :key="method">{{ method }}</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { onMounted } from 'vue'
    import { useDrugStore } from '@/stores/drugStore'

    // 使用药品 store
    const drugStore = useDrugStore()

    // 挂载时获取药品数据
    onMounted(() => {
        if (drugStore.drugList.length === 0) {
            drugStore.fetchDrugs()
        }
    })
</script>

<style scoped>
    .drug-preview-container {
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

    .method-tag {
        padding: 3px 8px;
        background: rgba(255, 255, 255, 0.9);
        color: #5f7fd9;
        border-radius: 8px;
        font-size: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
</style>