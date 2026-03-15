<template>
    <div class="flow-select" ref="selectRef">
        <!-- 触发器 -->
        <div class="flow-select-trigger" @click="toggleDropdown" :class="{ 'is-focused': isOpen, 'is-disabled': disabled }">
            <slot name="trigger" :selected="selectedLabel" :isOpen="isOpen">
                <div class="default-trigger">
                    <span class="trigger-text" :class="{ 'placeholder': !selectedLabel }">
                        {{ selectedLabel || placeholder }}
                    </span>
                    <svg class="arrow-icon" :class="{ 'is-open': isOpen }" width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
            </slot>
        </div>

        <!-- 下拉菜单 -->
        <transition name="dropdown-fade">
            <div v-if="isOpen" class="flow-select-dropdown" :style="dropdownStyle">
                <div class="dropdown-content">
                    <div
                        v-for="option in options"
                        class="dropdown-item"
                        :class="{ 'is-selected': option.value === modelValue }"
                        @click="selectOption(option)"
                    >
                        <slot name="option" :option="option" :isSelected="option.value === modelValue">
                            <span class="option-label">{{ option.label }}</span>
                            <svg v-if="option.value === modelValue" class="check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none">
                                <path d="M9 16.17L4.83 12L3.41 13.41L9 19L21 7L19.59 5.59L9 16.17Z" fill="currentColor"/>
                            </svg>
                        </slot>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed, onMounted, onUnmounted } from 'vue'

    interface Option {
        value: string | number | null
        label: string
        [key: string]: any
    }

    interface Props {
        modelValue?: string | number | null
        options: Option[]
        placeholder?: string
        disabled?: boolean
    }

    const props = withDefaults(defineProps<Props>(), {
        modelValue: null,
        placeholder: '请选择',
        disabled: false
    })

    const emit = defineEmits<{
        'update:modelValue': [value: string | number | null]
        'change': [value: string | number | null]
    }>()

    const isOpen = ref(false)
    const selectRef = ref<HTMLElement | null>(null)

    const selectedLabel = computed(() => {
        if (props.modelValue === null || props.modelValue === undefined) return ''
        const option = props.options.find(opt => opt.value === props.modelValue)
        return option?.label || ''
    })

    const toggleDropdown = () => {
        if (props.disabled) return
        isOpen.value = !isOpen.value
    }

    const selectOption = (option: Option) => {
        emit('update:modelValue', option.value)
        emit('change', option.value)
        isOpen.value = false
    }

    // 点击外部关闭
    const handleClickOutside = (event: MouseEvent) => {
        if (selectRef.value && !selectRef.value.contains(event.target as Node)) {
            isOpen.value = false
        }
    }

    // 计算下拉菜单位置
    const dropdownStyle = computed(() => {
        if (!selectRef.value) return {}
        const rect = selectRef.value.getBoundingClientRect()
        return {
            top: `${rect.bottom + 8}px`,
            left: `${rect.left}px`,
            width: `${rect.width}px`
        }
    })

    onMounted(() => {
        document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
        document.removeEventListener('click', handleClickOutside)
    })
</script>

<style scoped>
    .flow-select {
        position: relative;
        width: 100%;
    }

    /* 触发器 */
    .flow-select-trigger {
        cursor: pointer;
    }

    .flow-select-trigger.is-disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .default-trigger {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 15px;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        background: #fff;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .flow-select-trigger.is-focused .default-trigger {
        border-color: #7494ec;
        box-shadow: 0 0 0 4px rgba(116, 148, 236, 0.15);
    }

    .trigger-text {
        color: #333;
        font-size: 14px;
    }

    .trigger-text.placeholder {
        color: #999;
    }

    .arrow-icon {
        color: #999;
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .arrow-icon.is-open {
        transform: rotate(180deg);
    }

    /* 下拉菜单 */
    .flow-select-dropdown {
        position: fixed;
        z-index: 1000;
    }

    .dropdown-content {
        background: #fff;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        overflow: hidden;
        max-height: 240px;
        overflow-y: auto;
    }

    /* 隐藏滚动条 */
    .dropdown-content::-webkit-scrollbar {
        width: 6px;
    }

    .dropdown-content::-webkit-scrollbar-track {
        background: transparent;
    }

    .dropdown-content::-webkit-scrollbar-thumb {
        background: #e0e0e0;
        border-radius: 3px;
    }

    .dropdown-content::-webkit-scrollbar-thumb:hover {
        background: #ccc;
    }

    /* 选项 */
    .dropdown-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 16px;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .dropdown-item:hover {
        background: #f5f8ff;
    }

    .dropdown-item.is-selected {
        background: #e8f0ff;
    }

    .dropdown-item.is-selected .option-label {
        color: #7494ec;
        font-weight: 500;
    }

    .option-label {
        color: #333;
        font-size: 14px;
    }

    .check-icon {
        color: #7494ec;
    }

    /* 下拉动画 */
    .dropdown-fade-enter-active,
    .dropdown-fade-leave-active {
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .dropdown-fade-enter-from,
    .dropdown-fade-leave-to {
        opacity: 0;
        transform: translateY(-10px) scale(0.95);
    }

    .dropdown-fade-enter-to,
    .dropdown-fade-leave-from {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
</style>
