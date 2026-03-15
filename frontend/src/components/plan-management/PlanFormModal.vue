<template>
    <div class="plan-form-modal">
        <!-- 左侧蓝色导航区 -->
        <div class="nav-sidebar">
            <div class="nav-header">
                <h2 class="nav-title">{{ editingPlan ? '编辑计划' : '添加计划' }}</h2>
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
                <!-- 基本信息步骤 -->
                <div v-if="currentStep === 0" key="basic" class="view-panel">
                    <div class="view-header">
                        <h3 class="view-title">基本信息</h3>
                        <p class="view-desc">填写计划名称和类型</p>
                    </div>

                    <div class="form-content">
                        <div class="form-group">
                            <label>计划名称 *</label>
                            <input
                                type="text"
                                v-model="formData.name"
                                placeholder="如: 每日降压药"
                                class="form-input"
                            >
                        </div>

                        <div class="form-group">
                            <label>计划类型 *</label>
                            <FlowSelect 
                            :options="[
                                {value: '长期', label: '长期计划'},
                                {value: '周期', label: '周期计划'}
                            ]",
                            v-model="formData.plan_type"
                            />
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label>开始日期 *</label>
                                <input
                                    type="date"
                                    v-model="formData.start_date"
                                    class="form-input"
                                >
                            </div>
                            <div class="form-group" v-if="formData.plan_type === '周期'">
                                <label>结束日期</label>
                                <input
                                    type="date"
                                    v-model="formData.end_date"
                                    class="form-input"
                                >
                            </div>
                        </div>

                        <div class="form-group">
                            <div class="checkbox-label">
                                <input type="checkbox" v-model="formData.sms_enabled">
                                启用短信提醒
                            </div>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button class="btn-cancel" @click="handleClose">取消</button>
                        <button class="btn-next" @click="nextStep">下一步</button>
                    </div>
                </div>

                <!-- 频率设置步骤 -->
                <div v-else-if="currentStep === 1" key="frequency" class="view-panel">
                    <div class="view-header">
                        <h3 class="view-title">频率设置</h3>
                        <p class="view-desc">设置用药频率和时间</p>
                    </div>

                    <div class="form-content">
                        <div class="form-group">
                            <label>用药频率 *</label>
                            <FlowSelect 
                            :options="[
                                {value: 'daily', label: '每天'},
                                {value: 'alternate', label: '间隔'},
                                {value: 'weekly', label: '每周'},
                                {value: 'monthly', label: '每月'}
                            ]",
                            v-model="formData.frequency_type"
                            @change="handleFrequencyChange"
                            />
                        </div>

                        <!-- 间隔天设置 -->
                        <div class="form-group" v-if="formData.frequency_type === 'alternate'">
                            <label>间隔天数</label>
                            <input
                                type="number"
                                v-model="formData.frequency_detail.interval_days"
                                min="1"
                                placeholder="如: 2"
                                class="form-input"
                            >
                        </div>

                        <!-- 每周设置 -->
                        <div class="form-group" v-if="formData.frequency_type === 'weekly'">
                            <label>选择星期</label>
                            <div class="weekday-selector">
                                <label
                                    v-for="day in weekdays"
                                    :key="day.value"
                                    :class="{ selected: formData.frequency_detail.weekdays?.includes(day.value) }"
                                >
                                    <input
                                        type="checkbox"
                                        :value="day.value"
                                        v-model="formData.frequency_detail.weekdays"
                                    >
                                    {{ day.label }}
                                </label>
                            </div>
                        </div>

                        <!-- 每月设置 -->
                        <div class="form-group" v-if="formData.frequency_type === 'monthly'">
                            <label>每月几号</label>
                            <input
                                type="text"
                                v-model="monthlyDaysInput"
                                placeholder="如: 1,15,30"
                                class="form-input"
                            >
                        </div>

                        <div class="form-group">
                            <label>每日用药时间 (设置好时间后请点击添加按钮) *</label>
                            <div class="time-input-wrapper">
                                <input
                                    type="time"
                                    v-model="newTimePoint"
                                    @keyup.enter="addTimePoint"
                                    class="form-input"
                                >
                                <button type="button" class="add-time-btn" @click="addTimePoint">添加</button>
                            </div>
                            <div class="time-points-list" v-if="formData.time_points.length > 0">
                                <span v-for="(time, index) in formData.time_points" :key="index" class="time-point-tag">
                                    {{ time }}
                                    <button type="button" @click="removeTimePoint(index)">×</button>
                                </span>
                            </div>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button class="btn-cancel" @click="prevStep">上一步</button>
                        <button class="btn-next" @click="nextStep">下一步</button>
                    </div>
                </div>

                <!-- 药品关联步骤 -->
                <div v-else-if="currentStep === 2" key="drugs" class="view-panel">
                    <div class="view-header">
                        <h3 class="view-title">关联药品</h3>
                        <p class="view-desc">选择计划关联的药品</p>
                    </div>

                    <div class="form-content">
                        <div class="drug-selector">
                            <div v-if="availableDrugs.length === 0" class="no-drugs-tip">
                                请先在药品管理中添加药品
                            </div>
                            <div v-else class="drug-checkbox-list">
                                <div
                                    v-for="drug in availableDrugs"
                                    :key="drug.id"
                                    class="drug-checkbox-item"
                                    @click="toggleDrug(drug.id)"
                                >
                                    <input
                                        type="checkbox"
                                        :checked="selectedDrugIds.includes(drug.id)"
                                        @click.stop
                                        @change="toggleDrug(drug.id)"
                                    >
                                    <span class="drug-name">{{ drug.name }}</span>
                                    <input
                                        type="text"
                                        :value="selectedDrugDosages[drug.id] || drug.dosage"
                                        @input="updateDosage(drug.id, ($event.target as HTMLInputElement).value)"
                                        placeholder="用量"
                                        class="dosage-input"
                                        @click.stop
                                    >
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button class="btn-cancel" @click="prevStep">上一步</button>
                        <button class="btn-submit" @click="handleSubmit" :disabled="submitting">
                            {{ submitting ? '保存中...' : '保存' }}
                        </button>
                    </div>
                </div>
            </Transition>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, onMounted } from 'vue'
    import { getDrugList } from '@/api/drug'
    import FlowSelect from '../common/FlowSelect.vue';
    import type { Drug } from '@/types/drugTypes'
    import type { Plan, CreatePlanRequest, UpdatePlanRequest, PlanType, FrequencyType, FrequencyDetail } from '@/types/planTypes'

    const props = defineProps<{
        editingPlan?: Plan | null
    }>()

    const emit = defineEmits<{
        'close': []
        'success': []
    }>()

    // 步骤配置
    const steps = [
        { id: 'basic', title: '基本信息', desc: '填写计划名称和类型' },
        { id: 'frequency', title: '频率设置', desc: '设置用药频率和时间' },
        { id: 'drugs', title: '关联药品', desc: '选择计划关联的药品' }
    ]

    // 当前步骤
    const currentStep = ref(0)

    // 星期选项
    const weekdays = [
        { value: 1, label: '周一' },
        { value: 2, label: '周二' },
        { value: 3, label: '周三' },
        { value: 4, label: '周四' },
        { value: 5, label: '周五' },
        { value: 6, label: '周六' },
        { value: 7, label: '周日' }
    ]

    // 月份天数输入
    const monthlyDaysInput = ref('')

    // 新增时间点
    const newTimePoint = ref('')

    // 药品列表
    const availableDrugs = ref<Drug[]>([])

    // 选中的药品
    const selectedDrugIds = ref<number[]>([])
    const selectedDrugDosages = reactive<Record<number, string>>({})

    // 提交状态
    const submitting = ref(false)

    // 表单数据
    const formData = reactive<{
        name: string
        plan_type: PlanType
        start_date: string
        end_date: string
        frequency_type: FrequencyType
        frequency_detail: FrequencyDetail
        time_points: string[]
        sms_enabled: boolean
    }>({
        name: '',
        plan_type: '长期',
        start_date: '',
        end_date: '',
        frequency_type: 'daily',
        frequency_detail: {},
        time_points: [],
        sms_enabled: false
    })

    // 初始化
    onMounted(async () => {
        await loadAvailableDrugs()

        if (props.editingPlan) {
            // 编辑模式
            Object.assign(formData, {
                name: props.editingPlan.name,
                plan_type: props.editingPlan.plan_type,
                start_date: props.editingPlan.start_date.split('T')[0],
                end_date: props.editingPlan.end_date ? props.editingPlan.end_date.split('T')[0] : '',
                frequency_type: props.editingPlan.frequency_type,
                frequency_detail: props.editingPlan.frequency_detail ? { ...props.editingPlan.frequency_detail } : {},
                time_points: [...props.editingPlan.time_points],
                sms_enabled: props.editingPlan.sms_enabled
            })

            if (props.editingPlan.drugs) {
                props.editingPlan.drugs.forEach(pd => {
                    selectedDrugIds.value.push(pd.drug_id)
                    selectedDrugDosages[pd.drug_id] = pd.dosage
                })
            }

            if (props.editingPlan.frequency_type === 'monthly' && props.editingPlan.frequency_detail?.days_of_month) {
                monthlyDaysInput.value = props.editingPlan.frequency_detail.days_of_month.join(',')
            }
        } else {
            // 添加模式
            formData.start_date = new Date().toISOString().split('T')[0] as string
        }
    })

    // 加载药品列表
    const loadAvailableDrugs = async () => {
        try {
            const res = await getDrugList()
            availableDrugs.value = res.items
        } catch (error) {
            console.error('加载药品列表失败:', error)
        }
    }

    // 下一步
    const nextStep = () => {
        if (currentStep.value < steps.length - 1) {
            currentStep.value++
        }
    }

    // 上一步
    const prevStep = () => {
        if (currentStep.value > 0) {
            currentStep.value--
        }
    }

    // 处理频率类型变化
    const handleFrequencyChange = () => {
        formData.frequency_detail = {}
        if (formData.frequency_type === 'weekly') {
            formData.frequency_detail.weekdays = []
        } else if (formData.frequency_type === 'monthly') {
            monthlyDaysInput.value = ''
        }
    }

    // 添加时间点
    const addTimePoint = () => {
        if (newTimePoint.value && !formData.time_points.includes(newTimePoint.value)) {
            formData.time_points.push(newTimePoint.value)
            formData.time_points.sort()
            newTimePoint.value = ''
        }
    }

    // 移除时间点
    const removeTimePoint = (index: number) => {
        formData.time_points.splice(index, 1)
    }

    // 切换药品选择
    const toggleDrug = (drugId: number) => {
        const index = selectedDrugIds.value.indexOf(drugId)
        if (index > -1) {
            selectedDrugIds.value.splice(index, 1)
            delete selectedDrugDosages[drugId]
        } else {
            selectedDrugIds.value.push(drugId)
        }
    }

    // 更新用量
    const updateDosage = (drugId: number, dosage: string) => {
        selectedDrugDosages[drugId] = dosage
    }

    // 提交表单
    const handleSubmit = async () => {
        if (!formData.name.trim()) {
            alert('请输入计划名称')
            return
        }
        if (formData.time_points.length === 0) {
            alert('请至少添加一个用药时间')
            return
        }
        if (selectedDrugIds.value.length === 0) {
            alert('请至少选择一个药品')
            return
        }

        submitting.value = true

        try {
            const frequency_detail: FrequencyDetail = { ...formData.frequency_detail }

            if (formData.frequency_type === 'monthly' && monthlyDaysInput.value) {
                frequency_detail.days_of_month = monthlyDaysInput.value.split(',').map(d => Number(d.trim())).filter(d => !isNaN(d))
            }

            const drug_ids = selectedDrugIds.value.map(id => ({
                drug_id: id,
                dosage: selectedDrugDosages[id] || ''
            }))

            const planStore = (await import('@/stores/planStore')).usePlanStore()

            if (props.editingPlan) {
                const data: UpdatePlanRequest = {
                    name: formData.name,
                    plan_type: formData.plan_type,
                    start_date: formData.start_date,
                    end_date: formData.end_date || undefined,
                    frequency_type: formData.frequency_type,
                    frequency_detail,
                    time_points: formData.time_points,
                    sms_enabled: formData.sms_enabled,
                    drug_ids
                }
                await planStore.editPlan(props.editingPlan.id, data)
            } else {
                const data: CreatePlanRequest = {
                    name: formData.name,
                    plan_type: formData.plan_type,
                    start_date: formData.start_date,
                    end_date: formData.end_date || undefined,
                    frequency_type: formData.frequency_type,
                    frequency_detail,
                    time_points: formData.time_points,
                    sms_enabled: formData.sms_enabled,
                    drug_ids
                }
                await planStore.addPlan(data)
            }

            emit('success')
            handleClose()
        } catch (error) {
            console.error('保存计划失败:', error)
        } finally {
            submitting.value = false
        }
    }

    // 关闭弹窗
    const handleClose = () => {
        emit('close')
    }
</script>

<style scoped>
    .plan-form-modal {
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
        position: relative;
    }

    .view-panel {
        flex: 1;
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    .view-header {
        margin-bottom: 24px;
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

    .form-content {
        flex: 1;
        overflow-y: auto;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-group label {
        display: block;
        margin-bottom: 8px;
        color: #666;
        font-size: 14px;
    }

    .form-row {
        display: flex;
        gap: 15px;
    }

    .form-row .form-group {
        flex: 1;
    }

    .form-input,
    .form-select {
        width: 100%;
        padding: 12px 15px;
        border: 2px solid #e2e2e2;
        border-radius: 12px;
        font-size: 14px;
        color: #333;
        transition: all 0.3s ease;
        box-sizing: border-box;
    }

    .form-input:focus,
    .form-select:focus {
        outline: none;
        border-color: #7494ec;
        box-shadow: 0 0 0 4px rgba(116, 148, 236, 0.15);
    }

    .checkbox-label {
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        color: #333;
    }

    .checkbox-label input[type="checkbox"] {
        width: 18px;
        height: 18px;
    }

    .weekday-selector {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .weekday-selector label {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 8px 12px;
        background: #f5f5f5;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .weekday-selector label.selected {
        background: #7494ec;
        color: #fff;
    }

    .weekday-selector input {
        display: none;
    }

    .time-input-wrapper {
        display: flex;
        gap: 10px;
    }

    .time-input-wrapper .form-input {
        flex: 1;
    }

    .add-time-btn {
        padding: 12px 20px;
        border: none;
        border-radius: 12px;
        background: #7494ec;
        color: #fff;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .add-time-btn:hover {
        background: #5a7de0;
    }

    .time-points-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 10px;
    }

    .time-point-tag {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 6px 12px;
        background: #e3edff;
        color: #7494ec;
        border-radius: 15px;
        font-size: 14px;
    }

    .time-point-tag button {
        width: 18px;
        height: 18px;
        border: none;
        background: rgba(116, 148, 236, 0.3);
        border-radius: 50%;
        color: #7494ec;
        font-size: 14px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .drug-selector {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 10px;
    }

    .no-drugs-tip {
        text-align: center;
        color: #999;
        padding: 20px;
    }

    .drug-checkbox-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .drug-checkbox-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px;
        background: #f9f9f9;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .drug-checkbox-item:hover {
        background: #eef0f8;
    }

    .drug-checkbox-item input[type="checkbox"] {
        width: 18px;
        height: 18px;
    }

    .drug-checkbox-item .drug-name {
        flex: 1;
        color: #333;
    }

    .drug-checkbox-item .dosage-input {
        width: 80px;
        padding: 6px 10px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        font-size: 13px;
    }

    .form-actions {
        display: flex;
        gap: 15px;
        justify-content: flex-end;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #f0f0f0;
    }

    .btn-cancel,
    .btn-next,
    .btn-submit {
        padding: 12px 25px;
        border: none;
        border-radius: 20px;
        font-size: 14px;
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

    .btn-next,
    .btn-submit {
        background: #7494ec;
        color: #fff;
    }

    .btn-next:hover,
    .btn-submit:hover:not(:disabled) {
        background: #5a7de0;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(116, 148, 236, 0.3);
    }

    .btn-submit:disabled {
        opacity: 0.6;
        cursor: not-allowed;
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
        .plan-form-modal {
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

        .close-icon {
            top: 10px;
            right: 10px;
            width: 32px;
            height: 32px;
        }

        .form-row {
            flex-direction: column;
        }
    }
</style>