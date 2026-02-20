/**
 * Dashboard API Client
 * 提供與後端 FastAPI 的通訊介面
 */
import { DashboardMetrics, StatusDistribution } from '@/types/dashboard'

// API 回應介面
export interface StatusDistributionResponse {
  distribution: StatusDistribution[]
  totalIssueCount: number
  timestamp: string
  cacheHit: boolean
}

export class DashboardApiClient {
  private baseUrl: string

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
  }

  /**
   * 取得儀表板指標
   * @param sprint Sprint 篩選條件（預設 "All"）
   * @returns DashboardMetrics
   */
  async getMetrics(sprint: string = 'All'): Promise<DashboardMetrics> {
    try {
      const url = `${this.baseUrl}/dashboard/metrics?sprint=${encodeURIComponent(sprint)}`
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(30000), // 30 秒超時
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('Failed to fetch metrics:', error)
      throw error
    }
  }

  /**
   * 取得狀態分布資料
   * @param sprint Sprint 篩選條件（預設 "All"）
   * @returns StatusDistributionResponse
   */
  async getStatusDistribution(sprint: string = 'All'): Promise<StatusDistributionResponse> {
    try {
      const url = `${this.baseUrl}/dashboard/status-distribution?sprint=${encodeURIComponent(sprint)}`
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(30000),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('Failed to fetch status distribution:', error)
      throw error
    }
  }

  /**
   * 取得 Sprint 選項列表
   * @returns string[] Sprint 選項
   */
  async getSprints(): Promise<string[]> {
    try {
      const url = `${this.baseUrl}/sprints`
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(30000),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data.options || []
    } catch (error) {
      console.error('Failed to fetch sprints:', error)
      throw error
    }
  }
}

// 全域 API Client 實例
export const apiClient = new DashboardApiClient()
