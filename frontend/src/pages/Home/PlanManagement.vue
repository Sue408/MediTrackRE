<template>
    <div class="plan-management-container">
        <!-- 顶部操作栏 -->
        <div class="top-bar">
            <TopBar @addPlan="openAddModal" :total="planStore.total"/>
        </div>

        <!-- 状态筛选栏 -->
        <div class="status-filter">
            <StatusFilter v-model="filterStatus" @update:modelValue="handleStatusChange" />
        </div>

        <!-- 计划列表视图 -->
        <div class="plan-list">
            <PlanList
                :plan-list="planStore.planList"
                @pause="handlePause"
                @resume="handleResume"
                @edit="openEditModal"
                @delete="openDeleteConfirm"
                @addPlan="openAddModal"
            />
        </div>

        <!-- 遮罩层 -->
        <div
            class="modal-container"
            :class="{show: showModal}"
            v-if="showModal && showModal !== 'Delete'"
            @click="closeModal"
        >
            <!-- 计划添加/编辑弹窗 -->
            <div class="modal plan-modal" v-if="showModal === 'Add' || showModal === 'Edit'">
                <PlanFormModal
                    :editing-plan="editingPlan"
                    @success="handleFormSuccess"
                    @close="closeModal"
                />
            </div>
        </div>

        <!-- 删除确认弹窗 -->
        <ConfirmModal
            :visible="showModal === 'Delete'"
            message="确定要删除该计划吗?"
            @cancel="closeModal"
            @confirm="confirmDelete"
        />
    </div>
</template>

<script setup lang="ts">
    import { ref, computed } from 'vue'
    import TopBar from '@/components/plan-management/TopBar.vue'
    import StatusFilter from '@/components/plan-management/StatusFilter.vue'
    import PlanList from '@/components/plan-management/PlanList.vue'
    import PlanFormModal from '@/components/plan-management/PlanFormModal.vue'
    import ConfirmModal from '@/components/common/ConfirmModal.vue'
    import { usePlanStore } from '@/stores/planStore'
    import type { Plan, PlanStatus } from '@/types/planTypes'

    // 使用计划 store
    const planStore = usePlanStore()

    // 弹窗状态
    const showModal = ref<'Add'|'Edit'|'Delete'|null>(null)
    const editingPlan = ref<Plan|null>(null)
    const deletingPlanID = ref<number>(0)

    // 状态筛选
    const filterStatus = ref<PlanStatus | ''>('')

    // 加载计划列表
    const loadPlans = async () => {
        await planStore.fetchPlans({
            status: filterStatus.value || undefined
        })
    }

    // 状态筛选变化
    const handleStatusChange = async (status: PlanStatus | '') => {
        filterStatus.value = status
        await planStore.filterByStatus(status)
    }

    // 打开添加弹窗
    const openAddModal = () => {
        editingPlan.value = null
        showModal.value = 'Add'
    }

    // 打开编辑弹窗
    const openEditModal = (plan: Plan) => {
        editingPlan.value = plan
        showModal.value = 'Edit'
    }

    // 打开删除确认弹窗
    const openDeleteConfirm = (plan: Plan) => {
        deletingPlanID.value = plan.id
        showModal.value = 'Delete'
    }

    // 关闭弹窗
    const closeModal = (event?: Event) => {
        if (event) {
            if (event.target === event.currentTarget) {
                showModal.value = null
                editingPlan.value = null
            }
            return
        }
        showModal.value = null
        editingPlan.value = null
    }

    // 表单提交成功回调
    const handleFormSuccess = () => {
        loadPlans()
    }

    // 暂停计划
    const handlePause = async (plan: Plan) => {
        try {
            await planStore.pause(plan.id)
        } catch (error) {
            console.error('暂停计划失败:', error)
        }
    }

    // 恢复计划
    const handleResume = async (plan: Plan) => {
        try {
            await planStore.resume(plan.id)
        } catch (error) {
            console.error('恢复计划失败:', error)
        }
    }

    // 确认删除
    const confirmDelete = async () => {
        if (deletingPlanID.value === 0) return
        try {
            await planStore.removePlan(deletingPlanID.value)
        } catch (error) {
            console.error('删除计划失败:', error)
        } finally {
            closeModal()
        }
    }

    // 挂载后自动加载计划
    planStore.fetchPlans()
</script>

<style scoped>
    .plan-management-container {
        position: relative;
        height: 100%;
        width: 100%;
        padding: 20px;
        display: flex;
        flex-direction: column;
    }

    .status-filter {
        width: 100%;
    }

    .plan-list {
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
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .modal.plan-modal {
        width: 80%;
        height: 80%;
        max-width: 900px;
        max-height: 600px;
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