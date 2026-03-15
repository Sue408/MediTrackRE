<template>
    <transition name="modal-fade">
        <div v-if="visible" class="confirm-overlay" @click.self="handleCancel">
            <div class="confirm-dialog">
                <!-- 图标 -->
                <div class="confirm-icon" :class="type">
                    <svg v-if="type === 'danger'" width="28" height="28" viewBox="0 0 24 24" fill="none">
                        <path d="M6 19C6 20.1 6.9 21 8 21H16C17.1 21 18 20.1 18 19V7H6V19ZM19 4H15.5L14.5 3H9.5L8.5 4H5V6H19V4Z" fill="currentColor"/>
                    </svg>
                    <svg v-else-if="type === 'warning'" width="28" height="28" viewBox="0 0 24 24" fill="none">
                        <path d="M1 21H23L12 2L1 21ZM13 18H11V16H13V18ZM13 14H11V10H13V14Z" fill="currentColor"/>
                    </svg>
                    <svg v-else width="28" height="28" viewBox="0 0 24 24" fill="none">
                        <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM11 7H13V13H11V7ZM11 15H13V17H11V15Z" fill="currentColor"/>
                    </svg>
                </div>

                <!-- 内容 -->
                <div class="confirm-content">
                    <h4 class="confirm-title">{{ title }}</h4>
                    <p class="confirm-message">{{ message }}</p>
                </div>

                <!-- 操作按钮 -->
                <div class="confirm-actions">
                    <button class="btn-cancel" @click="handleCancel">
                        {{ cancelText }}
                    </button>
                    <button class="btn-confirm" :class="type" @click="handleConfirm" :disabled="loading">
                        <span v-if="loading" class="btn-spinner"></span>
                        {{ loading ? loadingText : confirmText }}
                    </button>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
    interface Props {
        visible: boolean
        title?: string
        message: string
        type?: 'danger' | 'warning' | 'info'
        confirmText?: string
        cancelText?: string
        loadingText?: string
        loading?: boolean
    }

    withDefaults(defineProps<Props>(), {
        title: '确认操作',
        type: 'danger',
        confirmText: '确认',
        cancelText: '取消',
        loadingText: '处理中...',
        loading: false
    })

    const emit = defineEmits<{
        'confirm': []
        'cancel': []
    }>()

    const handleConfirm = () => {
        emit('confirm')
    }

    const handleCancel = () => {
        emit('cancel')
    }
</script>

<style scoped>
    .confirm-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1100;
        backdrop-filter: blur(4px);
    }

    .confirm-dialog {
        width: 90%;
        max-width: 360px;
        background: #fff;
        border-radius: 24px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
    }

    /* 图标 */
    .confirm-icon {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        margin: 0 auto 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .confirm-icon.danger {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #ef4444;
    }

    .confirm-icon.warning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #f59e0b;
    }

    .confirm-icon.info {
        background: linear-gradient(135deg, #e0effe 0%, #d0ebfe 100%);
        color: #0284c7;
    }

    /* 内容 */
    .confirm-content {
        margin-bottom: 24px;
    }

    .confirm-title {
        margin: 0 0 8px;
        font-size: 18px;
        font-weight: 600;
        color: #333;
    }

    .confirm-message {
        margin: 0;
        font-size: 14px;
        color: #666;
        line-height: 1.6;
    }

    /* 操作按钮 */
    .confirm-actions {
        display: flex;
        gap: 12px;
        justify-content: center;
    }

    .btn-cancel,
    .btn-confirm {
        flex: 1;
        padding: 12px 20px;
        border: none;
        border-radius: 16px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .btn-cancel {
        background: #f5f5f5;
        color: #666;
    }

    .btn-cancel:hover {
        background: #e0e0e0;
    }

    .btn-confirm {
        color: #fff;
    }

    .btn-confirm.danger {
        background: linear-gradient(135deg, #ff6b6b 0%, #e05555 100%);
    }

    .btn-confirm.danger:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }

    .btn-confirm.warning {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    }

    .btn-confirm.warning:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.4);
    }

    .btn-confirm.info {
        background: linear-gradient(135deg, #7494ec 0%, #5a7de0 100%);
    }

    .btn-confirm.info:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(116, 148, 236, 0.4);
    }

    .btn-confirm:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .btn-spinner {
        display: inline-block;
        width: 14px;
        height: 14px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top-color: #fff;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-right: 6px;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* 动画 */
    .modal-fade-enter-active,
    .modal-fade-leave-active {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .modal-fade-enter-from,
    .modal-fade-leave-to {
        opacity: 0;
    }

    .modal-fade-enter-from .confirm-dialog,
    .modal-fade-leave-to .confirm-dialog {
        transform: scale(0);
    }
</style>