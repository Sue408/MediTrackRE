/**
 * 用户API服务层
 */
import { http } from '@/request'
import type {
    UserInfoResponse,
    UpdateUserInfoRequest,
    ProfileResponse,
    UpdateProfileRequest,
    ChangePasswordRequest
} from '@/types/userTypes'

/**
 * 获取当前用户信息
 * GET /api/user/info
 * @returns 用户信息
 */
export async function getUserInfo(): Promise<UserInfoResponse> {
    return await http.get<UserInfoResponse>('/user/info')
}

/**
 * 更新用户信息
 * PUT /api/user/info
 * @param data 更新用户信息请求
 * @returns 更新后的用户信息
 */
export async function updateUserInfo(data: UpdateUserInfoRequest): Promise<UserInfoResponse> {
    return await http.put<UserInfoResponse>('/user/info', data)
}

/**
 * 获取健康档案
 * GET /api/user/profile
 * @returns 健康档案信息
 */
export async function getProfile(): Promise<ProfileResponse> {
    return await http.get<ProfileResponse>('/user/profile')
}

/**
 * 更新健康档案
 * PUT /api/user/profile
 * @param data 更新健康档案请求
 * @returns 更新后的健康档案
 */
export async function updateProfile(data: UpdateProfileRequest): Promise<ProfileResponse> {
    return await http.put<ProfileResponse>('/user/profile', data)
}

/**
 * 修改密码
 * POST /api/user/change-password
 * @param data 修改密码请求
 */
export async function changePassword(data: ChangePasswordRequest): Promise<void> {
    return await http.post<void>('/user/change-password', data)
}