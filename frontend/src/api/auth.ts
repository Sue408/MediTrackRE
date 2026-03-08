/**
 * 认证API服务层
 */
import { http } from '@/request'
import type { RegisterRequest, LoginRequest, RefreshRequest, LoginResponse, TokenResponse } from '@/types/authTypes'

/**
 * 用户注册接口
 * POST /api/auth/register
 * @param data 注册信息
 */
export async function register(data: RegisterRequest): Promise<void> {
    return await http.post<void>('/auth/register', data)
}

/**
 * 用户登录接口
 * POST /api/auth/login
 * @param data 登录信息
 * @returns 登录响应包含用户信息和token
 */
export async function login(data: LoginRequest): Promise<LoginResponse> {
    return await http.post<LoginResponse>('/auth/login', data)
}

/**
 * 刷新Token接口
 * POST /api/auth/refresh
 * @param data 刷新token请求
 * @returns 新的token响应
 */
export async function refreshToken(data: RefreshRequest): Promise<TokenResponse> {
    return await http.post<TokenResponse>('/auth/refresh', data)
}
