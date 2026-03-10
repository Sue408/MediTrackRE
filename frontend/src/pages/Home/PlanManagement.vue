<template>
    <div class="plan-management">
        <!-- 顶部操作栏 -->
        <div class="top-bar">
            <button class="back-btn" @click="backHome">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M15.41 7.41L14 6L8 12L14 18L15.41 16.59L10.83 12L15.41 7.41Z" fill="currentColor"/>
                </svg>
            </button>
            <h3>计划管理</h3>
            <button class="add-btn" @click="openAddModal">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
                </svg>
                创建计划
            </button>
        </div>

        <!-- 状态筛选 -->
        <div class="status-tabs">
            <button :class="['tab', { active: filterStatus === '' }]" @click="filterStatus = ''; loadPlanList()">
                全部
            </button>
            <button :class="['tab', { active: filterStatus === 'active' }]" @click="filterStatus = 'active'; loadPlanList()">
                进行中
            </button>
            <button :class="['tab', { active: filterStatus === 'paused' }]" @click="filterStatus = 'paused'; loadPlanList()">
                已暂停
            </button>
            <button :class="['tab', { active: filterStatus === 'completed' }]" @click="filterStatus = 'completed'; loadPlanList()">
                已完成
            </button>
        </div>

        <!-- 计划列表 -->
        <div class="plan-list" v-if="planList.length > 0">
            <div class="plan-card" v-for="plan in planList" :key="plan.id">
                <div class="plan-header">
                    <div class="plan-info">
                        <h4>{{ plan.name }}</h4>
                        <span :class="['status-badge', plan.status]">
                            {{ plan.status === 'active' ? '进行中' : plan.status === 'paused' ? '已暂停' : '已完成' }}
                        </span>
                    </div>
                    <div class="plan-actions">
                        <button v-if="plan.status === 'active'" class="action-btn pause" @click="handlePause(plan)" title="暂停">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M6 19H10V5H6V19ZM14 5V19H18V5H14Z" fill="currentColor"/></svg>
                        </button>
                        <button v-if="plan.status === 'paused'" class="action-btn resume" @click="handleResume(plan)" title="恢复">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M8 5V19L19 12L8 5Z" fill="currentColor"/></svg>
                        </button>
                        <button class="action-btn edit" @click="openEditModal(plan)" title="编辑">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z" fill="currentColor"/></svg>
                        </button>
                        <button class="action-btn delete" @click="confirmDelete(plan)" title="删除">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M6 19C6 20.1 6.9 21 8 21H16C17.1 21 18 20.1 18 19V7H6V19ZM19 4H15.5L14.5 3H9.5L8.5 4H5V6H19V4Z" fill="currentColor"/></svg>
                        </button>
                    </div>
                </div>

                <div class="plan-type">
                    <span class="type-tag">{{ plan.plan_type }}</span>
                    <span class="date-range">
                        {{ formatDate(plan.start_date) }}
                        {{ plan.end_date ? ' - ' + formatDate(plan.end_date) : ' 起长期' }}
                    </span>
                </div>

                <div class="plan-frequency">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM12.5 7H11V13L16.2 16.2L17 14.9L12.5 12.2V7Z" fill="#7494ec"/></svg>
                    <span>{{ getFrequencyText(plan) }}</span>
                </div>

                <div class="plan-time-points">
                    <span class="time-label">用药时间:</span>
                    <div class="time-tags">
                        <span v-for="time in plan.time_points" :key="time" class="time-tag">{{ time }}</span>
                    </div>
                </div>

                <div class="plan-drugs" v-if="plan.drugs && plan.drugs.length > 0">
                    <span class="drugs-label">关联药品:</span>
                    <div class="drug-tags">
                        <span v-for="pd in plan.drugs" :key="pd.id" class="drug-tag">
                            {{ pd.drug?.name || '未知' }} - {{ pd.dosage }}
                        </span>
                    </div>
                </div>

                <div class="plan-footer">
                    <span v-if="plan.sms_enabled" class="sms-badge">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM20 16H6L4 18V4H20V16Z" fill="currentColor"/></svg>
                        短信提醒
                    </span>
                </div>
            </div>
        </div>

        <!-- 空状态 -->
        <div class="empty-state" v-else>
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 4H5C3.89 4 3 4.9 3 6V20C3 21.1 3.89 22 5 22H19C20.1 22 21 21.1 21 20V6C21 4.9 20.1 4 19 4ZM19 20H5V9H19V20ZM7 11H12V13H7V11ZM7 15H15V17H7V15Z" fill="#ccc"/>
            </svg>
            <p>暂无用药计划</p>
            <button class="add-first-btn" @click="openAddModal">创建第一个计划</button>
        </div>

        <!-- 分页 -->
        <div class="pagination" v-if="total > pageSize">
            <button :disabled="page <= 1" @click="changePage(page - 1)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M15.41 7.41L14 6L8 12L14 18L15.41 16.59L10.83 12L15.41 7.41Z" fill="currentColor"/></svg>
            </button>
            <span>{{ page }} / {{ Math.ceil(total / pageSize) }}</span>
            <button :disabled="page >= Math.ceil(total / pageSize)" @click="changePage(page + 1)">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M8.59 16.59L10 18L16 12L10 6L8.59 7.41L13.17 12L8.59 16.59Z" fill="currentColor"/></svg>
            </button>
        </div>

        <!-- 添加/编辑弹窗 -->
        <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>{{ editingPlan ? '编辑计划' : '创建计划' }}</h3>
                    <button class="close-btn" @click="closeModal">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/></svg>
                    </button>
                </div>
                <form @submit.prevent="submitForm" class="plan-form">
                    <div class="form-group">
                        <label>计划名称 *</label>
                        <input type="text" v-model="formData.name" required placeholder="如: 每日降压药">
                    </div>

                    <div class="form-group">
                        <label>计划类型 *</label>
                        <select v-model="formData.plan_type" required>
                            <option value="长期">长期计划</option>
                            <option value="周期">周期计划</option>
                        </select>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>开始日期 *</label>
                            <input type="date" v-model="formData.start_date" required>
                        </div>
                        <div class="form-group" v-if="formData.plan_type === '周期'">
                            <label>结束日期</label>
                            <input type="date" v-model="formData.end_date">
                        </div>
                    </div>

                    <div class="form-group">
                        <label>用药频率 *</label>
                        <select v-model="formData.frequency_type" required @change="handleFrequencyChange">
                            <option value="daily">每天</option>
                            <option value="alternate">间隔天</option>
                            <option value="weekly">每周</option>
                            <option value="monthly">每月</option>
                        </select>
                    </div>

                    <!-- 间隔天设置 -->
                    <div class="form-group" v-if="formData.frequency_type === 'alternate'">
                        <label>间隔天数</label>
                        <input type="number" v-model="formData.frequency_detail.interval_days" min="1" placeholder="如: 2">
                    </div>

                    <!-- 每周设置 -->
                    <div class="form-group" v-if="formData.frequency_type === 'weekly'">
                        <label>选择星期</label>
                        <div class="weekday-selector">
                            <label v-for="day in weekdays" :key="day.value" :class="{ selected: formData.frequency_detail.weekdays?.includes(day.value) }">
                                <input type="checkbox" :value="day.value" v-model="formData.frequency_detail.weekdays">
                                {{ day.label }}
                            </label>
                        </div>
                    </div>

                    <!-- 每月设置 -->
                    <div class="form-group" v-if="formData.frequency_type === 'monthly'">
                        <label>每月几号</label>
                        <input type="text" v-model="monthlyDaysInput" placeholder="如: 1,15,30">
                    </div>

                    <div class="form-group">
                        <label>每日用药时间 *</label>
                        <div class="time-input-wrapper">
                            <input type="time" v-model="newTimePoint" @keyup.enter="addTimePoint">
                            <button type="button" class="add-time-btn" @click="addTimePoint">添加</button>
                        </div>
                        <div class="time-points-list" v-if="formData.time_points.length > 0">
                            <span v-for="(time, index) in formData.time_points" :key="index" class="time-point-tag">
                                {{ time }}
                                <button type="button" @click="removeTimePoint(index)">×</button>
                            </span>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>选择药品 *</label>
                        <div class="drug-selector">
                            <div v-if="availableDrugs.length === 0" class="no-drugs-tip">
                                请先在药品管理中添加药品
                            </div>
                            <div v-else class="drug-checkbox-list">
                                <label v-for="drug in availableDrugs" :key="drug.id" class="drug-checkbox-item">
                                    <input type="checkbox" :value="drug.id" v-model="selectedDrugIds">
                                    <span class="drug-name">{{ drug.name }}</span>
                                    <input type="text" v-model="selectedDrugDosages[drug.id]" placeholder="用量" class="dosage-input">
                                </label>
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="formData.sms_enabled">
                            启用短信提醒
                        </label>
                    </div>

                    <div class="form-actions">
                        <button type="button" class="btn-cancel" @click="closeModal">取消</button>
                        <button type="submit" class="btn-submit" :disabled="submitting">
                            {{ submitting ? '保存中...' : '保存' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- 删除确认弹窗 -->
        <div class="modal-overlay" v-if="showDeleteConfirm" @click.self="showDeleteConfirm = false">
            <div class="modal-content small">
                <div class="modal-header">
                    <h3>确认删除</h3>
                </div>
                <p class="confirm-text">确定要删除计划「{{ deletingPlan?.name }}」吗？此操作不可恢复。</p>
                <div class="form-actions">
                    <button class="btn-cancel" @click="showDeleteConfirm = false">取消</button>
                    <button class="btn-delete" @click="handleDelete" :disabled="deleting">
                        {{ deleting ? '删除中...' : '确认删除' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, reactive, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { getPlanList, createPlan, updatePlan, deletePlan, pausePlan, resumePlan } from '@/api/plan'
    import { getDrugList } from '@/api/drug'
    import type { Plan, CreatePlanRequest, UpdatePlanRequest, PlanStatus, FrequencyType, FrequencyDetail } from '@/types/planTypes'
    import type { Drug } from '@/types/drugTypes'

    const router = useRouter()

    // 列表数据
    const planList = ref<Plan[]>([])
    const total = ref(0)
    const page = ref(1)
    const pageSize = 10
    const filterStatus = ref<PlanStatus | ''>('')

    // 药品列表
    const availableDrugs = ref<Drug[]>([])

    // 弹窗状态
    const showModal = ref(false)
    const showDeleteConfirm = ref(false)
    const editingPlan = ref<Plan | null>(null)
    const deletingPlan = ref<Plan | null>(null)
    const submitting = ref(false)
    const deleting = ref(false)

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

    // 选中的药品
    const selectedDrugIds = ref<number[]>([])
    const selectedDrugDosages = reactive<Record<number, string>>({})

    // 表单数据
    const formData = reactive<{
        name: string
        plan_type: '长期' | '周期'
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

    // 返回首页
    const backHome = () => {
        router.replace('/')
    }

    // 加载计划列表
    const loadPlanList = async () => {
        try {
            const res = await getPlanList({
                page: page.value,
                page_size: pageSize,
                status: filterStatus.value || undefined
            })
            planList.value = res.items
            total.value = res.total
        } catch (error) {
            console.error('加载计划列表失败:', error)
        }
    }

    // 加载药品列表
    const loadAvailableDrugs = async () => {
        try {
            const res = await getDrugList({ page_size: 100 })
            availableDrugs.value = res.items
        } catch (error) {
            console.error('加载药品列表失败:', error)
        }
    }

    // 翻页
    const changePage = (newPage: number) => {
        page.value = newPage
        loadPlanList()
    }

    // 格式化日期
    const formatDate = (dateStr: string) => {
        const date = new Date(dateStr)
        return date.toLocaleDateString('zh-CN')
    }

    // 获取频率文本
    const getFrequencyText = (plan: Plan) => {
        const typeMap: Record<FrequencyType, string> = {
            daily: '每天',
            alternate: `每${plan.frequency_detail?.interval_days || 2}天`,
            weekly: '每周',
            monthly: '每月'
        }
        return typeMap[plan.frequency_type] || '未知'
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

    // 打开添加弹窗
    const openAddModal = async () => {
        editingPlan.value = null
        Object.assign(formData, {
            name: '',
            plan_type: '长期',
            start_date: new Date().toISOString().split('T')[0],
            end_date: '',
            frequency_type: 'daily',
            frequency_detail: {},
            time_points: [],
            sms_enabled: false
        })
        selectedDrugIds.value = []
        Object.keys(selectedDrugDosages).forEach(key => delete selectedDrugDosages[Number(key)])
        monthlyDaysInput.value = ''
        newTimePoint.value = ''
        await loadAvailableDrugs()
        showModal.value = true
    }

    // 打开编辑弹窗
    const openEditModal = async (plan: Plan) => {
        editingPlan.value = plan
        Object.assign(formData, {
            name: plan.name,
            plan_type: plan.plan_type,
            start_date: plan.start_date.split('T')[0],
            end_date: plan.end_date ? plan.end_date.split('T')[0] : '',
            frequency_type: plan.frequency_type,
            frequency_detail: plan.frequency_detail ? { ...plan.frequency_detail } : {},
            time_points: [...plan.time_points],
            sms_enabled: plan.sms_enabled
        })

        // 设置选中药品
        selectedDrugIds.value = []
        Object.keys(selectedDrugDosages).forEach(key => delete selectedDrugDosages[Number(key)])

        if (plan.drugs) {
            plan.drugs.forEach(pd => {
                selectedDrugIds.value.push(pd.drug_id)
                selectedDrugDosages[pd.drug_id] = pd.dosage
            })
        }

        if (plan.frequency_type === 'monthly' && plan.frequency_detail?.days_of_month) {
            monthlyDaysInput.value = plan.frequency_detail.days_of_month.join(',')
        }

        await loadAvailableDrugs()
        showModal.value = true
    }

    // 关闭弹窗
    const closeModal = () => {
        showModal.value = false
        editingPlan.value = null
    }

    // 提交表单
    const submitForm = async () => {
        if (submitting.value) return
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

            if (editingPlan.value) {
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
                await updatePlan(editingPlan.value.id, data)
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
                await createPlan(data)
            }
            closeModal()
            loadPlanList()
        } catch (error) {
            console.error('保存计划失败:', error)
        } finally {
            submitting.value = false
        }
    }

    // 暂停计划
    const handlePause = async (plan: Plan) => {
        try {
            await pausePlan(plan.id)
            loadPlanList()
        } catch (error) {
            console.error('暂停计划失败:', error)
        }
    }

    // 恢复计划
    const handleResume = async (plan: Plan) => {
        try {
            await resumePlan(plan.id)
            loadPlanList()
        } catch (error) {
            console.error('恢复计划失败:', error)
        }
    }

    // 确认删除
    const confirmDelete = (plan: Plan) => {
        deletingPlan.value = plan
        showDeleteConfirm.value = true
    }

    // 执行删除
    const handleDelete = async () => {
        if (!deletingPlan.value || deleting.value) return
        deleting.value = true

        try {
            await deletePlan(deletingPlan.value.id)
            showDeleteConfirm.value = false
            deletingPlan.value = null
            loadPlanList()
        } catch (error) {
            console.error('删除计划失败:', error)
        } finally {
            deleting.value = false
        }
    }

    onMounted(() => {
        loadPlanList()
    })
</script>

<style scoped>
    .plan-management {
        padding: 20px;
        height: 100%;
        overflow-y: auto;
    }

    .top-bar {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }

    .back-btn {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border: none;
        background: #7494ec;
        color: #fff;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .back-btn:hover {
        background: #5a7de0;
        transform: scale(1.1);
    }

    .top-bar h3 {
        flex: 1;
        color: #333;
        margin: 0;
    }

    .add-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        border: none;
        border-radius: 20px;
        background: #7494ec;
        color: #fff;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .add-btn:hover {
        background: #5a7de0;
    }

    .status-tabs {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }

    .tab {
        padding: 8px 20px;
        border: none;
        border-radius: 20px;
        background: #f5f5f5;
        color: #666;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .tab:hover {
        background: #e8e8e8;
    }

    .tab.active {
        background: #7494ec;
        color: #fff;
    }

    .plan-list {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .plan-card {
        padding: 20px;
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    .plan-card:hover {
        box-shadow: 0 4px 15px rgba(116, 148, 236, 0.2);
    }

    .plan-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 15px;
    }

    .plan-info {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .plan-info h4 {
        margin: 0;
        color: #333;
        font-size: 18px;
    }

    .status-badge {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
    }

    .status-badge.active {
        background: #e3edff;
        color: #7494ec;
    }

    .status-badge.paused {
        background: #fff3e0;
        color: #ff9800;
    }

    .status-badge.completed {
        background: #e8f5e9;
        color: #4caf50;
    }

    .plan-actions {
        display: flex;
        gap: 8px;
    }

    .action-btn {
        width: 32px;
        height: 32px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .action-btn.pause {
        background: #fff3e0;
        color: #ff9800;
    }

    .action-btn.pause:hover {
        background: #ff9800;
        color: #fff;
    }

    .action-btn.resume {
        background: #e3edff;
        color: #7494ec;
    }

    .action-btn.resume:hover {
        background: #7494ec;
        color: #fff;
    }

    .action-btn.edit {
        background: #e3edff;
        color: #7494ec;
    }

    .action-btn.edit:hover {
        background: #7494ec;
        color: #fff;
    }

    .action-btn.delete {
        background: #ffeaea;
        color: #ff6b6b;
    }

    .action-btn.delete:hover {
        background: #ff6b6b;
        color: #fff;
    }

    .plan-type {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }

    .type-tag {
        padding: 4px 12px;
        background: #f5f5f5;
        border-radius: 12px;
        font-size: 12px;
        color: #666;
    }

    .date-range {
        font-size: 13px;
        color: #999;
    }

    .plan-frequency {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
        font-size: 14px;
        color: #666;
    }

    .plan-time-points {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
    }

    .time-label,
    .drugs-label {
        font-size: 13px;
        color: #999;
    }

    .time-tags,
    .drug-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .time-tag {
        padding: 4px 10px;
        background: #e3edff;
        color: #7494ec;
        border-radius: 10px;
        font-size: 13px;
    }

    .plan-drugs {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 12px;
    }

    .drug-tag {
        padding: 4px 10px;
        background: #f5f5f5;
        color: #666;
        border-radius: 10px;
        font-size: 13px;
    }

    .plan-footer {
        padding-top: 12px;
        border-top: 1px solid #f0f0f0;
    }

    .sms-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        background: #e3edff;
        color: #7494ec;
        border-radius: 10px;
        font-size: 12px;
    }

    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 20px;
        color: #999;
    }

    .empty-state p {
        margin: 20px 0;
        font-size: 16px;
    }

    .add-first-btn {
        padding: 12px 30px;
        border: none;
        border-radius: 25px;
        background: #7494ec;
        color: #fff;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .add-first-btn:hover {
        background: #5a7de0;
    }

    .pagination {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-top: 30px;
    }

    .pagination button {
        width: 36px;
        height: 36px;
        border: 1px solid #e0e0e0;
        border-radius: 50%;
        background: #fff;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .pagination button:hover:not(:disabled) {
        background: #7494ec;
        color: #fff;
        border-color: #7494ec;
    }

    .pagination button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .pagination span {
        color: #666;
        font-size: 14px;
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
        max-width: 500px;
        max-height: 90vh;
        overflow-y: auto;
        background: #fff;
        border-radius: 25px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    }

    .modal-content.small {
        max-width: 380px;
        padding: 25px;
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

    .plan-form {
        padding: 25px;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-row {
        display: flex;
        gap: 15px;
    }

    .form-row .form-group {
        flex: 1;
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

    .time-input-wrapper input {
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
        max-height: 200px;
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

    .checkbox-label {
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
    }

    .checkbox-label input[type="checkbox"] {
        width: 18px;
        height: 18px;
    }

    .form-actions {
        display: flex;
        gap: 15px;
        justify-content: flex-end;
        margin-top: 25px;
    }

    .btn-cancel,
    .btn-submit,
    .btn-delete {
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

    .btn-submit {
        background: #7494ec;
        color: #fff;
    }

    .btn-submit:hover:not(:disabled) {
        background: #5a7de0;
    }

    .btn-submit:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .btn-delete {
        background: #ff6b6b;
        color: #fff;
    }

    .btn-delete:hover:not(:disabled) {
        background: #e05555;
    }

    .confirm-text {
        padding: 20px 25px;
        color: #666;
        line-height: 1.6;
    }
</style>
