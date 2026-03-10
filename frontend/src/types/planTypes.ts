/**
 * 计划模块类型定义
 */

// 计划类型
export type PlanType = '长期' | '周期'

// 用药频率类型
export type FrequencyType = 'daily' | 'alternate' | 'weekly' | 'monthly'

// 计划状态
export type PlanStatus = 'active' | 'paused' | 'completed'

// 频率详情类型
export interface FrequencyDetail {
    // 间隔天数（alternate类型）
    interval_days?: number
    // 星期几（weekly类型），1-7表示周一到周日
    weekdays?: number[]
    // 每月几号（monthly类型），1-31
    days_of_month?: number[]
}

// 计划药品关联信息
export interface PlanDrug {
    id: number
    plan_id: number
    drug_id: number
    dosage: string
    drug?: {
        id: number
        name: string
        usage_method: string
        image: string | null
    }
}

// 计划信息
export interface Plan {
    id: number
    user_id: number
    name: string
    plan_type: PlanType
    start_date: string
    end_date: string | null
    frequency_type: FrequencyType
    frequency_detail: FrequencyDetail | null
    time_points: string[]
    sms_enabled: boolean
    status: PlanStatus
    created_at: string
    updated_at: string
    drugs?: PlanDrug[]
}

// 创建计划请求
export interface CreatePlanRequest {
    name: string
    plan_type: PlanType
    start_date: string
    end_date?: string
    frequency_type: FrequencyType
    frequency_detail?: FrequencyDetail
    time_points: string[]
    sms_enabled?: boolean
    drug_ids: Array<{
        drug_id: number
        dosage: string
    }>
}

// 更新计划请求
export interface UpdatePlanRequest {
    name?: string
    plan_type?: PlanType
    start_date?: string
    end_date?: string
    frequency_type?: FrequencyType
    frequency_detail?: FrequencyDetail
    time_points?: string[]
    sms_enabled?: boolean
    status?: PlanStatus
    drug_ids?: Array<{
        drug_id: number
        dosage: string
    }>
}

// 计划列表查询参数
export interface PlanListParams {
    page?: number
    page_size?: number
    status?: PlanStatus
    plan_type?: PlanType
    keyword?: string
}

// 计划列表响应
export interface PlanListResponse {
    items: Plan[]
    total: number
    page: number
    page_size: number
}

// 今日计划响应
export interface TodayPlanResponse {
    date: string
    plans: Array<{
        plan: Plan
        time_point: string
        drugs: PlanDrug[]
        taken: boolean
        track_id?: number
    }>
}
