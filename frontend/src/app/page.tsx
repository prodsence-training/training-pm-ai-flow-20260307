'use client'

/**
 * Dashboard 主頁面
 * 整合所有元件：Sprint 篩選器、指標卡片、狀態分布圖表
 */

import { LoadingSpinner } from '@/components/LoadingSpinner'
import { MetricsGrid } from '@/components/MetricsGrid'
import { StatusDistributionChart } from '@/components/StatusDistributionChart'
import { SprintFilter } from '@/components/SprintFilter'
import { EmptyState } from '@/components/EmptyState'
import { useDashboardData } from '@/hooks/useDashboardData'
import { useSprintFilter } from '@/hooks/useSprintFilter'

export default function DashboardPage() {
  // Sprint 篩選狀態
  const {
    options: sprintOptions,
    selectedSprint,
    setSelectedSprint,
    isLoading: sprintLoading,
  } = useSprintFilter()

  // Dashboard 資料
  const {
    metrics,
    statusDistribution,
    totalIssueCount,
    isLoading: dataLoading,
    error,
  } = useDashboardData(selectedSprint)

  // 顯示載入狀態
  if (dataLoading || sprintLoading) {
    return <LoadingSpinner isLoading={true} />
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto p-6">
        {/* 標題 */}
        <h1 className="text-3xl font-bold mb-6 text-blue-600">
          Jira Dashboard MVP v1.0
        </h1>

        {/* 錯誤訊息 */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            <p className="font-medium">錯誤</p>
            <p>{error}</p>
          </div>
        )}

        {/* Sprint 篩選器 */}
        <SprintFilter
          options={sprintOptions}
          selectedSprint={selectedSprint}
          onSprintChange={setSelectedSprint}
        />

        {/* 指標卡片 */}
        {metrics ? (
          <>
            <MetricsGrid metrics={metrics} />

            {/* 狀態分布圖表 */}
            {statusDistribution && statusDistribution.length > 0 ? (
              <StatusDistributionChart
                data={statusDistribution}
                totalIssueCount={totalIssueCount}
              />
            ) : (
              <EmptyState message="沒有狀態分布資料" />
            )}
          </>
        ) : (
          <EmptyState />
        )}
      </div>
    </main>
  )
}
