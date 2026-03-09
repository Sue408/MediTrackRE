/**
 * Axios客户端定义
 * http对象
 */
import axios, {type AxiosError, type AxiosRequestConfig } from 'axios'
import config from '@/config'
import router from '@/router'
import { useAuthStore } from '@/stores/authStore'

const anthStore = () => useAuthStore()

// 创建基础Axios实例对象
const request = axios.create(
    {
        baseURL: config.env === 'development' ? '/api' : config.apiBaseUrl,
        timeout: 150000,
        headers:
            {
                'Content-Type': 'application/json'
            }
    }
)

// 请求拦截器定义
request.interceptors.request.use(
    (config) => {
        // 自动获取访问token
        const token = localStorage.getItem('access_token')

        // 如果存在访问token则自动添加到请求头中
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`
        }

        return config
    },
    (error: AxiosError) => {
        // 抛出异常
        return Promise.reject(error)
    }
)

// 响应拦截器定义
request.interceptors.response.use(
    (response) => {
        return response
    },
    async (error: AxiosError) => {
        // 处理401未授权错误
        if (error.response?.status === 401) {
            // 获取当前路由路径
            const currentPath = window.location.pathname

            // 如果不在登录页
            if (currentPath !== '/auth') {
                // 尝试刷新token
                const refreshSuccess = await anthStore().refresh()

                if (refreshSuccess) {
                    // 刷新成功，重新发送请求
                    const originalRequest = error.config
                    if (originalRequest) {
                        const token = localStorage.getItem('access_token')
                        if (token && originalRequest.headers) {
                            originalRequest.headers.Authorization = `Bearer ${token}`
                        }
                        return request(originalRequest)
                    }
                }

                // 刷新失败，执行登出并跳转到登录页
                anthStore().logout()
                router.replace('/auth')
            }
        }

        return Promise.reject(error)
    }
)

// 泛型支持导出
export const http = {
    async get<T>(url: string, httpConfig?: AxiosRequestConfig): Promise<T> {
        const response = await request.get<T>(url, httpConfig)
        return response.data
    },
    async post<T>(url: string, httpData?: any, httpConfig?: AxiosRequestConfig): Promise<T> {
        const response = await request.post<T>(url, httpData, httpConfig)
        return response.data
    },
    async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
        const response = await request.put<T>(url, data, config)
        return response.data
    },
    async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
        const response = await request.delete<T>(url, config)
        return response.data
    }
}