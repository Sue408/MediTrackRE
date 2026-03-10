/**
 * 用户模块类型定义
 */

// 用户信息响应
export interface UserInfoResponse {
    nickname: string
    email: string
    avatar: string
    created_at: string
}

// 更新用户信息请求
export interface UpdateUserInfoRequest {
    nickname?: string
    avatar?: string
}

// ==================== 健康档案相关类型 ====================

// 性别类型
export type Gender = '男' | '女' | 'unknown'

// 血型类型
export type BloodType = 'A' | 'B' | 'AB' | 'O' | 'unknown'

// 女性特殊状态
export type SpecialStatus = '备孕' | '怀孕' | '哺乳' | null

// 过敏史项目
export interface AllergyItem {
    name: string
    reaction: string
}

// 疾病史项目
export interface DiseaseItem {
    name: string
    diagnosed_at: string
    status: string
}

// 健康档案响应
export interface ProfileResponse {
    id: number
    user_id: number
    gender: Gender
    height: number | null
    weight: number | null
    blood_type: BloodType
    allergies: AllergyItem[]
    diseases: DiseaseItem[]
    special_status: SpecialStatus
    created_at: string
    updated_at: string
}

// 更新健康档案请求
export interface UpdateProfileRequest {
    gender?: Gender
    height?: number | null
    weight?: number | null
    blood_type?: BloodType
    allergies?: AllergyItem[]
    diseases?: DiseaseItem[]
    special_status?: SpecialStatus
}

// ==================== 安全中心相关类型 ====================

// 修改密码请求
export interface ChangePasswordRequest {
    old_password: string
    new_password: string
    confirm_password: string
}