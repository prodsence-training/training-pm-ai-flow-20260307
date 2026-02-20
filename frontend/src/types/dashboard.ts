/**
 * Dashboard 相關的 TypeScript 型別定義
 * 對應後端的資料模型
 */

// Issue 介面（對應 rawData 的 23 個欄位）
export interface Issue {
  // 核心識別 (索引 0-4)
  key: string // 0: Issue 唯一識別碼
  issueType: string // 1: 類型
  project: string // 2: 專案代碼
  summary: string // 3: Issue 標題
  parent: string | null // 4: 父級 Issue Key

  // 工作流程 (索引 5-7)
  status: string // 5: 當前狀態
  sprint: string | null // 6: Sprint 名稱
  dueDate: string | null // 7: 預計完成日期

  // 優先級與緊急度 (索引 8-9)
  priority: string // 8: 優先級等級
  urgency: string // 9: 緊急程度

  // 估算欄位 (索引 10-15)
  tSize: string // 10: T-Shirt 大小估算
  confidence: string // 11: 估算信心程度
  clients: string // 12: 相關客戶
  taskTags: string // 13: 任務標籤
  businessPoints: number // 14: 商業價值點數
  storyPoints: number // 15: 故事點數

  // 狀態追蹤 (索引 16-18)
  statusCategory: string // 16: 簡化狀態分類
  statusCategoryChanged: string | null // 17: 狀態變更時間戳
  timeSpent: number // 18: 實際花費時間（秒）

  // 時間軸 (索引 19-22)
  created: string // 19: Issue 建立時間
  updated: string // 20: 最後更新時間
  resolved: string | null // 21: 解決/完成時間
  projectName: string // 22: Jira 專案完整識別名稱
}

// Sprint 介面
export interface Sprint {
  boardId: number // A: 看板 ID
  boardName: string // B: 看板名稱
  sprintName: string // C: Sprint 名稱（用於篩選）
  sprintId: number // D: Sprint ID
  state: 'future' | 'active' | 'closed' // E: 當前狀態
  startDate: string // F: 開始日期
  endDate: string // G: 結束日期
  completeDate?: string // H: 完成日期（可選）
  goal: string // I: Sprint 目標
}

// 狀態分布介面
export interface StatusDistribution {
  status: string // 狀態名稱（9 個固定值之一）
  count: number // 該狀態的 Issue 數量
  percentage: number // 該狀態佔比（%）
}

// 指標卡片介面
export interface MetricCard {
  title: string // 卡片標題
  value: number | string // 統計數值
  icon: string // 圖標（emoji 或 SVG）
  unit?: string // 單位（可選）
}

// 儀表板指標介面
export interface DashboardMetrics {
  totalIssueCount: number // 指標 1: 總 Issue 數
  totalStoryPoints: number // 指標 2: 總故事點數
  totalDoneItemCount: number // 指標 3: 已完成 Issue 數
  doneStoryPoints: number // 指標 4: 已完成故事點數
}

// 固定狀態順序（不變）
export const FIXED_STATUSES = [
  'Backlog',
  'Evaluated',
  'To Do',
  'In Progress',
  'Waiting',
  'Ready to Verify',
  'Done',
  'Invalid',
  'Routine',
] as const

export type FixedStatus = typeof FIXED_STATUSES[number]

/**
 * 轉換函數: 將 CSV 列陣列轉換為 Issue 物件
 */
export function parseIssueFromRow(row: string[]): Issue {
  return {
    key: row[0] || '',
    issueType: row[1] || '',
    project: row[2] || '',
    summary: row[3] || '',
    parent: row[4] || null,
    status: row[5] || '',
    sprint: row[6] || null,
    dueDate: row[7] || null,
    priority: row[8] || '',
    urgency: row[9] || '',
    tSize: row[10] || '',
    confidence: row[11] || '',
    clients: row[12] || '',
    taskTags: row[13] || '',
    businessPoints: parseFloat(row[14]) || 0,
    storyPoints: parseFloat(row[15]) || 0, // 非數值轉 0
    statusCategory: row[16] || '',
    statusCategoryChanged: row[17] || null,
    timeSpent: parseInt(row[18]) || 0,
    created: row[19] || '',
    updated: row[20] || '',
    resolved: row[21] || null,
    projectName: row[22] || '',
  }
}

/**
 * 轉換為卡片顯示
 */
export function toMetricCards(metrics: DashboardMetrics): MetricCard[] {
  return [
    {
      title: 'Total Issue Count',
      value: metrics.totalIssueCount,
      icon: '📄',
    },
    {
      title: 'Total Story Points',
      value: metrics.totalStoryPoints.toFixed(2),
      icon: '🎯',
      unit: 'pts',
    },
    {
      title: 'Total Done Item Count',
      value: metrics.totalDoneItemCount,
      icon: '✓',
    },
    {
      title: 'Done Story Points',
      value: metrics.doneStoryPoints.toFixed(2),
      icon: '🕐',
      unit: 'pts',
    },
  ]
}
