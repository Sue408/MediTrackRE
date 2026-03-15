<template>
    <div class="diseases-container">
        <div class="card-header">
            <h4>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M19 3H5C3.89 3 3 4.57 3 6V20C3 21.1 3.89 22 5 22H19C20.1 22 21 21.1 21 20V6C21 4.57 20.1 3 19 3ZM19 19H5V9H19V19ZM7 11H12V13H7V11ZM7 15H17V17H7V15Z" fill="#ff9800"/>
                </svg>
                疾病史
            </h4>
            <button class="add-btn" @click="showAddModal = true">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
                </svg>
                添加
            </button>
        </div>

        <div class="card-body">
            <div v-if="diseases.length > 0" class="disease-list">
                <div v-for="(disease, index) in diseases" :key="index" class="disease-item">
                    <div class="disease-info">
                        <span class="disease-name">{{ disease.name }}</span>
                        <span class="disease-date">确诊: {{ formatDate(disease.diagnosed_at) }}</span>
                    </div>
                    <span class="disease-status" :class="disease.status">{{ disease.status }}</span>
                    <button class="delete-btn" @click="removeDisease(index)">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                            <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
                        </svg>
                    </button>
                </div>
            </div>
            <div v-else class="empty-tip">
                <span>暂无疾病史</span>
            </div>
        </div>

        <!-- 添加疾病史弹窗 -->
        <div class="modal-overlay" v-if="showAddModal" @click.self="showAddModal = false">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>添加疾病史</h3>
                    <button class="close-btn" @click="showAddModal = false">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                            <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
                        </svg>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label>疾病名称 *</label>
                        <input type="text" v-model="newDisease.name" placeholder="如: 高血压">
                    </div>
                    <div class="form-group">
                        <label>确诊日期 *</label>
                        <input type="date" v-model="newDisease.diagnosed_at">
                    </div>
                    <div class="form-group">
                        <label>当前状态 *</label>
                        <FlowSelect
                            v-model="newDisease.status"
                            :options="statusOptions"
                            placeholder="请选择状态"
                        />
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-btn" @click="showAddModal = false">取消</button>
                    <button class="confirm-btn" @click="addDisease">添加</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, computed } from 'vue'
    import { updateProfile } from '@/api/user'
    import type { DiseaseItem } from '@/types/userTypes'
    import FlowSelect from '@/components/common/FlowSelect.vue'

    // 接收父组件传递的数据
    const props = defineProps<{
        profile: {
            diseases: DiseaseItem[]
        }
    }>()

    const emit = defineEmits<{
        'refresh': []
    }>()

    // 使用计算属性获取疾病史列表
    const diseases = computed(() => props.profile.diseases || [])

    // 弹窗状态
    const showAddModal = ref(false)

    // 新增疾病史
    const newDisease = reactive({
        name: '',
        diagnosed_at: '',
        status: '治疗中'
    })

    // 状态选项
    const statusOptions = [
        { value: '治疗中', label: '治疗中' },
        { value: '已控制', label: '已控制' },
        { value: '已痊愈', label: '已痊愈' }
    ]

    // 添加疾病史
    const addDisease = async () => {
        if (!newDisease.name || !newDisease.diagnosed_at) {
            alert('请填写完整信息')
            return
        }

        const diseaseList: DiseaseItem[] = [...diseases.value, { ...newDisease }]
        try {
            await updateProfile({ diseases: diseaseList })
            showAddModal.value = false
            newDisease.name = ''
            newDisease.diagnosed_at = ''
            newDisease.status = '治疗中'
            emit('refresh')
        } catch (error) {
            console.error('添加疾病史失败:', error)
        }
    }

    // 删除疾病史
    const removeDisease = async (index: number) => {
        const diseaseList = diseases.value.filter((_, i) => i !== index)
        try {
            await updateProfile({ diseases: diseaseList })
            emit('refresh')
        } catch (error) {
            console.error('删除疾病史失败:', error)
        }
    }

    // 格式化日期
    const formatDate = (dateStr: string) => {
        if (!dateStr) return '-'
        const date = new Date(dateStr)
        return date.toLocaleDateString('zh-CN')
    }
</script>

<style scoped>
    .diseases-container {
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

    .disease-list {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .disease-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px;
        background: #fff8f0;
        border-radius: 15px;
    }

    .disease-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .disease-name {
        color: #ff9800;
        font-weight: 500;
    }

    .disease-date {
        font-size: 12px;
        color: #999;
    }

    .disease-status {
        padding: 4px 12px;
        border-radius: 10px;
        font-size: 12px;
    }

    .disease-status.治疗中 {
        background: #fff3e0;
        color: #ff9800;
    }

    .disease-status.已控制 {
        background: #e3edff;
        color: #7494ec;
    }

    .disease-status.已痊愈 {
        background: #e8f5e9;
        color: #4caf50;
    }

    .delete-btn {
        width: 24px;
        height: 24px;
        border: none;
        border-radius: 50%;
        background: rgba(255, 152, 0, 0.1);
        color: #ff9800;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .delete-btn:hover {
        background: #ff9800;
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

    .form-group input,
    .form-group select {
        width: 100%;
        padding: 12px 15px;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        font-size: 14px;
        outline: none;
        transition: border-color 0.3s ease;
    }

    .form-group input:focus,
    .form-group select:focus {
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