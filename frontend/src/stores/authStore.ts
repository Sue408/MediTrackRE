/**
 * 用户认证状态管理
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { login as loginApi, refreshToken } from '@/api/auth'
import type { LoginRequest, LoginResponse } from '@/types/authTypes'

export const useAuthStore = defineStore('auth', () => {
    // 从localStorage中获取accessToken
    const accessToken = ref<string | null>(localStorage.getItem('access_token'))
    const refreshTokenValue = ref<string | null>(localStorage.getItem('refresh_token'))
    const nickname = ref<string>('')
    const email = ref<string>('')
    const imageUrl = ref<string>('')

    // 计算属性：是否已登录
    const isLoggedIn = computed(() => !!accessToken.value)

    /**
     * 登录方法
     * @param data 登录信息
     * @returns 登录响应
     */
    async function login(data: LoginRequest): Promise<LoginResponse> {
        const response = await loginApi(data)

        // 保存token到localStorage
        accessToken.value = response.token.access_token
        refreshTokenValue.value = response.token.refresh_token
        localStorage.setItem('access_token', response.token.access_token)
        localStorage.setItem('refresh_token', response.token.refresh_token)

        // 保存用户信息
        nickname.value = response.nickname
        email.value = response.email

        return response
    }

    /**
     * 登出方法
     */
    function logout() {
        // 清除token
        accessToken.value = null
        refreshTokenValue.value = null
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')

        // 清除用户信息
        nickname.value = ''
        email.value = ''
        imageUrl.value = ''
    }

    /**
     * 刷新token方法
     */
    async function refresh(): Promise<void> {
        if (!refreshTokenValue.value) {
            logout()
            return
        }

        try {
            const response = await refreshToken({ refresh_token: refreshTokenValue.value })
            accessToken.value = response.access_token
            localStorage.setItem('access_token', response.access_token)
        } catch {
            logout()
        }
    }

    return {
        accessToken,
        nickname,
        email,
        imageUrl,
        isLoggedIn,
        login,
        logout,
        refresh
    }
})
