<template>
    <div class="status-filter-container">
        <button
            :class="['filter-tab', { active: modelValue === '' }]"
            @click="handleChange('')"
        >
            全部
        </button>
        <button
            :class="['filter-tab', { active: modelValue === 'active' }]"
            @click="handleChange('active')"
        >
            进行中
        </button>
        <button
            :class="['filter-tab', { active: modelValue === 'paused' }]"
            @click="handleChange('paused')"
        >
            已暂停
        </button>
        <button
            :class="['filter-tab', { active: modelValue === 'completed' }]"
            @click="handleChange('completed')"
        >
            已完成
        </button>
    </div>
</template>

<script setup lang="ts">
    import type { PlanStatus } from '@/types/planTypes'

    const props = defineProps<{
        modelValue: PlanStatus | ''
    }>()

    const emit = defineEmits<{
        'update:modelValue': [value: PlanStatus | '']
    }>()

    const handleChange = (value: PlanStatus | '') => {
        emit('update:modelValue', value)
    }
</script>

<style scoped>
    .status-filter-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }

    .filter-tab {
        padding: 8px 20px;
        border: none;
        border-radius: 20px;
        background: #f5f5f5;
        color: #666;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .filter-tab:hover {
        background: #e8e8e8;
        transform: translateY(-2px);
    }

    .filter-tab.active {
        background: linear-gradient(135deg, #7494ec 0%, #5a7de0 100%);
        color: #fff;
        box-shadow: 0 4px 15px rgba(116, 148, 236, 0.3);
    }
</style>