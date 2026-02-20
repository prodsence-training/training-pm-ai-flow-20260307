'use client'

/**
 * MetricCard 元件
 * 顯示單一指標卡片（包含圖標、標題、數值、單位）
 */

import { MetricCard as MetricCardType } from '@/types/dashboard'

export function MetricCard({ title, value, icon, unit }: MetricCardType) {
  // 格式化數值（如果是小數，顯示 2 位小數；如果是整數，直接顯示）
  const formatValue = (val: number | string) => {
    if (typeof val !== 'number') return val
    // 如果有小數位，格式化為 2 位小數
    if (!Number.isInteger(val)) {
      return val.toFixed(2)
    }
    return val.toString()
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-2">{title}</p>
          <div className="flex items-baseline gap-2">
            <p className="text-3xl font-bold text-blue-600">
              {formatValue(value)}
            </p>
            {unit && <span className="text-sm text-gray-500">{unit}</span>}
          </div>
        </div>
        <div className="text-4xl ml-4">{icon}</div>
      </div>
    </div>
  )
}
