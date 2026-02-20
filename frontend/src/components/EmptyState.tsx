'use client'

/**
 * EmptyState 元件
 * 當沒有資料時顯示的友善訊息
 */

interface EmptyStateProps {
  message?: string
}

export function EmptyState({ message = '目前沒有可用資料' }: EmptyStateProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-12 text-center">
      <div className="text-6xl mb-4">📊</div>
      <p className="text-xl text-gray-600">{message}</p>
    </div>
  )
}
