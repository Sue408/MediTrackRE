<template>
    <div class="drug-card-container">
        <!-- 药品图标 -->
        <div class="drug-icon">
            <img v-if="drug.image" :src="drug.image" :alt="drug.name">
            <div v-else class="icon-placeholder">
                <svg  xmlns="http://www.w3.org/2000/svg" width="32" height="32"  
                    fill="currentColor" viewBox="0 0 24 24" >
                    <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                    <path d="M18 6h-1V4c0-1.1-.9-2-2-2H9c-1.1 0-2 .9-2 2v2H6c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2M9 4h6v2H9zM6 20V8h12v12z"></path><path d="M13 10h-2v3H8v2h3v3h2v-3h3v-2h-3z"></path>
                </svg>
            </div>
        </div>

        <!-- 药品信息 -->
        <div class="drug-info">
            <!-- 药品名称 -->
            <h4 class="drug-name">{{ drug.name }}</h4>
            <!-- 药品用法和用量 -->
            <div class="drug-tags">
                <span class="tag usage-tag">{{ drug.usage_method }}</span>
                <span class="tag dosage-tag">{{ drug.dosage }}</span>
            </div>
        </div>

        <!-- 操作按钮 -->
        <div class="drug-actions">
            <button class="action-btn edit-btn" @click.stop="$emit('editDrug', drug.id)" title="编辑">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z" fill="currentColor"/>
                </svg>
            </button>
            <button class="action-btn delete-btn" @click.stop="$emit('deleteDrug', drug.id)" title="删除">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M6 19C6 20.1 6.9 21 8 21H16C17.1 21 18 20.1 18 19V7H6V19ZM19 4H15.5L14.5 3H9.5L8.5 4H5V6H19V4Z" fill="currentColor"/>
                </svg>
            </button>
        </div>

        <!-- 悬浮装饰 -->
        <div class="hover-decoration">
            <span class="deco-circle"></span>
            <span class="deco-circle"></span>
        </div>
    </div>
</template>

<script setup lang="ts"> 
    import type { Drug } from '@/types/drugTypes'

    // 定义药品信息插槽
    const props = defineProps<{drug: Drug}>()

</script>

<style scoped>
    .drug-card-container {
        width: 100%;
        height: 100px;
        position: relative;
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 18px;
        background: #fff;
        border-radius: 24px;
        box-shadow: 0 4px 20px rgba(116, 148, 236, 0.25);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
    }

    .drug-card-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(116, 148, 236, 0.5);
    }

    /* 药品图标 */
    .drug-icon {
        position: relative;
        width: 70px;
        height: 70px;
        border-radius: 18px;
        overflow: hidden;
        flex-shrink: 0;
        background: linear-gradient(135deg, #f0f4ff 0%, #e8f0ff 100%);
    }

    .drug-icon img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .icon-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #7494ec;
    }

    /* 药品信息 */
    .drug-info {
        flex: 1;
        min-width: 0;
        overflow: hidden;
    }

    .drug-name {
        margin: 0 0 8px 0;
        font-size: 16px;
        font-weight: 600;
        color: #333;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .drug-tags {
        display: flex;
        gap: 8px;
        margin-bottom: 8px;
    }

    .tag {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }

    .usage-tag {
        background: linear-gradient(135deg, #e0effe 0%, #d0ebfe 100%);
        color: #0284c7;
    }

    .dosage-tag {
        background: #f3f4f6;
        color: #6b7280;
    }

    /* 操作按钮 */
    .drug-actions {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .action-btn {
        width: 28px;
        height: 28px;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .edit-btn {
        background: linear-gradient(135deg, #e0effe 0%, #d0ebfe 100%);
        color: #0284c7;
    }

    .edit-btn:hover {
        background: linear-gradient(135deg, #7494ec 0%, #5a7de0 100%);
        color: #fff;
        transform: scale(1.1);
    }

    .delete-btn {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #ef4444;
    }

    .delete-btn:hover {
        background: linear-gradient(135deg, #ff6b6b 0%, #e05555 100%);
        color: #fff;
        transform: scale(1.1);
    }

    /* 悬浮装饰 */
    .hover-decoration {
        position: absolute;
        top: -20px;
        right: -20px;
        pointer-events: none;
    }

    .deco-circle {
        position: absolute;
        border-radius: 50%;
        background: rgba(116, 148, 236, 0.1);
        transition: all 0.4s ease;
    }

    .deco-circle:first-child {
        width: 60px;
        height: 60px;
        top: 10px;
        right: 10px;
    }

    .deco-circle:last-child {
        width: 40px;
        height: 40px;
        top: 30px;
        right: 40px;
    }

    .drug-card.is-hovered .deco-circle {
        transform: scale(1.2);
    }
</style>