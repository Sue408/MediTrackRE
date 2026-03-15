<template>
    <div class="drug-management-container">
        <!-- 顶部操作栏 -->
        <div class="top-bar">
            <TopBar @addDrug="addDrug" :total="total"/>
        </div>

        <!-- 搜索筛选栏 -->
         <div class="search-bar">
            <SearchBar @search="handleSearch" />
         </div>

        <!-- 药品列表视图 -->
         <div class="drug-list">
            <DrugList
             :drug-info-list="drugInfoList"
             @addDrug="addDrug"
             @editDrug="editDrug"
             @deleteDrug="openDeleteDrug"
             />
         </div>

        <!-- 遮罩层 -->
        <div
        class="modal-container"
        :class="{show: showModal}"
        v-if="showModal && showModal !== 'Delete'"
        @click="closeModal">
            <!-- 药品添加弹窗 -->
            <div class="modal drug-add" v-if="showModal === 'Add'">
                <DrugAddModal @success="handleAddSuccess" @close="closeModal" />
            </div>

            <!-- 药品编辑弹窗 -->
            <div class="modal drug-edit" v-if="showModal === 'Edit'">
                <DrugEditPanel
                :drug="edittingDrug"
                @cancel="closeModal"
                @confirm="confirmEditting"
                />
            </div>
        </div>

        <!-- 删除确认弹窗 -->
        <ConfirmModal
        :visible="showModal === 'Delete'",
        message="确定要删除该药品吗?"
        @cancel="closeModal"
        @confirm="confirmDelete"
        />
    </div>
</template>

<script setup lang="ts">
    import { ref, computed } from 'vue'
    import TopBar from '@/components/drug-management/TopBar.vue';
    import SearchBar from '@/components/drug-management/SearchBar.vue';
    import DrugList from '@/components/drug-management/DrugList.vue';
    import type { Drug, UpdateDrugRequest, UsageMethod } from '@/types/drugTypes'
    import DrugAddModal from '@/components/drug-management/DrugAddModal.vue';
    import DrugEditPanel from '@/components/drug-management/DrugEditPanel.vue';
    import ConfirmModal from '@/components/common/ConfirmModal.vue';
    import { useDrugStore } from '@/stores/drugStore';

    // 使用药品 store
    const drugStore = useDrugStore()

    // 使用 store 中的数据
    const total = computed(() => drugStore.total)
    const drugInfoList = computed(() => drugStore.drugList)

    const showModal = ref<'Add'|'Edit'|'Delete'|null>(null)
    const edittingDrug = ref<Drug|null>(null)
    const deletingDrugID = ref<number>(0)

    // 加载药品方法
    async function loadDrug(keyword: string, option: UsageMethod|'') {
        await drugStore.fetchDrugs({
            keyword: keyword || undefined,
            usage_method: option || undefined
        })
    }

    // 打开弹窗方法
    const openModal = (modalName: 'Add'|'Edit'|'Delete') => {
        showModal.value = modalName
    }

    // 关闭弹窗方法
    const closeModal = (event?: Event) => {
        if (event) {
            if (event.target === event.currentTarget) {
                showModal.value = null
            }
            return
        }
        showModal.value = null
    }

    // 添加药品成功后的回调
    const handleAddSuccess = () => {
        drugStore.refreshDrugs()
    }

    // 添加药品方法 (打开添加面板)
    const addDrug = () => {
        openModal('Add')
    }

    // 编辑药品方法 (打开编辑面板)
    const editDrug = (id: number) => {
        drugInfoList.value.forEach((drug) => {
            if (drug.id === id) {
                edittingDrug.value = drug
            }
        })

        openModal('Edit')
    }

    // 提交编辑药品方法
    const confirmEditting = async (drug: Drug) => {
        const data: UpdateDrugRequest = {
            name: drug.name,
            image: drug.image || undefined,
            usage_method: drug.usage_method,
            dosage: drug.dosage,
            remaining: drug.remaining || undefined,
            source: drug.source,
            external_id: drug.external_id || undefined
        }

        try {
            await drugStore.editDrug(drug.id, data)
        } catch(error) {
            console.error(`更新药品失败,${error}`)
        } finally {
            closeModal()
        }
    }

    // 删除药品方法 (打开删除弹窗)
    const openDeleteDrug = (id: number) => {
        deletingDrugID.value = id
        openModal('Delete')
    }

    // 提交删除药品方法
    const confirmDelete = async () => {
        if (deletingDrugID.value === 0) return
        try {
            await drugStore.removeDrug(deletingDrugID.value)
        } catch(error) {
            console.error(`删除药品失败,${error}`)
        } finally {
            closeModal()
        }
    }

    // 药品搜索方法
    const handleSearch = async (
        searchKeyword: string,
        searchOption: UsageMethod|''
        ) => {
        try {
            await loadDrug(searchKeyword, searchOption)
        } catch(error) {
            console.log(error)
        }
    }

    // 挂载后自动加载药品
    drugStore.fetchDrugs()
</script>

<style scoped>
    .drug-management-container {
        position: relative;
        height: 100%;
        width: 100%;
        padding: 20px;
        display: flex;
        flex-direction: column;
    }

    .search-bar {
        width: 100%;
    }

    .drug-list {
        flex: 1;
        margin-top: 20px;
        overflow-y: hidden;
    }

    .modal-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(120, 120, 120, 0.5);
        z-index: 1000;
    }

    .modal {
        position: absolute;
        top: 25%;
        left: 25%;
        width: 50%;
        height: 50%;
        padding: 15px;
        background-color: #fff;
        border-radius: 24px;
        animation: zoomIn 0.35s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }

    .modal.drug-add {
        top: 10%;
        left: 10%;
        width: 80%;
        height: 80%;
        padding: 0;
    }

    @keyframes zoomIn {
        0% {
            opacity: 0;
            transform: scale(0.5);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
</style>