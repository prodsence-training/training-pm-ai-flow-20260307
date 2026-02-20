'use client'

/**
 * MetricsGrid 元件
 * 顯示 4 個指標卡片的網格佈局
 */

import { DashboardMetrics, toMetricCards } from '@/types/dashboard'
import { MetricCard } from './MetricCard'

interface MetricsGridProps {
  metrics: DashboardMetrics
}

export function MetricsGrid({ metrics }: MetricsGridProps) {
  const cards = toMetricCards(metrics)

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {cards.map((card, index) => (
        <MetricCard
          key={index}
          title={card.title}
          value={card.value}
          icon={card.icon}
          unit={card.unit}
        />
      ))}
    </div>
  )
}
