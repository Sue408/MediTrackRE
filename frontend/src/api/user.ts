/**
 * 用户API服务层
 */
import { http } from '@/request'
import type { UserInfoResponse, UpdateUserInfoRequest } from '@/types/userTypes'

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