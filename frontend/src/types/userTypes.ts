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