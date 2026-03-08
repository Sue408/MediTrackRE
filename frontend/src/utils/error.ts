/**
 * 错误处理工具函数
 */

/**
 * 从错误对象中提取友好的错误信息
 * @param error 错误对象
 * @returns 格式化的错误信息
 */
export function extractErrorMessage(error: unknown): string {
  // 如果不是错误对象，直接转换为字符串
  if (!(error instanceof Error)) {
    return String(error)
  }

  // 尝试获取响应对象中的 detail 信息
  const httpError = error as { response?: { data?: { detail?: string } } }

  if (httpError.response?.data?.detail) {
    return httpError.response.data.detail
  }

  // 如果没有 response 属性，说明是网络错误，直接返回 error.message
  if (!('response' in error)) {
    return error.message
  }

  // 其他情况返回默认错误信息
  return '操作失败，请稍后重试'
}