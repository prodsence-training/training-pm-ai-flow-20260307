/**
 * Unit tests for MetricCard component
 * 對應 tasks.md T026
 *
 * 測試目標：
 * - 測試組件正確渲染（title, value, icon）
 * - 測試響應式佈局
 * - 測試可選 unit 顯示
 * - 測試數值格式化（toLocaleString）
 */

import { render, screen } from '@testing-library/react'
import { MetricCard } from '@/components/MetricCard'

describe('MetricCard', () => {
  it('renders all props correctly', () => {
    render(
      <MetricCard
        title="Total Issues"
        value={42}
        icon="📊"
        unit="issues"
      />
    )

    // 驗證標題顯示
    expect(screen.getByText('Total Issues')).toBeInTheDocument()

    // 驗證數值顯示
    expect(screen.getByText('42')).toBeInTheDocument()

    // 驗證圖標顯示
    expect(screen.getByText('📊')).toBeInTheDocument()

    // 驗證單位顯示
    expect(screen.getByText('issues')).toBeInTheDocument()
  })

  it('renders without unit when unit is not provided', () => {
    render(
      <MetricCard
        title="Total Count"
        value={100}
        icon="🔢"
      />
    )

    expect(screen.getByText('Total Count')).toBeInTheDocument()
    expect(screen.getByText('100')).toBeInTheDocument()
    expect(screen.getByText('🔢')).toBeInTheDocument()

    // 驗證沒有 unit 文字
    expect(screen.queryByText(/points|issues|items/)).not.toBeInTheDocument()
  })

  it('formats numeric values with toLocaleString', () => {
    render(
      <MetricCard
        title="Large Number"
        value={1234567}
        icon="💯"
      />
    )

    // 驗證數值格式化（應該有千位分隔符）
    // toLocaleString() 會根據環境產生不同格式，這裡檢查數字存在即可
    expect(screen.getByText(/1.*234.*567/)).toBeInTheDocument()
  })

  it('displays decimal numbers correctly', () => {
    render(
      <MetricCard
        title="Story Points"
        value={25.5}
        icon="🎯"
        unit="points"
      />
    )

    expect(screen.getByText('Story Points')).toBeInTheDocument()
    expect(screen.getByText('25.5')).toBeInTheDocument()
    expect(screen.getByText('points')).toBeInTheDocument()
  })

  it('displays zero value correctly', () => {
    render(
      <MetricCard
        title="Done Items"
        value={0}
        icon="✅"
      />
    )

    expect(screen.getByText('Done Items')).toBeInTheDocument()
    expect(screen.getByText('0')).toBeInTheDocument()
  })

  it('handles string values', () => {
    render(
      <MetricCard
        title="Status"
        value="Active"
        icon="🟢"
      />
    )

    expect(screen.getByText('Status')).toBeInTheDocument()
    expect(screen.getByText('Active')).toBeInTheDocument()
  })

  it('applies correct CSS classes for styling', () => {
    const { container } = render(
      <MetricCard
        title="Test Card"
        value={123}
        icon="🧪"
      />
    )

    // 驗證卡片容器有正確的樣式類
    const card = container.firstChild as HTMLElement
    expect(card).toHaveClass('bg-white')
    expect(card).toHaveClass('rounded-lg')
    expect(card).toHaveClass('shadow-md')
    expect(card).toHaveClass('p-6')
  })

  it('displays title with correct styling', () => {
    render(
      <MetricCard
        title="My Metric"
        value={999}
        icon="📈"
      />
    )

    const title = screen.getByText('My Metric')
    expect(title).toHaveClass('text-sm')
    expect(title).toHaveClass('font-medium')
    expect(title).toHaveClass('text-gray-600')
  })

  it('displays value with correct styling (blue color)', () => {
    render(
      <MetricCard
        title="Metric"
        value={500}
        icon="💙"
      />
    )

    const value = screen.getByText('500')
    expect(value).toHaveClass('text-3xl')
    expect(value).toHaveClass('font-bold')
    expect(value).toHaveClass('text-blue-600')  // Blue theme (#3b82f6)
  })

  it('displays icon with correct size', () => {
    render(
      <MetricCard
        title="Icon Test"
        value={1}
        icon="🎨"
      />
    )

    const icon = screen.getByText('🎨')
    expect(icon).toHaveClass('text-4xl')
  })

  it('renders multiple cards with different values', () => {
    const { rerender } = render(
      <MetricCard
        title="Card 1"
        value={10}
        icon="1️⃣"
      />
    )

    expect(screen.getByText('Card 1')).toBeInTheDocument()
    expect(screen.getByText('10')).toBeInTheDocument()

    // 重新渲染不同的卡片
    rerender(
      <MetricCard
        title="Card 2"
        value={20}
        icon="2️⃣"
      />
    )

    expect(screen.getByText('Card 2')).toBeInTheDocument()
    expect(screen.getByText('20')).toBeInTheDocument()
  })

  it('handles very large numbers', () => {
    render(
      <MetricCard
        title="Big Number"
        value={999999999}
        icon="🚀"
      />
    )

    // 驗證大數字被正確渲染
    expect(screen.getByText(/999.*999.*999/)).toBeInTheDocument()
  })

  it('handles negative numbers', () => {
    render(
      <MetricCard
        title="Negative"
        value={-42}
        icon="➖"
      />
    )

    expect(screen.getByText('-42')).toBeInTheDocument()
  })

  it('maintains layout structure', () => {
    const { container } = render(
      <MetricCard
        title="Layout Test"
        value={100}
        icon="📐"
        unit="units"
      />
    )

    // 驗證 flex 佈局存在
    const flexContainer = container.querySelector('.flex.items-center.justify-between')
    expect(flexContainer).toBeInTheDocument()

    // 驗證內容區域和圖標區域分開
    const contentArea = container.querySelector('.flex-1')
    expect(contentArea).toBeInTheDocument()
  })
})
