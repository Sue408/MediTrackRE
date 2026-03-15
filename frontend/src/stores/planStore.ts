/**
 * 计划状态管理
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { getPlanList, createPlan, updatePlan, deletePlan, pausePlan, resumePlan } from '@/api/plan'
import type { Plan, CreatePlanRequest, UpdatePlanRequest, PlanListParams, PlanStatus } from '@/types/planTypes'

export const usePlanStore = defineStore('plan', () => {
    // 计划列表数据
    const planList = ref<Plan[]>([])
    // 计划总数
    const total = ref<number>(0)
    // 加载状态
    const loading = ref<boolean>(false)
    // 当前查询参数
    const currentParams = ref<PlanListParams>({})

    // 计划数量
    const planCount = computed(() => planList.value.length)

    // 进行中数量
    const activeCount = computed(() => planList.value.filter(p => p.status === 'active').length)

    // 已暂停数量
    const pausedCount = computed(() => planList.value.filter(p => p.status === 'paused').length)

    // 已完成数量
    const completedCount = computed(() => planList.value.filter(p => p.status === 'completed').length)

    /**
     * 获取计划列表
     * @param params 查询参数
     */
    async function fetchPlans(params: PlanListParams = {}): Promise<void> {
        loading.value = true
        currentParams.value = params

        try {
            const res = await getPlanList({
                page: params.page || 1,
                page_size: params.page_size || 10,
                status: params.status,
                plan_type: params.plan_type,
                keyword: params.keyword
            })
            planList.value = res.items || []
            total.value = res.total
        } catch (error) {
            console.error('获取计划列表失败:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    /**
     * 刷新计划列表（使用当前参数）
     */
    async function refreshPlans(): Promise<void> {
        await fetchPlans(currentParams.value)
    }

    /**
     * 添加计划
     * @param data 计划信息
     */
    async function addPlan(data: CreatePlanRequest): Promise<Plan> {
        const newPlan = await createPlan(data)
        await refreshPlans()
        return newPlan
    }

    /**
     * 更新计划
     * @param id 计划ID
     * @param data 计划信息
     */
    async function editPlan(id: number, data: UpdatePlanRequest): Promise<Plan> {
        const updatedPlan = await updatePlan(id, data)
        await refreshPlans()
        return updatedPlan
    }

    /**
     * 删除计划
     * @param id 计划ID
     */
    async function removePlan(id: number): Promise<void> {
        await deletePlan(id)
        await refreshPlans()
    }

    /**
     * 暂停计划
     * @param id 计划ID
     */
    async function pause(id: number): Promise<Plan> {
        const result = await pausePlan(id)
        await refreshPlans()
        return result
    }

    /**
     * 恢复计划
     * @param id 计划ID
     */
    async function resume(id: number): Promise<Plan> {
        const result = await resumePlan(id)
        await refreshPlans()
        return result
    }

    /**
     * 按状态筛选
     * @param status 计划状态
     */
    async function filterByStatus(status: PlanStatus | ''): Promise<void> {
        await fetchPlans({
            ...currentParams.value,
            status: status || undefined
        })
    }

    return {
        planList,
        total,
        loading,
        currentParams,
        planCount,
        activeCount,
        pausedCount,
        completedCount,
        fetchPlans,
        refreshPlans,
        addPlan,
        editPlan,
        removePlan,
        pause,
        resume,
        filterByStatus
    }
})