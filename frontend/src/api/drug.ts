/**
 * 药品API服务层
 */
import { http } from '@/request'
import type {
    Drug,
    CreateDrugRequest,
    UpdateDrugRequest,
    DrugListParams,
    DrugListResponse
} from '@/types/drugTypes'

/**
 * 获取药品列表
 * GET /api/drugs
 * @param params 查询参数
 */
export async function getDrugList(params?: DrugListParams): Promise<DrugListResponse> {
    return await http.get<DrugListResponse>('/drugs', { params })
}

/**
 * 获取药品详情
 * GET /api/drugs/:id
 * @param id 药品ID
 */
export async function getDrugDetail(id: number): Promise<Drug> {
    return await http.get<Drug>(`/drugs/${id}`)
}

/**
 * 创建药品
 * POST /api/drugs
 * @param data 药品信息
 */
export async function createDrug(data: CreateDrugRequest): Promise<Drug> {
    return await http.post<Drug>('/drugs', data)
}

/**
 * 更新药品
 * PUT /api/drugs/:id
 * @param id 药品ID
 * @param data 药品信息
 */
export async function updateDrug(id: number, data: UpdateDrugRequest): Promise<Drug> {
    return await http.put<Drug>(`/drugs/${id}`, data)
}

/**
 * 删除药品
 * DELETE /api/drugs/:id
 * @param id 药品ID
 */
export async function deleteDrug(id: number): Promise<void> {
    return await http.delete<void>(`/drugs/${id}`)
}

/**
 * 搜索药品（从外部数据库搜索）
 * GET /api/drugs/search
 * @param keyword 搜索关键词
 */
export async function searchExternalDrugs(keyword: string): Promise<Array<Drug>> {
    return await http.get<Array<Drug>>('/drugs/search', { params: { keyword } })
}