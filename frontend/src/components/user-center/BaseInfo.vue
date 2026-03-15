<template>
    <div class="base-info-container">
        <div class="card-header">
            <h4>基本信息</h4>
            <button v-if="!isEditing" class="edit-btn" @click="startEdit">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z" fill="currentColor"/>
                </svg>
                编辑
            </button>
            <div v-else class="edit-actions">
                <button class="cancel-btn" @click="cancelEdit">取消</button>
                <button class="save-btn" @click="saveProfile" :disabled="saving">
                    {{ saving ? '保存中...' : '保存' }}
                </button>
            </div>
        </div>

        <div class="card-body">
            <div class="info-grid">
                <!-- 性别 -->
                <div class="info-item">
                    <span class="label">性别</span>
                    <div class="value" v-if="!isEditing">
                        {{ getGenderText(profile.gender) }}
                    </div>
                    <FlowSelect
                        v-else
                        v-model="editData.gender"
                        :options="genderOptions"
                        placeholder="请选择性别"
                    />
                </div>

                <!-- 身高 -->
                <div class="info-item">
                    <span class="label">身高</span>
                    <div class="value" v-if="!isEditing">
                        {{ profile.height ? profile.height + ' cm' : '未设置' }}
                    </div>
                    <input v-else type="number" v-model.number="editData.height" placeholder="cm" class="edit-input" min="50" max="250">
                </div>

                <!-- 体重 -->
                <div class="info-item">
                    <span class="label">体重</span>
                    <div class="value" v-if="!isEditing">
                        {{ profile.weight ? profile.weight + ' kg' : '未设置' }}
                    </div>
                    <input v-else type="number" v-model.number="editData.weight" placeholder="kg" class="edit-input" min="20" max="300">
                </div>

                <!-- 血型 -->
                <div class="info-item">
                    <span class="label">血型</span>
                    <div class="value" v-if="!isEditing">
                        {{ getBloodTypeText(profile.blood_type) }}
                    </div>
                    <FlowSelect
                        v-else
                        v-model="editData.blood_type"
                        :options="bloodTypeOptions"
                        placeholder="请选择血型"
                    />
                </div>
            </div>

            <!-- 女性特殊状态 -->
            <div class="special-status" v-if="profile.gender === '女' || (isEditing && editData.gender === '女')">
                <span class="label">特殊状态</span>
                <div class="value" v-if="!isEditing">
                    {{ profile.special_status || '无' }}
                </div>
                <FlowSelect
                    v-else
                    v-model="editData.special_status"
                    :options="specialStatusOptions"
                    placeholder="请选择特殊状态"
                />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive } from 'vue'
    import { updateProfile } from '@/api/user'
    import type { Gender, BloodType, SpecialStatus, UpdateProfileRequest } from '@/types/userTypes'
    import FlowSelect from '@/components/common/FlowSelect.vue'

    // 接收父组件传递的数据
    const props = defineProps<{
        profile: {
            gender: Gender
            height: number | null
            weight: number | null
            blood_type: BloodType
            special_status: SpecialStatus
        }
    }>()

    const emit = defineEmits<{
        'refresh': []
    }>()

    // 加载状态
    const saving = ref(false)
    const isEditing = ref(false)

    // 编辑数据
    const editData = reactive({
        gender: 'unknown' as Gender,
        height: null as number | null,
        weight: null as number | null,
        blood_type: 'unknown' as BloodType,
        special_status: null as SpecialStatus
    })

    // 性别选项
    const genderOptions = [
        { value: 'unknown', label: '保密' },
        { value: '男', label: '男' },
        { value: '女', label: '女' }
    ]

    // 血型选项
    const bloodTypeOptions = [
        { value: 'unknown', label: '未知' },
        { value: 'A', label: 'A型' },
        { value: 'B', label: 'B型' },
        { value: 'AB', label: 'AB型' },
        { value: 'O', label: 'O型' }
    ]

    // 特殊状态选项
    const specialStatusOptions = [
        { value: null, label: '无' },
        { value: '备孕', label: '备孕' },
        { value: '怀孕', label: '怀孕' },
        { value: '哺乳', label: '哺乳' }
    ]

    // 开始编辑
    const startEdit = () => {
        editData.gender = props.profile.gender
        editData.height = props.profile.height
        editData.weight = props.profile.weight
        editData.blood_type = props.profile.blood_type
        editData.special_status = props.profile.special_status
        isEditing.value = true
    }

    // 取消编辑
    const cancelEdit = () => {
        isEditing.value = false
    }

    // 保存档案
    const saveProfile = async () => {
        saving.value = true
        try {
            const data: UpdateProfileRequest = {
                gender: editData.gender,
                height: editData.height,
                weight: editData.weight,
                blood_type: editData.blood_type,
                special_status: editData.special_status
            }
            await updateProfile(data)
            isEditing.value = false
            emit('refresh')
        } catch (error) {
            console.error('保存健康档案失败:', error)
        } finally {
            saving.value = false
        }
    }

    // 格式化性别文本
    const getGenderText = (gender: Gender) => {
        const map: Record<Gender, string> = {
            '男': '男',
            '女': '女',
            'unknown': '保密'
        }
        return map[gender] || '保密'
    }

    // 格式化血型文本
    const getBloodTypeText = (bloodType: BloodType) => {
        const map: Record<BloodType, string> = {
            'A': 'A型',
            'B': 'B型',
            'AB': 'AB型',
            'O': 'O型',
            'unknown': '未知'
        }
        return map[bloodType] || '未知'
    }
</script>

<style scoped>
    .base-info-container {
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
        color: #333;
        font-size: 16px;
    }

    .edit-btn {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border: none;
        border-radius: 15px;
        background: #f5f5f5;
        color: #666;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .edit-btn:hover {
        background: #e8e8e8;
    }

    .edit-actions {
        display: flex;
        gap: 10px;
    }

    .edit-actions .cancel-btn,
    .edit-actions .save-btn {
        padding: 8px 16px;
        border: none;
        border-radius: 15px;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .edit-actions .cancel-btn {
        background: #f5f5f5;
        color: #666;
    }

    .edit-actions .save-btn {
        background: #7494ec;
        color: #fff;
    }

    .edit-actions .save-btn:disabled {
        opacity: 0.6;
    }

    .card-body {
        padding: 20px;
    }

    .info-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }

    .info-item {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .info-item .label {
        color: #999;
        font-size: 13px;
    }

    .info-item .value {
        color: #333;
        font-size: 15px;
        font-weight: 500;
    }

    .edit-input {
        padding: 10px 15px;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        font-size: 14px;
        outline: none;
        transition: border-color 0.3s ease;
    }

    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    .edit-input:focus {
        border-color: #7494ec;
    }

    .special-status {
        margin-top: 20px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .special-status .label {
        color: #999;
        font-size: 13px;
    }

    .special-status .value {
        color: #ff9800;
        font-size: 15px;
        font-weight: 500;
    }

    @media (max-width: 650px) {
        .info-grid {
            grid-template-columns: 1fr;
        }
    }
</style>