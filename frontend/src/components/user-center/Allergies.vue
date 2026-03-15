<template>
    <div class="allergies-container">
        <div class="card-header">
            <h4>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM15.5 11C16.33 11 17 10.33 17 9.5C17 8.67 16.33 8 15.5 8C14.67 8 14 8.67 14 9.5C14 10.33 14.67 11 15.5 11ZM8.5 11C9.33 11 10 10.33 10 9.5C10 8.67 9.33 8 8.5 8C7.67 8 7 8.67 7 9.5C7 10.33 7.67 11 8.5 11ZM12 17.5C14.33 17.5 16.31 16.04 17.11 14H6.89C7.69 16.04 9.67 17.5 12 17.5Z" fill="#ff6b6b"/>
                </svg>
                过敏史
            </h4>
            <button class="add-btn" @click="showAddModal = true">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
                </svg>
                添加
            </button>
        </div>

        <div class="card-body">
            <div v-if="allergies.length > 0" class="tag-list">
                <div v-for="(allergy, index) in allergies" :key="index" class="tag-item">
                    <div class="tag-content">
                        <span class="tag-name">{{ allergy.name }}</span>
                        <span class="tag-reaction">{{ allergy.reaction }}</span>
                    </div>
                    <button class="delete-btn" @click="removeAllergy(index)">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                            <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
                        </svg>
                    </button>
                </div>
            </div>
            <div v-else class="empty-tip">
                <span>暂无过敏史</span>
            </div>
        </div>

        <!-- 添加过敏史弹窗 -->
        <div class="modal-overlay" v-if="showAddModal" @click.self="showAddModal = false">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>添加过敏史</h3>
                    <button class="close-btn" @click="showAddModal = false">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                            <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
                        </svg>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label>过敏原名称 *</label>
                        <input type="text" v-model="newAllergy.name" placeholder="如: 青霉素">
                    </div>
                    <div class="form-group">
                        <label>过敏反应 *</label>
                        <input type="text" v-model="newAllergy.reaction" placeholder="如: 皮疹、呼吸困难">
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-btn" @click="showAddModal = false">取消</button>
                    <button class="confirm-btn" @click="addAllergy">添加</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, computed } from 'vue'
    import { updateProfile } from '@/api/user'
    import type { AllergyItem } from '@/types/userTypes'

    // 接收父组件传递的数据
    const props = defineProps<{
        profile: {
            allergies: AllergyItem[]
        }
    }>()

    const emit = defineEmits<{
        'refresh': []
    }>()

    // 使用计算属性获取过敏史列表
    const allergies = computed(() => props.profile.allergies || [])

    // 弹窗状态
    const showAddModal = ref(false)

    // 新增过敏史
    const newAllergy = reactive({
        name: '',
        reaction: ''
    })

    // 添加过敏史
    const addAllergy = async () => {
        if (!newAllergy.name || !newAllergy.reaction) {
            alert('请填写完整信息')
            return
        }

        const allgeries: AllergyItem[] = [...allergies.value, { ...newAllergy }]
        try {
            await updateProfile({ allergies: allgeries })
            showAddModal.value = false
            newAllergy.name = ''
            newAllergy.reaction = ''
            emit('refresh')
        } catch (error) {
            console.error('添加过敏史失败:', error)
        }
    }

    // 删除过敏史
    const removeAllergy = async (index: number) => {
        const allgeries = allergies.value.filter((_, i) => i !== index)
        try {
            await updateProfile({ allergies: allgeries })
            emit('refresh')
        } catch (error) {
            console.error('删除过敏史失败:', error)
        }
    }
</script>

<style scoped>
    .allergies-container {
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        overflow: hidden;
    }

    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 20px;
        border-bottom: 1px solid #f0f0f0;
    }

    .card-header h4 {
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
        color: #333;
        font-size: 16px;
    }

    .add-btn {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 8px 16px;
        border: none;
        border-radius: 15px;
        background: #e3edff;
        color: #7494ec;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .add-btn:hover {
        background: #7494ec;
        color: #fff;
    }

    .card-body {
        padding: 20px;
    }

    .tag-list {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
    }

    .tag-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 16px;
        background: #fff5f5;
        border-radius: 15px;
        transition: all 0.3s ease;
    }

    .tag-item:hover {
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.2);
    }

    .tag-content {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .tag-name {
        color: #ff6b6b;
        font-weight: 500;
    }

    .tag-reaction {
        font-size: 12px;
        color: #999;
    }

    .delete-btn {
        width: 24px;
        height: 24px;
        border: none;
        border-radius: 50%;
        background: rgba(255, 107, 107, 0.1);
        color: #ff6b6b;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .delete-btn:hover {
        background: #ff6b6b;
        color: #fff;
    }

    .empty-tip {
        text-align: center;
        padding: 30px;
        color: #999;
    }

    /* 弹窗样式 */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 100;
    }

    .modal-content {
        width: 90%;
        max-width: 400px;
        background: #fff;
        border-radius: 25px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    }

    .modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 25px;
        border-bottom: 1px solid #f0f0f0;
    }

    .modal-header h3 {
        margin: 0;
        color: #333;
    }

    .close-btn {
        width: 32px;
        height: 32px;
        border: none;
        background: #f5f5f5;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .close-btn:hover {
        background: #e0e0e0;
    }

    .modal-body {
        padding: 25px;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-group:last-child {
        margin-bottom: 0;
    }

    .form-group label {
        display: block;
        margin-bottom: 8px;
        color: #666;
        font-size: 14px;
    }

    .form-group input {
        width: 100%;
        padding: 12px 15px;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        font-size: 14px;
        outline: none;
        transition: border-color 0.3s ease;
    }

    .form-group input:focus {
        border-color: #7494ec;
    }

    .modal-footer {
        display: flex;
        gap: 15px;
        justify-content: flex-end;
        padding: 20px 25px;
        border-top: 1px solid #f0f0f0;
    }

    .modal-footer .cancel-btn,
    .modal-footer .confirm-btn {
        padding: 10px 20px;
        border: none;
        border-radius: 15px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .modal-footer .cancel-btn {
        background: #f5f5f5;
        color: #666;
    }

    .modal-footer .confirm-btn {
        background: #7494ec;
        color: #fff;
    }

    .modal-footer .confirm-btn:hover {
        background: #5a7de0;
    }
</style>