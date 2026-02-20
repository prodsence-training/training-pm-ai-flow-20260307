'use client'

/**
 * SprintFilter 元件
 * Sprint 篩選下拉選單
 */

interface SprintFilterProps {
  options: string[]
  selectedSprint: string
  onSprintChange: (sprint: string) => void
}

export function SprintFilter({
  options,
  selectedSprint,
  onSprintChange,
}: SprintFilterProps) {
  return (
    <div className="mb-6">
      <label
        htmlFor="sprint-filter"
        className="block text-sm font-medium text-gray-700 mb-2"
      >
        Sprint 篩選:
      </label>
      <select
        id="sprint-filter"
        value={selectedSprint}
        onChange={(e) => onSprintChange(e.target.value)}
        className="block w-full md:w-64 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-white"
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  )
}
