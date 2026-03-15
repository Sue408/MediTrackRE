<template>
    <div class="drug-add-modal">
        <!-- 左侧蓝色导航区 -->
        <div class="nav-sidebar">
            <div class="nav-header">
                <h2 class="nav-title">添加药品</h2>
            </div>

            <!-- 步骤指示器 -->
            <div class="steps-container">
                <div
                    v-for="(step, index) in steps"
                    :key="step.id"
                    class="step-item"
                    :class="{
                        'step-active': currentStep === index,
                        'step-completed': currentStep > index
                    }"
                >
                    <div class="step-indicator">
                        <div class="step-circle">
                            <span v-if="currentStep > index" class="check-icon">✓</span>
                            <span v-else>{{ index + 1 }}</span>
                        </div>
                        <div class="step-line" v-if="index < steps.length - 1"></div>
                    </div>
                    <div class="step-content">
                        <span class="step-title">{{ step.title }}</span>
                        <span class="step-desc">{{ step.desc }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 右侧白色编辑区 -->
        <div class="content-area">
            <div class="close-icon" @click="handleClose">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M15 5L5 15M5 5L15 15" stroke="#666666" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
            </div>

            <Transition name="slide-fade" mode="out-in">
                <!-- 搜索视图 -->
                <div v-if="currentStep === 0" key="search" class="view-panel search-view">
                    <div class="search-header">
                        <h3 class="view-title">搜索药品</h3>
                        <p class="view-desc">输入药品关键词从数据库搜索，或手动添加</p>
                    </div>

                    <!-- 搜索输入 -->
                    <div class="search-input-wrapper">
                        <input
                            v-model="searchKeyword"
                            type="text"
                            class="search-input"
                            placeholder="输入药品名称进行搜索..."
                            @keyup.enter="handleSearch"
                        />
                        <button class="search-btn" @click="handleSearch">
                            <span class="search-icon">
                                <svg class="search-icon" width="28" height="28" viewBox="0 0 24 24" fill="none">
                                    <path d="M15.5 14H14.71L14.43 13.73C15.41 12.59 16 11.11 16 9.5C16 5.91 13.09 3 9.5 3C5.91 3 3 5.91 3 9.5C3 13.09 5.91 16 9.5 16C11.11 16 12.59 15.41 13.73 14.43L14 14.71V15.5L19 20.49L20.49 19L15.5 14ZM9.5 14C7.01 14 5 11.99 5 9.5C5 7.01 7.01 5 9.5 5C11.99 5 14 7.01 14 9.5C14 11.99 11.99 14 9.5 14Z" fill="currentColor"/>
                                </svg>
                            </span>
                        </button>
                    </div>

                    <!-- 搜索结果列表 -->
                    <div class="search-results" v-if="searchResults.length > 0">
                        <div class="results-header">
                            <span>搜索结果 ({{ searchResults.length }})</span>
                        </div>
                        <div class="results-list">
                            <div
                                v-for="item in searchResults"
                                :key="item.id"
                                class="result-item"
                                @click="handleSelectExternal(item)"
                            >
                                <div class="result-image">
                                    <img v-if="item.image" :src="item.image" alt="" />
                                    <span v-else class="result-placeholder">
                                        <svg  xmlns="http://www.w3.org/2000/svg" width="32" height="32"  
                                            fill="currentColor" viewBox="0 0 24 24" >
                                            <!--Boxicons v3.0.8 https://boxicons.com | License  https://docs.boxicons.com/free-->
                                            <path d="M18 6h-1V4c0-1.1-.9-2-2-2H9c-1.1 0-2 .9-2 2v2H6c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2M9 4h6v2H9zM6 20V8h12v12z"></path><path d="M13 10h-2v3H8v2h3v3h2v-3h3v-2h-3z"></path>
                                        </svg>
                                    </span>
                                </div>
                                <div class="result-info">
                                    <span class="result-name">{{ item.name }}</span>
                                    <span class="result-detail">{{ item.usage_method }} | {{ item.dosage }}</span>
                                </div>
                                <span class="result-add">+</span>
                            </div>
                        </div>
                    </div>

                    <!-- 空状态 / 手动添加 -->
                    <div class="manual-add-section">
                        <div class="divider">
                            <span class="divider-text">或者</span>
                        </div>
                        <button class="manual-add-btn" @click="handleManualAdd">
                            <span class="manual-icon">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                                    <path d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z" fill="currentColor"/>
                                </svg>
                            </span>
                            <span>手动添加药品</span>
                        </button>
                    </div>
                </div>

                <!-- 编辑视图 -->
                <div v-else-if="currentStep === 1" key="edit" class="view-panel">
                    <div class="edit-header">
                        <h3 class="view-title">{{ isExternalDrug ? '编辑药品信息' : '添加药品' }}</h3>
                        <p class="view-desc">{{ isExternalDrug ? '查看药品详情并设置余量' : '填写药品详细信息' }}</p>
                    </div>

                    <div class="edit-view">
                        <DrugEditPanel
                        :drug="currentDrug"
                        @confirm="handleConfirm"
                        @cancel="handleBack"
                        />
                    </div>
                    
                </div>
            </Transition>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue'
    import { searchExternalDrugs, createDrug } from '@/api/drug'
    import DrugEditPanel from './DrugEditPanel.vue'
    import type { Drug, CreateDrugRequest } from '@/types/drugTypes'

    const emit = defineEmits<{
        (e: 'close'): void
        (e: 'success'): void
    }>()

    // 步骤配置
    const steps = [
        { id: 'search', title: '搜索药品', desc: '从数据库搜索或手动添加' },
        { id: 'edit', title: '编辑信息', desc: '设置余量完成添加' }
    ]

    // 当前步骤
    const currentStep = ref(0)

    // 搜索关键词
    const searchKeyword = ref('')

    // 搜索结果
    const searchResults = ref<Drug[]>([])

    // 当前编辑的药品数据
    const currentDrug = ref<Drug|null>(null)

    // 是否来自权威数据库
    const isExternalDrug = ref(false)

    // 搜索药品
    const handleSearch = async () => {
        if (!searchKeyword.value.trim()) {
            searchResults.value = []
            return
        }

        try {
            const results = await searchExternalDrugs(searchKeyword.value)
            searchResults.value = results
        } catch (error) {
            console.error('搜索失败:', error)
        }
    }

    // 选择外部药品
    const handleSelectExternal = (item: Drug) => {
        currentDrug.value = item
        currentStep.value = 1
    }

    // 手动添加
    const handleManualAdd = () => {
        currentDrug.value = {
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
        currentStep.value = 1
    }

    // 返回上一步
    const handleBack = () => {
        currentStep.value = 0
        currentDrug.value = null
        isExternalDrug.value = false
    }

    // 确认创建药品
    const handleConfirm = async (data: Drug) => {
        try {
            const drugData: CreateDrugRequest = {
                name: data.name,
                image: data.image || undefined,
                usage_method: data.usage_method,
                dosage: data.dosage,
                remaining: data.remaining || undefined,
                source: data.source,
                external_id: data.external_id ?? undefined
            }

            await createDrug(drugData)
            emit('success')
            handleClose()
        } catch (error: any) {
            console.error('创建药品失败:', error)
            const message = error.response?.data?.detail || '创建药品失败，请重试'
            alert(message)
        }
    }

    // 关闭弹窗
    const handleClose = () => {
        // 重置状态
        currentStep.value = 0
        searchKeyword.value = ''
        searchResults.value = []
        currentDrug.value = null
        isExternalDrug.value = false
        emit('close')
    }
</script>

<style scoped>
.drug-add-modal {
    display: flex;
    width: 100%;
    height: 100%;
    border-radius: 24px;
    overflow: hidden;
    background: #fff;
}

/* 左侧蓝色导航区 */
.nav-sidebar {
    width: 240px;
    background: linear-gradient(180deg, #7494ec 0%, #5a7de0 100%);
    display: flex;
    flex-direction: column;
    padding: 30px 20px;
    flex-shrink: 0;
}

.nav-header {
    margin-bottom: 40px;
}

.nav-title {
    color: #ffffff;
    font-size: 22px;
    font-weight: 600;
    margin: 0;
}

/* 步骤指示器 */
.steps-container {
    display: flex;
    flex-direction: column;
    gap: 0;
}

.step-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    position: relative;
}

.step-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.step-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    color: rgba(255, 255, 255, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.step-active .step-circle {
    background: #ffffff;
    color: #7494ec;
    transform: scale(1.15);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.step-completed .step-circle {
    background: #ffffff;
    color: #7494ec;
}

.check-icon {
    font-size: 16px;
}

.step-line {
    width: 2px;
    height: 40px;
    background: rgba(255, 255, 255, 0.3);
    transition: background 0.5s ease;
}

.step-completed .step-line {
    background: #ffffff;
}

.step-content {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding-top: 6px;
    transition: all 0.3s ease;
}

.step-title {
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.step-active .step-title {
    color: #ffffff;
    font-weight: 600;
}

.step-completed .step-title {
    color: #ffffff;
}

.step-desc {
    color: rgba(255, 255, 255, 0.5);
    font-size: 12px;
    line-height: 1.4;
}

.step-active .step-desc {
    color: rgba(255, 255, 255, 0.8);
}

/* 右侧白色编辑区 */
.content-area {
    flex: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 30px;
    overflow: hidden;
}

.view-panel {
    flex: 1;
    display: flex;
    height: 100%;
    flex-direction: column;
}

.search-header,
.edit-header {
    margin-bottom: 24px;
    height: 10%;
}

.view-title {
    font-size: 20px;
    color: #333333;
    font-weight: 600;
    margin: 0 0 8px 0;
}

.view-desc {
    font-size: 14px;
    color: #999999;
    margin: 0;
}

/* 搜索视图 */
.search-input-wrapper {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    padding-right: 5px;
}

.search-input {
    flex: 1;
    padding: 14px 18px;
    border: 2px solid #e2e2e2;
    border-radius: 12px;
    font-size: 15px;
    color: #333333;
    transition: all 0.3s ease;
}

.search-input:focus {
    outline: none;
    border-color: #7494ec;
    box-shadow: 0 0 0 4px rgba(116, 148, 236, 0.15);
}

.search-btn {
    width: 50px;
    height: 50px;
    border: none;
    border-radius: 12px;
    background: #7494ec;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.search-btn:hover {
    background: #5a7de0;
    transform: scale(1.05);
}

.search-icon {
    color: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 搜索结果 */
.search-results {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
    margin-bottom: 20px;
}

.results-header {
    font-size: 14px;
    color: #999999;
    margin-bottom: 12px;
}

.results-list {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.results-list::-webkit-scrollbar {
    width: 3px;
}

.results-list::-webkit-scrollbar-button {
    background: transparent;
}

.results-list::-webkit-scrollbar-thumb {
    background-color: #ccc;
    border-radius: 5px;
}

.result-item {
    display: flex;
    align-items: center;
    width: 95%;
    gap: 14px;
    padding: 12px;
    border-radius: 12px;
    background: #f8f9fc;
    cursor: pointer;
    transition: all 0.3s ease;
}

.result-item:hover {
    background: #eef0f8;
    transform: translateX(6px);
    box-shadow: 0 4px 12px rgba(116, 148, 236, 0.15);
}

.result-image {
    width: 48px;
    height: 48px;
    border-radius: 10px;
    overflow: hidden;
    background: linear-gradient(135deg, #f0f4ff 0%, #e8f0ff 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.result-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.result-placeholder {
    color: #7494ec;
    display: flex;
    align-items: center;
    justify-content: center;
}

.result-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 0;
}

.result-name {
    font-size: 15px;
    color: #333333;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.result-detail {
    font-size: 12px;
    color: #999999;
}

.result-add {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #7494ec;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 600;
    opacity: 0;
    transform: scale(0.5);
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.result-item:hover .result-add {
    opacity: 1;
    transform: scale(1);
}

/* 手动添加 */
.manual-add-section {
    margin-top: auto;
    padding-top: 20px;
}

.divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
}

.divider::before,
.divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #e2e2e2;
}

.divider-text {
    font-size: 13px;
    color: #999999;
}

.manual-add-btn {
    width: 100%;
    padding: 14px;
    border: 2px dashed #c9d6ff;
    border-radius: 12px;
    background: transparent;
    color: #7494ec;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all 0.3s ease;
}

.manual-add-btn:hover {
    background: rgba(116, 148, 236, 0.08);
    border-color: #7494ec;
    transform: translateY(-2px);
}

.manual-icon {
    display: flex;
    align-items: center;
}

/* 关闭图标样式 */
.close-icon {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    z-index: 10;
}

.close-icon:hover {
    background: #f5f5f5;
    transform: rotate(90deg);
}

.close-icon:active {
    transform: rotate(90deg) scale(0.95);
}

/* 过渡动画 */
.slide-fade-enter-active {
    transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    transition-delay: 0.1s;
}

.slide-fade-leave-active {
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.slide-fade-enter-from {
    opacity: 0;
    transform: translateX(30px);
}

.slide-fade-leave-to {
    opacity: 0;
    transform: translateX(-20px);
}

/* 响应式 */
@media screen and (max-width: 650px) {
    .drug-add-modal {
        flex-direction: column;
    }

    .nav-sidebar {
        width: 100%;
        flex-direction: row;
        padding: 16px 20px;
        align-items: center;
    }

    .nav-header {
        margin-bottom: 0;
        margin-right: 20px;
    }

    .steps-container {
        flex-direction: row;
        gap: 20px;
    }

    .step-item {
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }

    .step-indicator {
        flex-direction: row;
        gap: 0;
    }

    .step-line {
        width: 30px;
        height: 2px;
    }

    .step-content {
        align-items: center;
        padding-top: 0;
    }

    .step-desc {
        display: none;
    }

    /* 移动端调整关闭按钮 */
    .close-icon {
        top: 10px;
        right: 10px;
        width: 32px;
        height: 32px;
    }
}

.edit-view {
    height: 90%;
}
</style>