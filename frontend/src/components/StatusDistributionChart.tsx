'use client'

/**
 * StatusDistributionChart 元件
 * 使用 Recharts 顯示狀態分布長條圖（9 個固定狀態）
 */

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ComposedChart,
} from 'recharts'
import { StatusDistribution } from '@/types/dashboard'

interface StatusDistributionChartProps {
  data: StatusDistribution[]
  totalIssueCount: number
}

export function StatusDistributionChart({
  data,
  totalIssueCount,
}: StatusDistributionChartProps) {
  // 自訂 Tooltip
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const item = payload[0].payload
      return (
        <div className="bg-white p-3 border border-gray-200 rounded shadow-lg">
          <p className="font-medium text-gray-800">{item.status}</p>
          <p className="text-sm text-gray-600">
            Count: <span className="font-bold">{item.count}</span>
          </p>
          <p className="text-sm text-gray-600">
            Percentage: <span className="font-bold">{item.percentage.toFixed(1)}%</span>
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Status Distribution</h2>

      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 0, bottom: 80 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="status"
            type="category"
            angle={-45}
            textAnchor="end"
            height={100}
          />
          <YAxis type="number" />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="count" fill="#3b82f6" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill="#3b82f6" />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      <div className="mt-4 text-center text-sm text-gray-600">
        Total Issues: <span className="font-bold text-blue-600">{totalIssueCount}</span>
      </div>
    </div>
  )
}
