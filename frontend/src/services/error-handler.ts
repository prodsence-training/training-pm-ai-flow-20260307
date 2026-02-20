/**
 * Global Error Handler
 * 處理所有錯誤，轉換為用戶友善的訊息
 */

export interface ApiError {
  message: string
  status?: number
  isNetworkError: boolean
  isTimeoutError: boolean
  originalError?: Error
}

/**
 * 處理 API 錯誤
 * @param error 原始錯誤
 * @returns 標準化的錯誤訊息
 */
export function handleApiError(error: unknown): ApiError {
  // 網路錯誤
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return {
      message: '無法連接到伺服器。請檢查網路連接。',
      isNetworkError: true,
      isTimeoutError: false,
      originalError: error,
    }
  }

  // 超時錯誤
  if (error instanceof Error && error.name === 'AbortError') {
    return {
      message: '連接超時。請稍後重試。',
      isNetworkError: false,
      isTimeoutError: true,
      originalError: error,
    }
  }

  // HTTP 錯誤
  if (error instanceof Error) {
    const match = error.message.match(/status: (\d+)/)
    if (match) {
      const status = parseInt(match[1])
      let message = '伺服器發生錯誤。'

      switch (status) {
        case 400:
          message = '請求參數無效。'
          break
        case 404:
          message = '找不到請求的資源。'
          break
        case 500:
        case 502:
        case 503:
        case 504:
          message = '伺服器暫時無法使用。請稍後重試。'
          break
        default:
          message = `發生錯誤（狀態碼：${status}）`
      }

      return {
        message,
        status,
        isNetworkError: false,
        isTimeoutError: false,
        originalError: error,
      }
    }

    // 其他 Error 物件
    return {
      message: error.message || '發生未知錯誤。',
      isNetworkError: false,
      isTimeoutError: false,
      originalError: error,
    }
  }

  // 未知錯誤
  return {
    message: '發生未知錯誤。',
    isNetworkError: false,
    isTimeoutError: false,
  }
}

/**
 * 重試邏輯
 * @param fn 要執行的非同步函數
 * @param maxRetries 最大重試次數
 * @param delay 重試延遲（毫秒）
 * @returns 執行結果
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  let lastError: unknown

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error

      // 只重試某些類型的錯誤
      const apiError = handleApiError(error)
      if (!apiError.isNetworkError && !apiError.isTimeoutError) {
        // 如果不是網路或超時錯誤，立即拋出
        throw error
      }

      // 如果不是最後一次，等待後重試
      if (i < maxRetries - 1) {
        await new Promise((resolve) => setTimeout(resolve, delay * Math.pow(2, i)))
      }
    }
  }

  throw lastError
}

/**
 * 記錄錯誤
 * @param context 錯誤上下文
 * @param error 錯誤物件
 */
export function logError(context: string, error: unknown): void {
  if (process.env.NODE_ENV === 'development') {
    console.error(`[${context}]`, error)
  }

  // 可以在此添加遠端日誌記錄
  // 例如：sendToLoggingService(context, error)
}
