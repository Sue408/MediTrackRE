<template>
    <div class="plan-list-container">
        <!-- 计划网格视图 -->
        <div class="plan-list-wrapper" v-if="planList.length > 0">
            <transition-group name="plan-list" tag="div" class="plan-list">
                <PlanCard
                    v-for="plan in planList"
                    :key="plan.id"
                    :plan="plan"
                    @pause="$emit('pause', plan)"
                    @resume="$emit('resume', plan)"
                    @edit="$emit('edit', plan)"
                    @delete="$emit('delete', plan)"
                />
            </transition-group>
        </div>

        <!-- 空白视图 -->
        <div class="empty-state" v-else>
            <div class="empty-illustration">
                <svg width="100" height="100" viewBox="0 0 24 24" fill="none">
                    <path d="M19 4H5C3.89 4 3 4.9 3 6V20C3 21.1 3.89 22 5 22H19C20.1 22 21 21.1 21 20V6C21 4.9 20.1 4 19 4ZM19 20H5V9H19V20ZM7 11H12V13H7V11ZM7 15H15V17H7V15Z" fill="#e0e0e0"/>
                </svg>

                <div class="floating-plans">
                    <span class="plan-float plan-float-1"></span>
                    <span class="plan-float plan-float-2"></span>
                    <span class="plan-float plan-float-3"></span>
                </div>
            </div>
            <h4>还没有添加计划</h4>
            <p>点击下方按钮创建您的第一个用药计划吧</p>
            <button class="add-first-btn" @click="$emit('addPlan')">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
                </svg>
                创建第一个计划
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import type { Plan } from '@/types/planTypes'
    import PlanCard from './PlanCard.vue'

    const props = defineProps<{
        planList: Plan[]
    }>()

    defineEmits<{
        'pause': [plan: Plan]
        'resume': [plan: Plan]
        'edit': [plan: Plan]
        'delete': [plan: Plan]
        'addPlan': []
    }>()

</script>

<style scoped>
    .plan-list-container {
        height: 100%;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow-y: auto;
    }

    .plan-list-container::-webkit-scrollbar {
        width: 0;
    }

    /* 计划列表 */
    .plan-list-wrapper {
        width: 100%;
        height: 100%;
    }

    .plan-list {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .plan-item {
        animation: slideUp 0.4s ease forwards;
        opacity: 0;
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* 列表动画 */
    .plan-list-enter-active,
    .plan-list-leave-active {
        transition: all 0.4s ease;
    }

    .plan-list-enter-from {
        opacity: 0;
        transform: scale(0.9);
    }

    .plan-list-leave-to {
        opacity: 0;
        transform: scale(0.9);
    }

    /* 空状态 */
    .empty-state {
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 20px;
        text-align: center;
    }

    .empty-illustration {
        position: relative;
        margin-bottom: 24px;
    }

    .empty-illustration svg {
        animation: float 3s ease-in-out infinite;
    }

    .floating-plans {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
    }

    .plan-float {
        position: absolute;
        border-radius: 8px;
        opacity: 0.6;
    }

    .plan-float-1 {
        width: 20px;
        height: 20px;
        background: linear-gradient(135deg, #7494ec 0%, #5a7de0 100%);
        top: 10px;
        left: -20px;
        animation: planFloat1 4s ease-in-out infinite;
    }

    .plan-float-2 {
        width: 15px;
        height: 15px;
        background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
        top: 50px;
        right: -15px;
        animation: planFloat2 5s ease-in-out infinite;
    }

    .plan-float-3 {
        width: 12px;
        height: 12px;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        bottom: 20px;
        left: -10px;
        animation: planFloat3 4.5s ease-in-out infinite;
    }

    @keyframes planFloat1 {
        0%, 100% { transform: translateY(0) rotate(-10deg); }
        50% { transform: translateY(-15px) rotate(10deg); }
    }

    @keyframes planFloat2 {
        0%, 100% { transform: translateY(0) rotate(15deg); }
        50% { transform: translateY(-10px) rotate(-15deg); }
    }

    @keyframes planFloat3 {
        0%, 100% { transform: translateY(0) rotate(-5deg); }
        50% { transform: translateY(-12px) rotate(5deg); }
    }

    .empty-state h4 {
        margin: 0 0 8px;
        font-size: 18px;
        font-weight: 600;
        color: #333;
    }

    .empty-state p {
        margin: 0 0 24px;
        font-size: 14px;
        color: #999;
    }

    .add-first-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 14px 32px;
        border: none;
        border-radius: 25px;
        background: linear-gradient(135deg, #7494ec 0%, #5a7de0 100%);
        color: #fff;
        font-size: 15px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(116, 148, 236, 0.3);
    }

    .add-first-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(116, 148, 236, 0.4);
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
</style>