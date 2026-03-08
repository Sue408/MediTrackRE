// 前端配置对象 - 统一进行环境变量管理
// 定义配置对象接口
export interface AppConfig {
    apiBaseUrl: string, // 后端API基础地址
    env: string  // 前端运行环境 (development / product)
}

// 实例化配置对象并导出
const config: AppConfig = {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api',
    env: import.meta.env.MODE || 'development'
}
export default config