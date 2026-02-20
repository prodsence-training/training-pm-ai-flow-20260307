/**
 * Test data fixtures for E2E tests
 * 模擬 API 回應資料
 */

export const mockMetricsBasic = {
  totalIssueCount: 10,
  totalStoryPoints: 25.5,
  totalDoneItemCount: 4,
  doneStoryPoints: 12.5,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

export const mockMetricsEmpty = {
  totalIssueCount: 0,
  totalStoryPoints: 0,
  totalDoneItemCount: 0,
  doneStoryPoints: 0,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

export const mockMetricsAllStatuses = {
  totalIssueCount: 27,
  totalStoryPoints: 50.0,
  totalDoneItemCount: 8,
  doneStoryPoints: 27.0,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

export const mockStatusDistributionBasic = {
  distribution: [
    { status: 'Backlog', count: 2, percentage: 7.41 },
    { status: 'Evaluated', count: 1, percentage: 3.7 },
    { status: 'To Do', count: 3, percentage: 11.11 },
    { status: 'In Progress', count: 5, percentage: 18.52 },
    { status: 'Waiting', count: 2, percentage: 7.41 },
    { status: 'Ready to Verify', count: 4, percentage: 14.81 },
    { status: 'Done', count: 8, percentage: 29.63 },
    { status: 'Invalid', count: 1, percentage: 3.7 },
    { status: 'Routine', count: 1, percentage: 3.7 },
  ],
  totalIssueCount: 27,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

export const mockStatusDistributionEmpty = {
  distribution: [
    { status: 'Backlog', count: 0, percentage: 0 },
    { status: 'Evaluated', count: 0, percentage: 0 },
    { status: 'To Do', count: 0, percentage: 0 },
    { status: 'In Progress', count: 0, percentage: 0 },
    { status: 'Waiting', count: 0, percentage: 0 },
    { status: 'Ready to Verify', count: 0, percentage: 0 },
    { status: 'Done', count: 0, percentage: 0 },
    { status: 'Invalid', count: 0, percentage: 0 },
    { status: 'Routine', count: 0, percentage: 0 },
  ],
  totalIssueCount: 0,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

export const mockSprintsBasic = {
  options: ['All', 'Sprint 1', 'Sprint 2', 'Sprint 3', 'No Sprints'],
  totalSprints: 3,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

export const mockSprintsWithDuplicates = {
  options: [
    'All',
    'Sprint 1 (11)',
    'Sprint 1 (15)',
    'Sprint 2',
    'No Sprints',
  ],
  totalSprints: 4,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

export const mockSprintsEmpty = {
  options: ['All', 'No Sprints'],
  totalSprints: 0,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

// Sprint 1 篩選後的資料
export const mockMetricsSprint1 = {
  totalIssueCount: 3,
  totalStoryPoints: 10.5,
  totalDoneItemCount: 2,
  doneStoryPoints: 7.5,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

export const mockStatusDistributionSprint1 = {
  distribution: [
    { status: 'Backlog', count: 0, percentage: 0 },
    { status: 'Evaluated', count: 0, percentage: 0 },
    { status: 'To Do', count: 0, percentage: 0 },
    { status: 'In Progress', count: 1, percentage: 33.33 },
    { status: 'Waiting', count: 0, percentage: 0 },
    { status: 'Ready to Verify', count: 0, percentage: 0 },
    { status: 'Done', count: 2, percentage: 66.67 },
    { status: 'Invalid', count: 0, percentage: 0 },
    { status: 'Routine', count: 0, percentage: 0 },
  ],
  totalIssueCount: 3,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

// No Sprints 篩選後的資料
export const mockMetricsNoSprints = {
  totalIssueCount: 1,
  totalStoryPoints: 0,
  totalDoneItemCount: 1,
  doneStoryPoints: 0,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}

export const mockStatusDistributionNoSprints = {
  distribution: [
    { status: 'Backlog', count: 0, percentage: 0 },
    { status: 'Evaluated', count: 0, percentage: 0 },
    { status: 'To Do', count: 0, percentage: 0 },
    { status: 'In Progress', count: 0, percentage: 0 },
    { status: 'Waiting', count: 0, percentage: 0 },
    { status: 'Ready to Verify', count: 0, percentage: 0 },
    { status: 'Done', count: 1, percentage: 100 },
    { status: 'Invalid', count: 0, percentage: 0 },
    { status: 'Routine', count: 0, percentage: 0 },
  ],
  totalIssueCount: 1,
  timestamp: '2025-10-29T12:00:00.000Z',
  cacheHit: false,
}
