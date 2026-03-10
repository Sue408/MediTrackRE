<template>
    <div class="health-records-container">
        <!-- 标题区域 -->
        <div class="header-section">
            <h3>健康档案</h3>
            <p>管理您的健康信息，帮助我们更好地为您服务</p>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <span>加载中...</span>
        </div>

        <!-- 内容区域 -->
        <div v-else class="content-section">
            <!-- 基本信息卡片 -->
            <transition name="fade-slide" mode="out-in">
                <div class="card basic-info" :key="'basic'">
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
                                <select v-else v-model="editData.gender" class="edit-select">
                                    <option value="unknown">保密</option>
                                    <option value="男">男</option>
                                    <option value="女">女</option>
                                </select>
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
                                <select v-else v-model="editData.blood_type" class="edit-select">
                                    <option value="unknown">未知</option>
                                    <option value="A">A型</option>
                                    <option value="B">B型</option>
                                    <option value="AB">AB型</option>
                                    <option value="O">O型</option>
                                </select>
                            </div>
                        </div>

                        <!-- 女性特殊状态 -->
                        <div class="special-status" v-if="profile.gender === '女' || (isEditing && editData.gender === '女')">
                            <span class="label">特殊状态</span>
                            <div class="value" v-if="!isEditing">
                                {{ profile.special_status || '无' }}
                            </div>
                            <select v-else v-model="editData.special_status" class="edit-select">
                                <option :value="null">无</option>
                                <option value="备孕">备孕</option>
                                <option value="怀孕">怀孕</option>
                                <option value="哺乳">哺乳</option>
                            </select>
                        </div>
                    </div>
                </div>
            </transition>

            <!-- 过敏史卡片 -->
            <transition name="fade-slide" mode="out-in">
                <div class="card allergies" :key="'allergies'">
                    <div class="card-header">
                        <h4>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM15.5 11C16.33 11 17 10.33 17 9.5C17 8.67 16.33 8 15.5 8C14.67 8 14 8.67 14 9.5C14 10.33 14.67 11 15.5 11ZM8.5 11C9.33 11 10 10.33 10 9.5C10 8.67 9.33 8 8.5 8C7.67 8 7 8.67 7 9.5C7 10.33 7.67 11 8.5 11ZM12 17.5C14.33 17.5 16.31 16.04 17.11 14H6.89C7.69 16.04 9.67 17.5 12 17.5Z" fill="#ff6b6b"/>
                            </svg>
                            过敏史
                        </h4>
                        <button class="add-btn" @click="showAddAllergy = true">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                                <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
                            </svg>
                            添加
                        </button>
                    </div>

                    <div class="card-body">
                        <div v-if="profile.allergies && profile.allergies.length > 0" class="tag-list">
                            <div v-for="(allergy, index) in profile.allergies" :key="index" class="tag-item">
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
                </div>
            </transition>

            <!-- 疾病史卡片 -->
            <transition name="fade-slide" mode="out-in">
                <div class="card diseases" :key="'diseases'">
                    <div class="card-header">
                        <h4>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                                <path d="M19 3H5C3.89 3 3 4.57 3 6V20C3 21.1 3.89 22 5 22H19C20.1 22 21 21.1 21 20V6C21 4.57 20.1 3 19 3ZM19 19H5V9H19V19ZM7 11H12V13H7V11ZM7 15H17V17H7V15Z" fill="#ff9800"/>
                            </svg>
                            疾病史
                        </h4>
                        <button class="add-btn" @click="showAddDisease = true">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                                <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
                            </svg>
                            添加
                        </button>
                    </div>

                    <div class="card-body">
                        <div v-if="profile.diseases && profile.diseases.length > 0" class="disease-list">
                            <div v-for="(disease, index) in profile.diseases" :key="index" class="disease-item">
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
                </div>
            </transition>
        </div>

        <!-- 添加过敏史弹窗 -->
        <div class="modal-overlay" v-if="showAddAllergy" @click.self="showAddAllergy = false">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>添加过敏史</h3>
                    <button class="close-btn" @click="showAddAllergy = false">
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
                    <button class="cancel-btn" @click="showAddAllergy = false">取消</button>
                    <button class="confirm-btn" @click="addAllergy">添加</button>
                </div>
            </div>
        </div>

        <!-- 添加疾病史弹窗 -->
        <div class="modal-overlay" v-if="showAddDisease" @click.self="showAddDisease = false">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>添加疾病史</h3>
                    <button class="close-btn" @click="showAddDisease = false">
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
                        <select v-model="newDisease.status">
                            <option value="治疗中">治疗中</option>
                            <option value="已控制">已控制</option>
                            <option value="已痊愈">已痊愈</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-btn" @click="showAddDisease = false">取消</button>
                    <button class="confirm-btn" @click="addDisease">添加</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, onMounted } from 'vue'
    import { getProfile, updateProfile } from '@/api/user'
    import type { ProfileResponse, Gender, BloodType, SpecialStatus, AllergyItem, DiseaseItem, UpdateProfileRequest } from '@/types/userTypes'

    // 加载状态
    const loading = ref(true)
    const saving = ref(false)
    const isEditing = ref(false)

    // 档案数据
    const profile = reactive<ProfileResponse>({
        id: 0,
        user_id: 0,
        gender: 'unknown',
        height: null,
        weight: null,
        blood_type: 'unknown',
        allergies: [],
        diseases: [],
        special_status: null,
        created_at: '',
        updated_at: ''
    })

    // 编辑数据
    const editData = reactive({
        gender: 'unknown' as Gender,
        height: null as number | null,
        weight: null as number | null,
        blood_type: 'unknown' as BloodType,
        special_status: null as SpecialStatus
    })

    // 弹窗状态
    const showAddAllergy = ref(false)
    const showAddDisease = ref(false)

    // 新增过敏史
    const newAllergy = reactive({
        name: '',
        reaction: ''
    })

    // 新增疾病史
    const newDisease = reactive({
        name: '',
        diagnosed_at: '',
        status: '治疗中'
    })

    // 加载档案
    const loadProfile = async () => {
        loading.value = true
        try {
            const data = await getProfile()
            Object.assign(profile, data)
        } catch (error) {
            console.error('加载健康档案失败:', error)
        } finally {
            loading.value = false
        }
    }

    // 开始编辑
    const startEdit = () => {
        editData.gender = profile.gender
        editData.height = profile.height
        editData.weight = profile.weight
        editData.blood_type = profile.blood_type
        editData.special_status = profile.special_status
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
            const res = await updateProfile(data)
            Object.assign(profile, res)
            isEditing.value = false
        } catch (error) {
            console.error('保存健康档案失败:', error)
        } finally {
            saving.value = false
        }
    }

    // 添加过敏史
    const addAllergy = async () => {
        if (!newAllergy.name || !newAllergy.reaction) {
            alert('请填写完整信息')
            return
        }

        const allergies: AllergyItem[] = [...profile.allergies, { ...newAllergy }]
        try {
            const res = await updateProfile({ allergies })
            profile.allergies = res.allergies
            showAddAllergy.value = false
            newAllergy.name = ''
            newAllergy.reaction = ''
        } catch (error) {
            console.error('添加过敏史失败:', error)
        }
    }

    // 删除过敏史
    const removeAllergy = async (index: number) => {
        const allergies = profile.allergies.filter((_, i) => i !== index)
        try {
            const res = await updateProfile({ allergies })
            profile.allergies = res.allergies
        } catch (error) {
            console.error('删除过敏史失败:', error)
        }
    }

    // 添加疾病史
    const addDisease = async () => {
        if (!newDisease.name || !newDisease.diagnosed_at) {
            alert('请填写完整信息')
            return
        }

        const diseases: DiseaseItem[] = [...profile.diseases, { ...newDisease }]
        try {
            const res = await updateProfile({ diseases })
            profile.diseases = res.diseases
            showAddDisease.value = false
            newDisease.name = ''
            newDisease.diagnosed_at = ''
            newDisease.status = '治疗中'
        } catch (error) {
            console.error('添加疾病史失败:', error)
        }
    }

    // 删除疾病史
    const removeDisease = async (index: number) => {
        const diseases = profile.diseases.filter((_, i) => i !== index)
        try {
            const res = await updateProfile({ diseases })
            profile.diseases = res.diseases
        } catch (error) {
            console.error('删除疾病史失败:', error)
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

    // 格式化日期
    const formatDate = (dateStr: string) => {
        if (!dateStr) return '-'
        const date = new Date(dateStr)
        return date.toLocaleDateString('zh-CN')
    }

    onMounted(() => {
        loadProfile()
    })
</script>

<style scoped>
    .health-records-container {
        height: 100%;
        width: 100%;
        overflow-y: auto;
        padding: 20px;
    }

    .header-section {
        margin-bottom: 25px;
    }

    .header-section h3 {
        margin: 0 0 8px 0;
        color: #333;
        font-size: 20px;
    }

    .header-section p {
        margin: 0;
        color: #999;
        font-size: 14px;
    }

    .loading-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px;
        color: #999;
    }

    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top-color: #7494ec;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 15px;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .content-section {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .card {
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

    .edit-input,
    .edit-select {
        padding: 10px 15px;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        font-size: 14px;
        outline: none;
        transition: border-color 0.3s ease;
    }

    .edit-input:focus,
    .edit-select:focus {
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

    /* 动画 */
    .fade-slide-enter-active,
    .fade-slide-leave-active {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .fade-slide-enter-from {
        opacity: 0;
        transform: translateY(20px);
    }

    .fade-slide-leave-to {
        opacity: 0;
        transform: translateY(-20px);
    }

    @media (max-width: 650px) {
        .info-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
