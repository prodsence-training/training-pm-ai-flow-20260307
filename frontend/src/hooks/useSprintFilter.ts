'use client'

/**
 * useSprintFilter Hook
 * 管理 Sprint 篩選選項和狀態
 */

import { useEffect, useState } from 'react'
import { apiClient } from '@/services/api'

interface SprintFilterData {
  options: string[]
  selectedSprint: string
  setSelectedSprint: (sprint: string) => void
  isLoading: boolean
  error: string | null
}

export function useSprintFilter(): SprintFilterData {
  const [options, setOptions] = useState<string[]>(['All'])
  const [selectedSprint, setSelectedSprint] = useState<string>('All')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchSprintOptions() {
      try {
        setIsLoading(true)
        setError(null)

        const sprints = await apiClient.getSprints()
        setOptions(sprints)
      } catch (err) {
        console.error('Failed to fetch sprint options:', err)
        setError(err instanceof Error ? err.message : '載入 Sprint 選項失敗')
        // 保留預設選項
        setOptions(['All'])
      } finally {
        setIsLoading(false)
      }
    }

    fetchSprintOptions()
  }, [])

  return {
    options,
    selectedSprint,
    setSelectedSprint,
    isLoading,
    error,
  }
}
