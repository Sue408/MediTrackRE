/**
 * 药品状态管理
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { getDrugList, createDrug, updateDrug, deleteDrug } from '@/api/drug'
import type { Drug, CreateDrugRequest, UpdateDrugRequest, DrugListParams } from '@/types/drugTypes'

export const useDrugStore = defineStore('drug', () => {
    // 药品列表数据
    const drugList = ref<Drug[]>([])
    // 药品总数
    const total = ref<number>(0)
    // 加载状态
    const loading = ref<boolean>(false)
    // 当前查询参数
    const currentParams = ref<DrugListParams>({})

    // 药品数量
    const drugCount = computed(() => drugList.value.length)

    // 用法类型统计
    const usageMethodCount = computed(() => {
        const methods = new Set(drugList.value.map(d => d.usage_method).filter(Boolean))
        return methods.size
    })

    // 顶部用法类型（使用频率最高的2个）
    const topMethods = computed(() => {
        const methodCounts: Record<string, number> = {}
        drugList.value.forEach(drug => {
            if (drug.usage_method) {
                methodCounts[drug.usage_method] = (methodCounts[drug.usage_method] || 0) + 1
            }
        })
        return Object.entries(methodCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 2)
            .map(([method]) => method)
    })

    /**
     * 获取药品列表
     * @param params 查询参数
     */
    async function fetchDrugs(params: DrugListParams = {}): Promise<void> {
        loading.value = true
        currentParams.value = params

        try {
            const res = await getDrugList({
                ...params
            })
            drugList.value = res.items || []
            total.value = res.total
        } catch (error) {
            console.error('获取药品列表失败:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    /**
     * 刷新药品列表（使用当前参数）
     */
    async function refreshDrugs(): Promise<void> {
        await fetchDrugs(currentParams.value)
    }

    /**
     * 添加药品
     * @param data 药品信息
     */
    async function addDrug(data: CreateDrugRequest): Promise<Drug> {
        const newDrug = await createDrug(data)
        await refreshDrugs()
        return newDrug
    }

    /**
     * 更新药品
     * @param id 药品ID
     * @param data 药品信息
     */
    async function editDrug(id: number, data: UpdateDrugRequest): Promise<Drug> {
        const updatedDrug = await updateDrug(id, data)
        await refreshDrugs()
        return updatedDrug
    }

    /**
     * 删除药品
     * @param id 药品ID
     */
    async function removeDrug(id: number): Promise<void> {
        await deleteDrug(id)
        await refreshDrugs()
    }

    return {
        drugList,
        total,
        loading,
        currentParams,
        drugCount,
        usageMethodCount,
        topMethods,
        fetchDrugs,
        refreshDrugs,
        addDrug,
        editDrug,
        removeDrug
    }
})