/**
 * 用户认证状态管理
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { login as loginApi, refreshAccessToken } from '@/api/auth'
import { getUserInfo, updateUserInfo as updateUserInfoApi } from '@/api/user'
import type { LoginRequest, LoginResponse } from '@/types/authTypes'
import type { UpdateUserInfoRequest } from '@/types/userTypes'

export const useUserStore = defineStore('user', () => {
    // 从localStorage中获取accessToken
    const accessToken = ref<string | null>(localStorage.getItem('access_token'))
    const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
    const nickname = ref<string>('')
    const email = ref<string>('')
    const imageUrl = ref<string>('')
    const userId = ref<number>(0)

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
        refreshToken.value = response.token.refresh_token
        localStorage.setItem('access_token', response.token.access_token)
        localStorage.setItem('refresh_token', response.token.refresh_token)

        // 保存用户信息
        nickname.value = response.nickname
        email.value = response.email

        // 登录后获取完整用户信息
        await fetchUserInfo()

        return response
    }

    /**
     * 登出方法
     */
    function logout() {
        // 清除token
        accessToken.value = null
        refreshToken.value = null
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')

        // 清除用户信息
        nickname.value = ''
        email.value = ''
        imageUrl.value = ''
        userId.value = 0
    }

    /**
     * 刷新token方法
     * @returns 刷新是否成功
     */
    async function refresh(): Promise<boolean> {
        if (!refreshToken.value) {
            return false
        }

        try {
            const response = await refreshAccessToken({ refresh_token: refreshToken.value })
            accessToken.value = response.access_token
            localStorage.setItem('access_token', response.access_token)
            return true
        } catch {
            return false
        }
    }

    /**
     * 获取用户信息
     * 从服务器获取完整的用户信息
     */
    async function fetchUserInfo(): Promise<void> {
        try {
            const userInfo = await getUserInfo()
            nickname.value = userInfo.nickname
            email.value = userInfo.email
            imageUrl.value = userInfo.avatar
        } catch (error) {
            console.error('获取用户信息失败:', error)
        }
    }

    /**
     * 更新用户信息
     * @param data 更新用户信息
     */
    async function updateUserInfo(data: UpdateUserInfoRequest): Promise<void> {
        const response = await updateUserInfoApi(data)
        nickname.value = response.nickname
        imageUrl.value = response.avatar
    }

    return {
        accessToken,
        nickname,
        email,
        imageUrl,
        userId,
        isLoggedIn,
        login,
        logout,
        refresh,
        fetchUserInfo,
        updateUserInfo
    }
})
