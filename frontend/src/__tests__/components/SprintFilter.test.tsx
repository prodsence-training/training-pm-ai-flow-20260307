/**
 * Unit tests for SprintFilter component
 * 對應 tasks.md T055
 *
 * 測試目標：
 * - 測試組件正確渲染選項
 * - 測試選項選擇和 callback 觸發
 * - 測試預設選擇
 * - 測試響應式佈局
 */

import { render, screen, fireEvent } from '@testing-library/react'
import { SprintFilter } from '@/components/SprintFilter'

describe('SprintFilter', () => {
  const mockOptions = ['All', 'Sprint 1', 'Sprint 2', 'Sprint 3', 'No Sprints']
  const mockOnSprintChange = jest.fn()

  beforeEach(() => {
    mockOnSprintChange.mockClear()
  })

  it('renders with all options', () => {
    render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="All"
        onSprintChange={mockOnSprintChange}
      />
    )

    // 驗證標籤顯示
    expect(screen.getByText('Sprint 篩選:')).toBeInTheDocument()

    // 驗證 select 元素存在
    const select = screen.getByRole('combobox')
    expect(select).toBeInTheDocument()

    // 驗證所有選項都存在
    mockOptions.forEach((option) => {
      expect(screen.getByRole('option', { name: option })).toBeInTheDocument()
    })
  })

  it('displays correct default selection', () => {
    render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="Sprint 1"
        onSprintChange={mockOnSprintChange}
      />
    )

    const select = screen.getByRole('combobox') as HTMLSelectElement
    expect(select.value).toBe('Sprint 1')
  })

  it('calls onSprintChange when selection changes', () => {
    render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="All"
        onSprintChange={mockOnSprintChange}
      />
    )

    const select = screen.getByRole('combobox')

    // 改變選擇
    fireEvent.change(select, { target: { value: 'Sprint 2' } })

    // 驗證 callback 被呼叫且參數正確
    expect(mockOnSprintChange).toHaveBeenCalledTimes(1)
    expect(mockOnSprintChange).toHaveBeenCalledWith('Sprint 2')
  })

  it('renders "All" option by default', () => {
    render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="All"
        onSprintChange={mockOnSprintChange}
      />
    )

    const allOption = screen.getByRole('option', { name: 'All' }) as HTMLOptionElement
    expect(allOption.selected).toBe(true)
  })

  it('renders "No Sprints" option', () => {
    render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="No Sprints"
        onSprintChange={mockOnSprintChange}
      />
    )

    const noSprintsOption = screen.getByRole('option', { name: 'No Sprints' }) as HTMLOptionElement
    expect(noSprintsOption).toBeInTheDocument()
    expect(noSprintsOption.selected).toBe(true)
  })

  it('handles empty options array', () => {
    render(
      <SprintFilter
        options={[]}
        selectedSprint=""
        onSprintChange={mockOnSprintChange}
      />
    )

    const select = screen.getByRole('combobox')
    expect(select).toBeInTheDocument()

    // 應該沒有選項
    const options = screen.queryAllByRole('option')
    expect(options).toHaveLength(0)
  })

  it('handles only "All" and "No Sprints" options (empty sprint data)', () => {
    const minimalOptions = ['All', 'No Sprints']

    render(
      <SprintFilter
        options={minimalOptions}
        selectedSprint="All"
        onSprintChange={mockOnSprintChange}
      />
    )

    expect(screen.getByRole('option', { name: 'All' })).toBeInTheDocument()
    expect(screen.getByRole('option', { name: 'No Sprints' })).toBeInTheDocument()

    const options = screen.getAllByRole('option')
    expect(options).toHaveLength(2)
  })

  it('handles sprint options with duplicate names (Sprint ID appended)', () => {
    const optionsWithDuplicates = [
      'All',
      'Sprint 1 (11)',
      'Sprint 1 (15)',
      'Sprint 2',
      'No Sprints'
    ]

    render(
      <SprintFilter
        options={optionsWithDuplicates}
        selectedSprint="Sprint 1 (11)"
        onSprintChange={mockOnSprintChange}
      />
    )

    expect(screen.getByRole('option', { name: 'Sprint 1 (11)' })).toBeInTheDocument()
    expect(screen.getByRole('option', { name: 'Sprint 1 (15)' })).toBeInTheDocument()
    expect(screen.getByRole('option', { name: 'Sprint 2' })).toBeInTheDocument()

    const select = screen.getByRole('combobox') as HTMLSelectElement
    expect(select.value).toBe('Sprint 1 (11)')
  })

  it('calls onSprintChange with correct value for duplicate sprint', () => {
    const optionsWithDuplicates = [
      'All',
      'Sprint 1 (11)',
      'Sprint 1 (15)',
      'No Sprints'
    ]

    render(
      <SprintFilter
        options={optionsWithDuplicates}
        selectedSprint="Sprint 1 (11)"
        onSprintChange={mockOnSprintChange}
      />
    )

    const select = screen.getByRole('combobox')
    fireEvent.change(select, { target: { value: 'Sprint 1 (15)' } })

    expect(mockOnSprintChange).toHaveBeenCalledWith('Sprint 1 (15)')
  })

  it('applies responsive CSS classes', () => {
    const { container } = render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="All"
        onSprintChange={mockOnSprintChange}
      />
    )

    const select = screen.getByRole('combobox')

    // 驗證響應式寬度類別（mobile: w-full, desktop: md:w-64）
    expect(select).toHaveClass('w-full')
    expect(select).toHaveClass('md:w-64')
  })

  it('applies blue theme styling (focus ring)', () => {
    render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="All"
        onSprintChange={mockOnSprintChange}
      />
    )

    const select = screen.getByRole('combobox')

    // 驗證藍色主題 focus 樣式
    expect(select).toHaveClass('focus:ring-blue-500')
    expect(select).toHaveClass('focus:border-blue-500')
  })

  it('has correct accessibility attributes', () => {
    render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="All"
        onSprintChange={mockOnSprintChange}
      />
    )

    const select = screen.getByRole('combobox')
    const label = screen.getByText('Sprint 篩選:')

    // 驗證 label 和 select 關聯
    expect(select).toHaveAttribute('id', 'sprint-filter')
    expect(label).toHaveAttribute('for', 'sprint-filter')
  })

  it('handles rapid selection changes', () => {
    render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="All"
        onSprintChange={mockOnSprintChange}
      />
    )

    const select = screen.getByRole('combobox')

    // 快速多次改變選擇
    fireEvent.change(select, { target: { value: 'Sprint 1' } })
    fireEvent.change(select, { target: { value: 'Sprint 2' } })
    fireEvent.change(select, { target: { value: 'Sprint 3' } })

    // 驗證每次都觸發 callback
    expect(mockOnSprintChange).toHaveBeenCalledTimes(3)
    expect(mockOnSprintChange).toHaveBeenNthCalledWith(1, 'Sprint 1')
    expect(mockOnSprintChange).toHaveBeenNthCalledWith(2, 'Sprint 2')
    expect(mockOnSprintChange).toHaveBeenNthCalledWith(3, 'Sprint 3')
  })

  it('maintains selection after re-render', () => {
    const { rerender } = render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="Sprint 1"
        onSprintChange={mockOnSprintChange}
      />
    )

    let select = screen.getByRole('combobox') as HTMLSelectElement
    expect(select.value).toBe('Sprint 1')

    // 重新渲染不同選擇
    rerender(
      <SprintFilter
        options={mockOptions}
        selectedSprint="Sprint 3"
        onSprintChange={mockOnSprintChange}
      />
    )

    select = screen.getByRole('combobox') as HTMLSelectElement
    expect(select.value).toBe('Sprint 3')
  })

  it('renders correct number of options', () => {
    render(
      <SprintFilter
        options={mockOptions}
        selectedSprint="All"
        onSprintChange={mockOnSprintChange}
      />
    )

    const options = screen.getAllByRole('option')
    expect(options).toHaveLength(mockOptions.length)
  })
})
