<template>
    <div class="statistics-container">
        <div class="stats-section">
            <div 
                class="stat-card" 
                v-for="stat in statsList" 
                :key="stat.id"
            >
                <div 
                    class="stat-icon" 
                    :style="{ background: stat.iconBg, color: stat.iconColor }"
                    v-html="stat.iconSvg"
                ></div>
                <div class="stat-info">
                    <!-- 动态绑定值 -->
                    <div class="stat-value">
                        {{ stat.value }}
                    </div>
                    <div class="stat-label">
                        {{ stat.label }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 定义卡片子元素接口
interface StatsItem {
    id: number;   // 编号
    value: number;   // 值
    label: string;   // 类别
    iconSvg: string;   // SVG内容
    iconColor: string;   // 图标颜色
    iconBg: string;   // 图标背景
}

// 定义卡片列表
const statsList = ref<StatsItem[]>([
    {
        id: 1,
        value: 0,
        label: '计划数量',
        iconSvg: `<svg  xmlns="http://www.w3.org/2000/svg" width="24" height="24"  
                fill="currentColor" viewBox="0 0 24 24" >
                <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                <path d="M20 3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2M4 19V5h16v14z"></path><path d="M13 8h5v2h-5zm-5 .59L6.96 7.54 5.54 8.96 8 11.41l3.46-3.45-1.42-1.42zM13 14h5v2h-5zm-5 .59-1.04-1.05-1.42 1.42L8 17.41l3.46-3.45-1.42-1.42z"></path>
                </svg>`,
        iconColor: '#7494ec',
        iconBg: 'linear-gradient(135deg, #e8f0ff, #d4e4ff)'
    },
    {
        id: 2,
        value: 0,
        label: '药品数量',
        iconSvg: `<svg  xmlns="http://www.w3.org/2000/svg" width="24" height="24"  
                fill="currentColor" viewBox="0 0 24 24" >
                <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                <path d="M18 6h-1V4c0-1.1-.9-2-2-2H9c-1.1 0-2 .9-2 2v2H6c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2M9 4h6v2H9zM6 20V8h12v12z"></path><path d="M13 10h-2v3H8v2h3v3h2v-3h3v-2h-3z"></path>
                </svg>`,
        iconColor: '#ff6b6b',
        iconBg: 'linear-gradient(135deg, #ffe8f0, #ffd4e4)'
    },
    {
        id: 3,
        value: 0,
        label: '好友数量',
        iconSvg: `<svg  xmlns="http://www.w3.org/2000/svg" width="24" height="24"  
                fill="currentColor" viewBox="0 0 24 24" >
                <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                <path d="M12 11c1.71 0 3-1.29 3-3s-1.29-3-3-3-3 1.29-3 3 1.29 3 3 3m0-4c.6 0 1 .4 1 1s-.4 1-1 1-1-.4-1-1 .4-1 1-1m1 5h-2c-2.76 0-5 2.24-5 5v.5c0 .83.67 1.5 1.5 1.5h9c.83 0 1.5-.67 1.5-1.5V17c0-2.76-2.24-5-5-5m-5 5c0-1.65 1.35-3 3-3h2c1.65 0 3 1.35 3 3zm-1.5-6c.47 0 .9-.12 1.27-.33a5.03 5.03 0 0 1-.42-4.52C7.09 6.06 6.8 6 6.5 6 5.06 6 4 7.06 4 8.5S5.06 11 6.5 11m-.39 1H5.5C3.57 12 2 13.57 2 15.5v1c0 .28.22.5.5.5H4c0-1.96.81-3.73 2.11-5m11.39-1c1.44 0 2.5-1.06 2.5-2.5S18.94 6 17.5 6c-.31 0-.59.06-.85.15a5.03 5.03 0 0 1-.42 4.52c.37.21.79.33 1.27.33m1 1h-.61A6.97 6.97 0 0 1 20 17h1.5c.28 0 .5-.22.5-.5v-1c0-1.93-1.57-3.5-3.5-3.5"></path>
                </svg>`,
        iconColor: '#51cf66',
        iconBg: 'linear-gradient(135deg, #f0ffe8, #e4ffd4)'
    }
])
</script>

<style scoped>
    .statistics-container {
        height: 100%;
        width: 100%;
    }

    .stats-section {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }

    .stat-card {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 20px;
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(116, 148, 236, 0.15);
    }

    .stat-icon {
        width: 50px;
        height: 50px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .stat-info {
        display: flex;
        flex-direction: column;
    }

    .stat-value {
        font-size: 24px;
        font-weight: 700;
        color: #333;
    }

    .stat-label {
        font-size: 13px;
        color: #999;
    }
</style>