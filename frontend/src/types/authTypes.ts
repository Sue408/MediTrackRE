/**
 * 认证模块类型定义
 */

// 注册请求
export interface RegisterRequest {
    nickname: string
    email: string
    password: string
}

// 登录请求
export interface LoginRequest {
    email: string
    password: string
}

// Token刷新请求
export interface RefreshRequest {
    refresh_token: string
}

// Token响应
export interface TokenResponse {
    access_token: string
    refresh_token: string
    token_type: string
}

// 登录响应
export interface LoginResponse {
    nickname: string
    email: string
    created_at: string
    token: TokenResponse
}
