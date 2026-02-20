'use client'

/**
 * useDashboardData Hook
 * 管理儀表板資料的取得和狀態
 */

import { useEffect, useState } from 'react'
import { apiClient } from '@/services/api'
import { DashboardMetrics, StatusDistribution } from '@/types/dashboard'

interface DashboardData {
  metrics: DashboardMetrics | null
  statusDistribution: StatusDistribution[] | null
  totalIssueCount: number
  isLoading: boolean
  error: string | null
}

export function useDashboardData(selectedSprint: string): DashboardData {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null)
  const [statusDistribution, setStatusDistribution] = useState<StatusDistribution[] | null>(
    null
  )
  const [totalIssueCount, setTotalIssueCount] = useState<number>(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true)
        setError(null)

        // 並行請求所有 API 端點
        const [metricsRes, distributionRes] = await Promise.all([
          apiClient.getMetrics(selectedSprint),
          apiClient.getStatusDistribution(selectedSprint),
        ])

        setMetrics(metricsRes)
        setStatusDistribution(distributionRes.distribution)
        setTotalIssueCount(distributionRes.totalIssueCount)
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err)
        setError(err instanceof Error ? err.message : '載入資料失敗')
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [selectedSprint])

  return {
    metrics,
    statusDistribution,
    totalIssueCount,
    isLoading,
    error,
  }
}
