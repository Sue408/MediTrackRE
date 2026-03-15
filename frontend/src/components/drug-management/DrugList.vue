<template>
    <div class="drug-list-container">
        <!-- 药品网格视图 -->
        <div class="drug-list-wrapper" v-if="drugInfoList.length > 0">
            <transition-group name="drug-list" tag="div" class="drug-list">
                <DrugCard
                 v-for="drug in drugInfoList"
                :key="drug.id"
                :drug="drug"
                @editDrug="$emit('editDrug', drug.id)"
                @deleteDrug="$emit('deleteDrug', drug.id)"
                />
            </transition-group>
        </div>

        <!-- 空白视图 -->
        <div class="empty-state" v-else>
            <div class="empty-illustration">
                <svg width="100" height="100" viewBox="0 0 24 24" fill="none">
                    <path d="M4.22 11.29L11.29 4.22C11.68 3.83 12.32 3.83 12.71 4.22L19.78 11.29C20.17 11.68 20.17 12.32 19.78 12.71L12.71 19.78C12.32 20.17 11.68 20.17 11.29 19.78L4.22 12.71C3.83 12.32 3.83 11.68 4.22 11.29Z" fill="#e0e0e0"/>
                    <circle cx="12" cy="12" r="3" fill="#e0e0e0"/>
                </svg>

                <div class="floating-pills">
                    <span class="pill pill-1"></span>
                    <span class="pill pill-2"></span>
                    <span class="pill pill-3"></span>
                </div>
            </div>
            <h4>还没有添加药品</h4>
            <p>点击下方按钮添加您的第一种药品吧</p>
            <button class="add-first-btn" @click="$emit('addDrug')">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
                </svg>
                添加第一个药品
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import type { Drug } from '@/types/drugTypes'
    import DrugCard from '@/components/drug-management/DrugCard.vue'

    // 定义药物列表插槽
    const props = defineProps<{
        drugInfoList: Drug[]
    }>()

    // 传递删除方法

</script>

<style scoped>
    .drug-list-container {
        height: 100%;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow-y: auto;
    }

    .drug-list-container::-webkit-scrollbar {
        width: 0;
    }

    /* 药品列表 */
    .drug-list-wrapper {
        width: 100%;
        height: 100%;
    }

    .drug-list {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }

    .drug-item {
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
    .drug-list-enter-active,
    .drug-list-leave-active {
        transition: all 0.4s ease;
    }

    .drug-list-enter-from {
        opacity: 0;
        transform: scale(0.9);
    }

    .drug-list-leave-to {
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

    .floating-pills {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
    }

    .pill {
        position: absolute;
        border-radius: 8px;
        opacity: 0.6;
    }

    .pill-1 {
        width: 20px;
        height: 10px;
        background: linear-gradient(135deg, #7494ec 0%, #5a7de0 100%);
        top: 10px;
        left: -20px;
        animation: pillFloat1 4s ease-in-out infinite;
    }

    .pill-2 {
        width: 15px;
        height: 8px;
        background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
        top: 50px;
        right: -15px;
        animation: pillFloat2 5s ease-in-out infinite;
    }

    .pill-3 {
        width: 12px;
        height: 6px;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        bottom: 20px;
        left: -10px;
        animation: pillFloat3 4.5s ease-in-out infinite;
    }

    @keyframes pillFloat1 {
        0%, 100% { transform: translateY(0) rotate(-10deg); }
        50% { transform: translateY(-15px) rotate(10deg); }
    }

    @keyframes pillFloat2 {
        0%, 100% { transform: translateY(0) rotate(15deg); }
        50% { transform: translateY(-10px) rotate(-15deg); }
    }

    @keyframes pillFloat3 {
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
</style>