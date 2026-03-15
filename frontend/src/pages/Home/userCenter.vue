<template>
    <div class="user-center-container">
        <div class="control-wrapper">
            <div class="top-panel">
                <button class="back-btn" @click="backHome">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M15.41 7.41L14 6L8 12L14 18L15.41 16.59L10.83 12L15.41 7.41Z" fill="currentColor"/>
                    </svg>
                </button>
                <h3>用户中心</h3>
            </div>
            <div class="side-bar-panel">
                <div class="side-bar-item" :class="{ active: currentRoute === 'user-info' }" @click="handleRedirect('user-info')">
                    <div class="icon-wrapper">
                        <svg  xmlns="http://www.w3.org/2000/svg" width="22" height="22"
                            fill="currentColor" viewBox="0 0 24 24" class="side-bar-icon">
                            <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                            <path d="M12 6c-2.28 0-4 1.72-4 4s1.72 4 4 4 4-1.72 4-4-1.72-4-4-4m0 6c-1.18 0-2-.82-2-2s.82-2 2-2 2 .82 2 2-.82 2-2 2"></path><path d="M12 2C6.49 2 2 6.49 2 12c0 3.26 1.58 6.16 4 7.98V20h.03c1.67 1.25 3.73 2 5.97 2s4.31-.75 5.97-2H18v-.02c2.42-1.83 4-4.72 4-7.98 0-5.51-4.49-10-10-10M8.18 19.02C8.59 17.85 9.69 17 11 17h2c1.31 0 2.42.85 2.82 2.02-1.14.62-2.44.98-3.82.98s-2.69-.35-3.82-.98m9.3-1.21c-.81-1.66-2.51-2.82-4.48-2.82h-2c-1.97 0-3.66 1.16-4.48 2.82A7.96 7.96 0 0 1 4 11.99c0-4.41 3.59-8 8-8s8 3.59 8 8c0 2.29-.97 4.36-2.52 5.82"></path>
                        </svg>
                    </div>
                    <span class="item-text">个人信息</span>
                    <div class="active-indicator"></div>
                </div>
                <div class="side-bar-item" :class="{ active: currentRoute === 'health-records' }" @click="handleRedirect('health-records')">
                    <div class="icon-wrapper">
                        <svg  xmlns="http://www.w3.org/2000/svg" width="22" height="22"
                            fill="currentColor" viewBox="0 0 24 24" class="side-bar-icon">
                            <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2M5 19V5h14v14z"></path><path d="M8.5 10.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 1 0 0-3m2.5.5h6v2h-6zM7 7h10v2H7zm0 8h10v2H7z"></path>
                        </svg>
                    </div>
                    <span class="item-text">健康档案</span>
                    <div class="active-indicator"></div>
                </div>
                <div class="side-bar-item" :class="{ active: currentRoute === 'security-center' }" @click="handleRedirect('security-center')">
                    <div class="icon-wrapper">
                        <svg  xmlns="http://www.w3.org/2000/svg" width="22" height="22"
                            fill="currentColor" viewBox="0 0 24 24" class="side-bar-icon">
                            <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                            <path d="m20.42 6.11-7.97-4c-.28-.14-.62-.14-.9 0l-7.97 4c-.31.15-.51.45-.55.79-.01.11-.96 10.76 8.55 15.01a.98.98 0 0 0 .82 0C21.91 17.66 20.97 7 20.95 6.9a.98.98 0 0 0-.55-.79ZM12 19.9C5.26 16.63 4.94 9.64 5 7.64l7-3.51 7 3.51c.04 1.99-.33 9.02-7 12.26"></path><path d="m11 12.59-1.29-1.3-1.42 1.42 2.71 2.7 4.71-4.7-1.42-1.42z"></path>
                        </svg>
                    </div>
                    <span class="item-text">安全中心</span>
                    <div class="active-indicator"></div>
                </div>
            </div>
        </div>
        <div class="content-wrapper">
            <router-view v-slot="{ Component }">
                <transition name="bounce" mode="out-in"> 
                    <component :is="Component" />
                </transition>
            </router-view>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { useRouter, useRoute } from 'vue-router';
    import { computed } from 'vue';

    // 初始化路由对象
    const router = useRouter()
    const route = useRoute()

    // 获取当前路由名称
    const currentRoute = computed(() => {
        const path = route.path
        if (path.includes('user-info')) return 'user-info'
        if (path.includes('health-records')) return 'health-records'
        if (path.includes('security-center')) return 'security-center'
        return ''
    })

    /**
     * 绑定返回事件
     */
    const backHome = () => {
        router.replace('/')
    }


    /**
     * 子路由跳转函数
     */
    const handleRedirect = (routerName: string) => {
        router.replace(`/user-center/${routerName}`)
    }

</script>

<style scoped>
    .user-center-container {
        width: 100%;
        height: 100%;
        display: flex;
    }

    .control-wrapper {
        height: 100%;
        width: 25%;
        min-width: 200px;
        user-select: none;
        background: linear-gradient(160deg, #6b8cf5 0%, #7d9cf0 40%, #8aa7f0 80%, #9bb3f0 100%);
        position: relative;
        overflow: hidden;
    }

    /* 侧边栏底部装饰 */
    .control-wrapper::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 120px;
        background: linear-gradient(to top, rgba(255,255,255,0.08) 0%, transparent 100%);
        pointer-events: none;
    }

    /* 顶部装饰圆点 */
    .control-wrapper::before {
        content: '';
        position: absolute;
        top: -30px;
        right: -30px;
        width: 100px;
        height: 100px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        pointer-events: none;
    }

    .top-panel {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 10px;
        color: #fff;
        padding: 20px 25px;
    }

    .back-btn {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        border: none;
        transition: all 0.6s ease;
        cursor: pointer;
    }

    .back-btn:hover {
        background-color: #fff;
        transform: scale(1.2);
    }

    .side-bar-panel {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0 15px;
    }

    .side-bar-item {
        position: relative;
        font-weight: 500;
        font-size: 15px;
        width: 100%;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 14px;
        color: rgba(255, 255, 255, 0.75);
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        margin-bottom: 8px;
        padding: 0 18px;
        overflow: hidden;
    }

    .side-bar-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
        border-radius: 12px;
    }

    .side-bar-item:hover {
        color: #fff;
        transform: translateX(6px);
        background: rgba(255, 255, 255, 0.1);
    }

    .side-bar-item:hover::before {
        opacity: 1;
    }

    .side-bar-item.active {
        color: #fff;
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .side-bar-item.active::before {
        opacity: 1;
    }

    /* 左侧激活指示条 */
    .active-indicator {
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 0;
        background: #fff;
        border-radius: 0 4px 4px 0;
        transition: height 0.3s ease;
    }

    .side-bar-item.active .active-indicator {
        height: 24px;
    }

    .icon-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        transition: all 0.3s ease;
        flex-shrink: 0;
    }

    .side-bar-item:hover .icon-wrapper {
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.1);
    }

    .side-bar-item.active .icon-wrapper {
        background: rgba(255, 255, 255, 0.25);
    }

    .side-bar-icon {
        transition: transform 0.3s ease;
    }

    .item-text {
        position: relative;
        z-index: 1;
        letter-spacing: 0.5px;
    }

    .content-wrapper {
        padding: 5px;
        width: 75%;
        overflow: hidden;
        position: relative; /* 为动画提供定位上下文 */
        min-height: 500px; /* 防止动画时高度抖动 */
    }

    /* 果冻弹跳动画 - 特别适合你的可爱风格！ */
    .bounce-enter-active {
        animation: bounce-in 0.6s;
    }

    .bounce-leave-active {
        animation: bounce-out 0.5s;
    }

    @keyframes bounce-in {
        0% {
            transform: scale(0.9);
            opacity: 0;
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
        }

        @keyframes bounce-out {
        0% {
            transform: scale(1);
            opacity: 1;
        }
        100% {
            transform: scale(0.9);
            opacity: 0;
        }
    }
</style>