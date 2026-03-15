<template>
    <div class="search-bar-container">
        <!-- 搜索输入框 -->
        <div class="search-input-wrapper">
            <!-- 搜索标志 -->
            <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M15.5 14H14.71L14.43 13.73C15.41 12.59 16 11.11 16 9.5C16 5.91 13.09 3 9.5 3C5.91 3 3 5.91 3 9.5C3 13.09 5.91 16 9.5 16C11.11 16 12.59 15.41 13.73 14.43L14 14.71V15.5L19 20.49L20.49 19L15.5 14ZM9.5 14C7.01 14 5 11.99 5 9.5C5 7.01 7.01 5 9.5 5C11.99 5 14 7.01 14 9.5C14 11.99 11.99 14 9.5 14Z" fill="currentColor"/>
            </svg>

            <!-- 输入框 -->
            <input
                type="text"
                v-model="searchKeyword"
                placeholder="搜索药品名称..."
                @input="handleSearch"
                class="search-input"
            >

            <!-- 清空按钮 -->
            <button v-if="searchKeyword" class="clear-search" @click="clearSearch">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
                </svg>
            </button>
        </div>

        <!-- 筛选栏 -->
        <div class="flow-select">
            <FlowSelect
            :options="SearchOption"
            v-model="selectOption"
            @change="handleSearch"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue'
    import FlowSelect from '../common/FlowSelect.vue'
    import type { UsageMethod } from '@/types/drugTypes'

    // 搜索关键字
    const searchKeyword = ref<string>('')
    const selectOption = ref<UsageMethod|''>('')
    const SearchOption = [
        { value: '', label: '全部用法' },
        { value: '口服', label: '口服' },
        { value: '注射', label: '注射' },
        { value: '外用', label: '外用' },
        { value: '滴入', label: '滴入' },
        { value: '吸入', label: '吸入' },
        { value: '其他', label: '其他' }
    ]

    // 定义搜索事件
    const emit = defineEmits<{
        'search': [searchKeyword: string, selectOption: UsageMethod|'']
        }>()

    // 执行搜索
    const handleSearch = () => {
        emit('search', searchKeyword.value, selectOption.value)
    }

    // 清空搜索栏
    const clearSearch = () => {
        searchKeyword.value = ''
        handleSearch()
    }

</script>

<style scoped>
    .search-bar-container {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* 搜索区域 */
    .search-input-wrapper {
        display: flex;
        align-items: center;
        gap: 10px;
        height: 50px;
        width: 50%;
        padding: 12px 18px;
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(116, 148, 236, 0.1);
        transition: all 0.3s ease;
    }

    .search-input-wrapper:focus-within {
        box-shadow: 0 4px 20px rgba(116, 148, 236, 0.2);
    }

    .search-icon {
        color: #999;
        flex-shrink: 0;
        transition: color 0.3s ease;
    }

    .search-input-wrapper:focus-within .search-icon {
        color: #7494ec;
    }

    .search-input {
        flex: 1;
        border: none;
        background: transparent;
        outline: none;
        font-size: 14px;
        color: #333;
    }

    .search-input::placeholder {
        color: #aaa;
    }

    .clear-search {
        width: 24px;
        height: 24px;
        border: none;
        background: #f0f0f0;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #999;
        transition: all 0.2s ease;
    }

    .clear-search:hover {
        background: #ff6b6b;
        color: #fff;
    }

    .filter-wrapper {
        position: relative;
    }

    .filter-select {
        padding: 12px 36px 12px 16px;
        border: none;
        border-radius: 20px;
        background: #fff;
        font-size: 14px;
        color: #666;
        cursor: pointer;
        outline: none;
        box-shadow: 0 4px 20px rgba(116, 148, 236, 0.1);
        appearance: none;
        background-image: url("data:image/svg+xml,%3Csvg width='12' height='12' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M7 10L12 15L17 10' stroke='%23999' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 14px center;
        transition: all 0.3s ease;
    }

    .filter-select:hover {
        box-shadow: 0 4px 20px rgba(116, 148, 236, 0.2);
    }

    .filter-select:focus {
        box-shadow: 0 4px 20px rgba(116, 148, 236, 0.2);
    }

    .flow-select {
        width: 200px;
    }
</style>