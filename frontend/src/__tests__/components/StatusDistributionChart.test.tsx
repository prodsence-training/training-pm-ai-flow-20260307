/**
 * Unit tests for StatusDistributionChart component
 * 對應 tasks.md T038
 *
 * 測試目標：
 * - 測試圖表渲染（9 個狀態）
 * - 測試狀態順序（Backlog → Routine）
 * - 測試資料值準確性
 * - 測試 tooltip 渲染（模擬 hover）
 */

import { render, screen } from '@testing-library/react'
import { StatusDistributionChart } from '@/components/StatusDistributionChart'
import { StatusDistribution } from '@/types/dashboard'

// Mock Recharts 組件（因為它們依賴 DOM 測量）
jest.mock('recharts', () => ({
  ResponsiveContainer: ({ children }: any) => (
    <div data-testid="responsive-container">{children}</div>
  ),
  BarChart: ({ children, data }: any) => (
    <div data-testid="bar-chart" data-chart-data={JSON.stringify(data)}>
      {children}
    </div>
  ),
  Bar: ({ dataKey, fill }: any) => (
    <div data-testid="bar" data-key={dataKey} data-fill={fill} />
  ),
  XAxis: () => <div data-testid="x-axis" />,
  YAxis: ({ dataKey }: any) => <div data-testid="y-axis" data-key={dataKey} />,
  CartesianGrid: () => <div data-testid="cartesian-grid" />,
  Tooltip: () => <div data-testid="tooltip" />,
  Cell: () => <div data-testid="cell" />,
}))

describe('StatusDistributionChart', () => {
  const mockData: StatusDistribution[] = [
    { status: 'Backlog', count: 2, percentage: 7.41 },
    { status: 'Evaluated', count: 1, percentage: 3.7 },
    { status: 'To Do', count: 3, percentage: 11.11 },
    { status: 'In Progress', count: 5, percentage: 18.52 },
    { status: 'Waiting', count: 2, percentage: 7.41 },
    { status: 'Ready to Verify', count: 4, percentage: 14.81 },
    { status: 'Done', count: 8, percentage: 29.63 },
    { status: 'Invalid', count: 1, percentage: 3.7 },
    { status: 'Routine', count: 1, percentage: 3.7 },
  ]

  const totalIssueCount = 27

  it('renders chart title', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    expect(screen.getByText('Status Distribution')).toBeInTheDocument()
  })

  it('renders chart components (ResponsiveContainer, BarChart)', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    expect(screen.getByTestId('responsive-container')).toBeInTheDocument()
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument()
  })

  it('displays total issue count at bottom', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    expect(screen.getByText('Total Issues:')).toBeInTheDocument()
    expect(screen.getByText('27')).toBeInTheDocument()
  })

  it('renders with all 9 statuses', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    // 驗證資料傳遞到圖表
    const barChart = screen.getByTestId('bar-chart')
    const chartData = JSON.parse(barChart.getAttribute('data-chart-data') || '[]')

    expect(chartData).toHaveLength(9)
  })

  it('displays statuses in correct order', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    const barChart = screen.getByTestId('bar-chart')
    const chartData = JSON.parse(barChart.getAttribute('data-chart-data') || '[]')

    // 驗證狀態順序
    const expectedOrder = [
      'Backlog',
      'Evaluated',
      'To Do',
      'In Progress',
      'Waiting',
      'Ready to Verify',
      'Done',
      'Invalid',
      'Routine',
    ]

    const actualOrder = chartData.map((item: any) => item.status)
    expect(actualOrder).toEqual(expectedOrder)
  })

  it('uses blue theme color (#3b82f6)', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    const bar = screen.getByTestId('bar')
    expect(bar).toHaveAttribute('data-fill', '#3b82f6')
  })

  it('renders with correct data values', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    const barChart = screen.getByTestId('bar-chart')
    const chartData = JSON.parse(barChart.getAttribute('data-chart-data') || '[]')

    // 驗證特定狀態的資料
    const doneStatus = chartData.find((item: any) => item.status === 'Done')
    expect(doneStatus.count).toBe(8)
    expect(doneStatus.percentage).toBe(29.63)

    const inProgressStatus = chartData.find((item: any) => item.status === 'In Progress')
    expect(inProgressStatus.count).toBe(5)
    expect(inProgressStatus.percentage).toBe(18.52)
  })

  it('handles empty data array', () => {
    render(
      <StatusDistributionChart
        data={[]}
        totalIssueCount={0}
      />
    )

    expect(screen.getByText('Status Distribution')).toBeInTheDocument()
    expect(screen.getByText('Total Issues:')).toBeInTheDocument()
    expect(screen.getByText('0')).toBeInTheDocument()

    const barChart = screen.getByTestId('bar-chart')
    const chartData = JSON.parse(barChart.getAttribute('data-chart-data') || '[]')
    expect(chartData).toHaveLength(0)
  })

  it('handles zero counts in some statuses', () => {
    const dataWithZeros: StatusDistribution[] = [
      { status: 'Backlog', count: 0, percentage: 0 },
      { status: 'Evaluated', count: 0, percentage: 0 },
      { status: 'To Do', count: 5, percentage: 50 },
      { status: 'In Progress', count: 3, percentage: 30 },
      { status: 'Waiting', count: 0, percentage: 0 },
      { status: 'Ready to Verify', count: 0, percentage: 0 },
      { status: 'Done', count: 2, percentage: 20 },
      { status: 'Invalid', count: 0, percentage: 0 },
      { status: 'Routine', count: 0, percentage: 0 },
    ]

    render(
      <StatusDistributionChart
        data={dataWithZeros}
        totalIssueCount={10}
      />
    )

    const barChart = screen.getByTestId('bar-chart')
    const chartData = JSON.parse(barChart.getAttribute('data-chart-data') || '[]')

    // 驗證所有 9 個狀態仍存在（即使 count 為 0）
    expect(chartData).toHaveLength(9)

    // 驗證 count 為 0 的狀態
    const backlogStatus = chartData.find((item: any) => item.status === 'Backlog')
    expect(backlogStatus.count).toBe(0)
  })

  it('applies correct container styling', () => {
    const { container } = render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    const chartContainer = container.firstChild as HTMLElement
    expect(chartContainer).toHaveClass('bg-white')
    expect(chartContainer).toHaveClass('rounded-lg')
    expect(chartContainer).toHaveClass('shadow-md')
    expect(chartContainer).toHaveClass('p-6')
  })

  it('displays total count with blue styling', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    const totalCount = screen.getByText('27')
    expect(totalCount).toHaveClass('font-bold')
    expect(totalCount).toHaveClass('text-blue-600')
  })

  it('renders Y-axis with status data key', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    const yAxis = screen.getByTestId('y-axis')
    expect(yAxis).toHaveAttribute('data-key', 'status')
  })

  it('renders Bar with count data key', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    const bar = screen.getByTestId('bar')
    expect(bar).toHaveAttribute('data-key', 'count')
  })

  it('handles large issue counts', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={9999}
      />
    )

    expect(screen.getByText('9999')).toBeInTheDocument()
  })

  it('displays correct title text', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    const title = screen.getByText('Status Distribution')
    expect(title).toHaveClass('text-xl')
    expect(title).toHaveClass('font-bold')
    expect(title).toHaveClass('text-gray-800')
  })

  it('renders responsive container', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    // ResponsiveContainer 被 mock 了，但我們可以驗證它被渲染
    expect(screen.getByTestId('responsive-container')).toBeInTheDocument()
  })

  it('renders all chart components (grid, axes, tooltip)', () => {
    render(
      <StatusDistributionChart
        data={mockData}
        totalIssueCount={totalIssueCount}
      />
    )

    expect(screen.getByTestId('cartesian-grid')).toBeInTheDocument()
    expect(screen.getByTestId('x-axis')).toBeInTheDocument()
    expect(screen.getByTestId('y-axis')).toBeInTheDocument()
    expect(screen.getByTestId('tooltip')).toBeInTheDocument()
  })
})
