/**
 * 药品模块类型定义
 */

// 用法类型
export type UsageMethod = '口服' | '注射' | '外用' | '含服' | '吸入' | '滴入' | '其他'

// 来源类型
export type DrugSource = '医疗数据库' | '手动输入'

// 药品信息
export interface Drug {
    id: number
    user_id: number
    name: string
    image: string | null
    usage_method: UsageMethod
    dosage: string
    remaining: string | null
    source: DrugSource
    external_id: number | null
    created_at: string
    updated_at: string
}

// 创建药品请求
export interface CreateDrugRequest {
    name: string
    image?: string
    usage_method: UsageMethod
    dosage: string
    remaining?: string
    source: DrugSource
    external_id?: number
}

// 更新药品请求
export interface UpdateDrugRequest {
    name?: string
    image?: string
    usage_method?: UsageMethod
    dosage?: string
    remaining?: string
    source?: DrugSource
    external_id?: number
}

// 药品列表查询参数
export interface DrugListParams {
    keyword?: string
    usage_method?: UsageMethod
    source?: DrugSource
}

// 药品列表响应
export interface DrugListResponse {
    items: Drug[]
    total: number
}
