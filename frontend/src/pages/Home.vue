<template>
    <div class="home-container">
        <!-- 遮罩层: 实现点击空白区域关闭卡片 -->
        <div class="overlay" v-if="activeCard" @click="closeCard"></div>
        <!-- 卡片布局容器 -->
        <div class="grid-container" :class="{ 'has-active': activeCard }">
            <!-- 卡片A: 今日用药 -->
            <div
            class="card A"
            :class="{ active: activeCard === 'A' }"
            @click="openCard('A')"
            >
                <div class="card-content">
                    今日用药
                </div>
            </div>

            <!-- 卡片B: 用户中心 -->
            <div
            class="card B"
            :class="{ active: activeCard === 'B' }"
            @click="openCard('B')"
            >
                <div class="card-content">
                    用户中心
                </div>
            </div>

            <!-- 卡片C: 药品管理 -->
            <div
            class="card C"
            :class="{ active: activeCard === 'C' }"
            @click="openCard('C')"
            >
                <div class="card-content">
                    药品管理
                </div>
            </div>

            <!-- 卡片D: 计划管理 -->
            <div
            class="card D"
            :class="{ active: activeCard === 'D' }"
            @click="openCard('D')"
            >
                <div class="card-content">
                    计划管理
                </div>
            </div>

            <!-- 卡片E: 关系管理 -->
            <div
            class="card E"
            :class="{ active: activeCard === 'E' }"
            @click="openCard('E')"
            >
                <div class="card-content">
                    关系管理
                </div>
            </div>

            <!-- 子路由视图 -->
            <div class="sub-page">
                <router-view />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    // 路由管理对象
    const router = useRouter()

    // 状态管理变量: 记录当前激活的卡片
    const activeCard = ref<string|null>(null)

    // 卡片到路由的映射
    const cardRoutes: Record<string, string> = {
        'A': '/today-medicine',
        'B': '/user-center',
        'C': '/medicine-management',
        'D': '/plan-management',
        'E': '/relationship-management'
    }

    /**
     * 关闭卡片方法
     */
    const closeCard = () => {
        // 打印调试信息
        console.log(`已经关闭了卡片${activeCard.value}`)
        // 修改状态变量
        activeCard.value = null
        // 更改路由
        router.replace('/')
    }

    /**
     * 打开卡片方法
     */
    const openCard = (cardName: string) => {
        // 修改状态变量
        activeCard.value = cardName
        // 打印调试信息
        console.log(`已经打开了卡片${activeCard.value}`)
        // 更改路由
        router.replace(cardRoutes[cardName]!)
    }

</script>

<style scoped>
    .home-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(90deg, #e2e2e2, #c9d6ff);
    }

    .grid-container {
        width: 900px;
        height: 650px;
        gap: 10px;
        position: relative;
    }

    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
    }

    .card {
        position: absolute;
        background-color: #fff;
        border-radius: 30px;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
        text-align: center;
        cursor: pointer;
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
        z-index: 2;
    }
    .card:hover {
        box-shadow: 0 0 30px #7494ec;
        transform: translateY(-5px);
    }

    .card .card-content {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        width: 100%;
        font-weight: 600;
        transition: all 0.6s ease;
    }

    .card.A {
        top: 0;
        left: 0;
        width: 80%;
        height: 80%;
    }
    .card.B {
        top: 0;
        right: 0;
        width: 18%;
        height: 80%;
    }
    .card.C {
        bottom: 0;
        left: 0;
        width: 39%;
        height: 18%;
    }
    .card.D {
        bottom: 0;
        left: 41%;
        width: 39%;
        height: 18%;
    }
    .card.E {
        bottom: 0;
        right: 0;
        width: 18%;
        height: 18%;
    }

    .card.active .card-content {
        opacity: 0
    }

    .has-active .card:not(.active) {
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
    }
    
    .card.active {
        width: 100%;
        height: 100%;
        z-index: 2;
    }

    .card.D.active {
        left: 0;
    }

    .sub-page {
        position: absolute;
        left: 0;
        top: 0;
        opacity: 0;
        width: 100%;
        height: 100%;
        background-color: #fff;
        border-radius: 30px;
        z-index: 1;
    }

    .has-active .sub-page {
        opacity: 1;
        transition: opacity 0.3s ease;
        z-index: 3;
        transition-delay: 0.6s;
    }
</style>