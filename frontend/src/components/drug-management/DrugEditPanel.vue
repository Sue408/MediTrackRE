<template>
    <div class="drug-edit-panel">
        <!-- 药品图片 -->
        <div class="drug-image-section">
            <div class="drug-image-wrapper">
                <img
                    v-if="localDrug.image"
                    :src="localDrug.image"
                    alt="药品图片"
                    class="drug-image"
                />
                <div v-else class="drug-image-placeholder">
                    <span class="placeholder-icon">
                        <svg  xmlns="http://www.w3.org/2000/svg" width="64" height="64"  
                            fill="currentColor" viewBox="0 0 24 24" >
                            <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                            <path d="M18 6h-1V4c0-1.1-.9-2-2-2H9c-1.1 0-2 .9-2 2v2H6c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2M9 4h6v2H9zM6 20V8h12v12z"></path><path d="M13 10h-2v3H8v2h3v3h2v-3h3v-2h-3z"></path>
                        </svg>
                    </span>
                </div>
            </div>
        </div>

        <!-- 药品信息表单 -->
        <div class="drug-info-section">
            <!-- 药品名称 -->
            <div class="form-item">
                <label class="form-label">药品名称</label>
                <input
                    v-model="localDrug.name"
                    type="text"
                    class="form-input"
                    :disabled="!isEditable"
                    placeholder="请输入药品名称"
                />
            </div>

            <!-- 用法 -->
            <div class="form-item">
                <label class="form-label">用法</label>
                <!-- <select
                    v-model="localDrug.usage_method"
                    class="form-select"
                    :disabled="!isEditable"
                >
                    <option value="口服">口服</option>
                    <option value="注射">注射</option>
                    <option value="外用">外用</option>
                    <option value="含服">含服</option>
                    <option value="吸入">吸入</option>
                    <option value="滴入">滴入</option>
                    <option value="其他">其他</option>
                </select> -->
                <FlowSelect
                :options="[
                    {value: '口服', label: '口服'},
                    {value: '注射', label: '注射'},
                    {value: '外用', label: '外用'},
                    {value: '含服', label: '含服'},
                    {value: '吸入', label: '吸入'},
                    {value: '滴入', label: '滴入'},
                    {value: '其他', label: '其他'}
                ]",
                v-model="localDrug.usage_method"
                :disabled="!isEditable"
                />
            </div>

            <!-- 用量 -->
            <div class="form-item">
                <label class="form-label">用量</label>
                <input
                    v-model="localDrug.dosage"
                    type="text"
                    class="form-input"
                    :disabled="!isEditable"
                    placeholder="如: 每次1片,每日3次"
                />
            </div>

            <!-- 余量（始终可编辑） -->
            <div class="form-item">
                <label class="form-label">余量</label>
                <input
                    v-model="localDrug.remaining"
                    type="text"
                    class="form-input"
                    placeholder="如:30片"
                />
            </div>

            <!-- 来源标识 -->
            <div class="source-tag" v-if="localDrug.source">
                <span class="tag-text">
                    {{ localDrug.source === '医疗数据库' ? '来自：医疗数据库' : '来自：手动输入' }}
                </span>
            </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
            <button class="btn btn-cancel" @click="handleCancel">取消</button>
            <button class="btn btn-confirm" @click="handleConfirm">保存</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Drug } from '@/types/drugTypes'
import FlowSelect from '@/components/common/FlowSelect.vue'

const props = defineProps<{
    drug?: Drug | null
}>()

const emit = defineEmits<{
    (e: 'confirm', data: Drug): void
    (e: 'cancel'): void
}>()

// 本地药物数据
const localDrug = ref<Drug>(
    {
        id: 0,
        user_id: 0,
        name: '',
        image: null,
        usage_method: '口服',
        dosage: '',
        remaining: null,
        source: '手动输入',
        external_id: null,
        created_at: '',
        updated_at: '',  
    }
)

// 是否可编辑（权威数据库来源不可编辑基本信息）
const isEditable = computed(() => {
    if (props.drug?.source === '医疗数据库') {
        return false  // 来自权威数据库，只能修改余量
    }
    return true  // 手动输入可以编辑所有
})

// 监听外部药物数据变化
watch(() => props.drug, (newDrug) => {
    if (newDrug) {
        localDrug.value = { ...newDrug }
    } else {
        // 重置为默认状态
        localDrug.value = {
            id: 0,
            user_id: 0,
            name: '',
            image: null,
            usage_method: '口服',
            dosage: '',
            remaining: null,
            source: '手动输入',
            external_id: null,
            created_at: '',
            updated_at: '',  
    }
    }
}, { immediate: true })

// 取消
const handleCancel = () => {
    emit('cancel')
}

// 确认保存
const handleConfirm = () => {
    // 验证必填字段
    if (!localDrug.value.name?.trim()) {
        alert('请输入药品名称')
        return
    }
    if (!localDrug.value.dosage?.trim()) {
        alert('请输入用量')
        return
    }
    emit('confirm', { ...localDrug.value })
}
</script>

<style scoped>
.drug-edit-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 10px;
    gap: 15px;
}

.drug-image-section {
    display: flex;
    justify-content: center;
    padding: 10px 0;
}

.drug-image-wrapper {
    width: 120px;
    height: 120px;
    border-radius: 16px;
    overflow: hidden;
    background: linear-gradient(135deg, #f0f4ff 0%, #e8f0ff 100%);
    display: flex;
    align-items: center;
    justify-content: center;
}

.drug-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.drug-image-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.placeholder-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    color: #7494ec;
}

.drug-info-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 0 15px;
    overflow-y: auto;
}

.drug-info-section::-webkit-scrollbar {
    width: 3px;
}

.drug-info-section::-webkit-scrollbar-thumb {
    background-color: #ccc;
    border-radius: 5px;
}


.form-item {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.form-label {
    font-size: 14px;
    color: #333333;
    font-weight: 500;
}

.form-input,
.form-select {
    padding: 10px 14px;
    border: 1px solid #e2e2e2;
    border-radius: 8px;
    font-size: 14px;
    color: #333333;
    background: #ffffff;
    transition: all 0.3s ease;
}

.form-input:focus,
.form-select:focus {
    outline: none;
    border-color: #7494ec;
    box-shadow: 0 0 0 3px rgba(116, 148, 236, 0.2);
}

.form-input:disabled,
.form-select:disabled {
    background: #f5f5f5;
    color: #999999;
    cursor: not-allowed;
}

.source-tag {
    margin-top: 8px;
}

.tag-text {
    display: inline-block;
    padding: 4px 12px;
    background: linear-gradient(135deg, #e2e2e2, #c9d6ff);
    border-radius: 20px;
    font-size: 12px;
    color: #666666;
}

.action-buttons {
    display: flex;
    gap: 12px;
    padding-top: 10px;
}

.btn {
    flex: 1;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-cancel {
    background: #f5f5f5;
    color: #666666;
}

.btn-cancel:hover {
    background: #e2e2e2;
}

.btn-confirm {
    background: #7494ec;
    color: #ffffff;
}

.btn-confirm:hover {
    background: #5a7de0;
}
</style>