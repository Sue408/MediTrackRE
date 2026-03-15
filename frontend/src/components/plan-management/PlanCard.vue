<template>
    <div class="plan-card">
        <div class="plan-header">
            <div class="plan-info">
                <h4>{{ plan.name }}</h4>
                <span :class="['status-badge', plan.status]">
                    {{ getStatusText(plan.status) }}
                </span>
            </div>
            <div class="plan-actions">
                <button
                    v-if="plan.status === 'active'"
                    class="action-btn pause"
                    @click="$emit('pause', plan)"
                    title="暂停"
                >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                        <path d="M6 19H10V5H6V19ZM14 5V19H18V5H14Z" fill="currentColor"/>
                    </svg>
                </button>
                <button
                    v-if="plan.status === 'paused'"
                    class="action-btn resume"
                    @click="$emit('resume', plan)"
                    title="恢复"
                >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                        <path d="M8 5V19L19 12L8 5Z" fill="currentColor"/>
                    </svg>
                </button>
                <button
                    class="action-btn edit"
                    @click="$emit('edit', plan)"
                    title="编辑"
                >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                        <path d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z" fill="currentColor"/>
                    </svg>
                </button>
                <button
                    class="action-btn delete"
                    @click="$emit('delete', plan)"
                    title="删除"
                >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                        <path d="M6 19C6 20.1 6.9 21 8 21H16C17.1 21 18 20.1 18 19V7H6V19ZM19 4H15.5L14.5 3H9.5L8.5 4H5V6H19V4Z" fill="currentColor"/>
                    </svg>
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
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM12.5 7H11V13L16.2 16.2L17 14.9L12.5 12.2V7Z" fill="#7494ec"/>
            </svg>
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
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM20 16H6L4 18V4H20V16Z" fill="currentColor"/>
                </svg>
                短信提醒
            </span>
        </div>
    </div>
</template>

<script setup lang="ts">
    import type { Plan, PlanStatus, FrequencyType } from '@/types/planTypes'

    const props = defineProps<{
        plan: Plan
    }>()

    defineEmits<{
        'pause': [plan: Plan]
        'resume': [plan: Plan]
        'edit': [plan: Plan]
        'delete': [plan: Plan]
    }>()

    const getStatusText = (status: PlanStatus) => {
        const map: Record<PlanStatus, string> = {
            active: '进行中',
            paused: '已暂停',
            completed: '已完成'
        }
        return map[status]
    }

    const formatDate = (dateStr: string) => {
        const date = new Date(dateStr)
        return date.toLocaleDateString('zh-CN')
    }

    const getFrequencyText = (plan: Plan) => {
        const typeMap: Record<FrequencyType, string> = {
            daily: '每天',
            alternate: `每${plan.frequency_detail?.interval_days || 2}天`,
            weekly: '每周',
            monthly: '每月'
        }
        return typeMap[plan.frequency_type] || '未知'
    }
</script>

<style scoped>
    .plan-card {
        padding: 20px;
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .plan-card:hover {
        box-shadow: 0 4px 15px rgba(116, 148, 236, 0.2);
        transform: translateY(-2px);
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
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .action-btn.pause {
        background: #fff3e0;
        color: #ff9800;
    }

    .action-btn.pause:hover {
        background: #ff9800;
        color: #fff;
        transform: scale(1.1);
    }

    .action-btn.resume {
        background: #e3edff;
        color: #7494ec;
    }

    .action-btn.resume:hover {
        background: #7494ec;
        color: #fff;
        transform: scale(1.1);
    }

    .action-btn.edit {
        background: #e3edff;
        color: #7494ec;
    }

    .action-btn.edit:hover {
        background: #7494ec;
        color: #fff;
        transform: scale(1.1);
    }

    .action-btn.delete {
        background: #ffeaea;
        color: #ff6b6b;
    }

    .action-btn.delete:hover {
        background: #ff6b6b;
        color: #fff;
        transform: scale(1.1);
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
</style>