/**
 * 计划API服务层
 */
import { http } from '@/request'
import type {
    Plan,
    CreatePlanRequest,
    UpdatePlanRequest,
    PlanListParams,
    PlanListResponse,
    TodayPlanResponse
} from '@/types/planTypes'

/**
 * 获取计划列表
 * GET /api/plans
 * @param params 查询参数
 */
export async function getPlanList(params?: PlanListParams): Promise<PlanListResponse> {
    return await http.get<PlanListResponse>('/plans', { params })
}

/**
 * 获取计划详情
 * GET /api/plans/:id
 * @param id 计划ID
 */
export async function getPlanDetail(id: number): Promise<Plan> {
    return await http.get<Plan>(`/plans/${id}`)
}

/**
 * 创建计划
 * POST /api/plans
 * @param data 计划信息
 */
export async function createPlan(data: CreatePlanRequest): Promise<Plan> {
    return await http.post<Plan>('/plans', data)
}

/**
 * 更新计划
 * PUT /api/plans/:id
 * @param id 计划ID
 * @param data 计划信息
 */
export async function updatePlan(id: number, data: UpdatePlanRequest): Promise<Plan> {
    return await http.put<Plan>(`/plans/${id}`, data)
}

/**
 * 删除计划
 * DELETE /api/plans/:id
 * @param id 计划ID
 */
export async function deletePlan(id: number): Promise<void> {
    return await http.delete<void>(`/plans/${id}`)
}

/**
 * 暂停计划
 * POST /api/plans/:id/pause
 * @param id 计划ID
 */
export async function pausePlan(id: number): Promise<Plan> {
    return await http.post<Plan>(`/plans/${id}/pause`)
}

/**
 * 恢复计划
 * POST /api/plans/:id/resume
 * @param id 计划ID
 */
export async function resumePlan(id: number): Promise<Plan> {
    return await http.post<Plan>(`/plans/${id}/resume`)
}

/**
 * 完成计划
 * POST /api/plans/:id/complete
 * @param id 计划ID
 */
export async function completePlan(id: number): Promise<Plan> {
    return await http.post<Plan>(`/plans/${id}/complete`)
}

/**
 * 获取今日计划
 * GET /api/plans/today
 */
export async function getTodayPlans(): Promise<TodayPlanResponse> {
    return await http.get<TodayPlanResponse>('/plans/today')
}

/**
 * 记录用药
 * POST /api/plans/:id/track
 * @param id 计划ID
 * @param time_point 用药时间点
 */
export async function trackMedication(id: number, time_point: string): Promise<{
    track_id: number
    created_at: string
}> {
    return await http.post<{
        track_id: number
        created_at: string
    }>(`/plans/${id}/track`, { time_point })
}

/**
 * 取消用药记录
 * DELETE /api/plans/:id/track/:track_id
 * @param id 计划ID
 * @param track_id 记录ID
 */
export async function untrackMedication(id: number, track_id: number): Promise<void> {
    return await http.delete<void>(`/plans/${id}/track/${track_id}`)
}