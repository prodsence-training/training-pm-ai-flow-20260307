# Data Model: Jira Dashboard MVP v1.0

**Date**: 2025-10-29 | **Phase**: Phase 1 - Design & Contracts

---

## 核心實體定義

### Issue 實體

**來源**: Google Sheets `rawData` 工作表（23 欄位 A:W）

**TypeScript 類型定義**:

```typescript
// frontend/src/types/dashboard.ts

/**
 * Issue 表示 Jira 系統中的單一工作項目
 * 資料來源: rawData 表的一列（索引 0-22）
 */
export interface Issue {
  // 核心識別 (索引 0-4)
  key: string;              // 0: Issue 唯一識別碼 (e.g., "IHAIC-1")
  issueType: string;        // 1: 類型 (e.g., "Story", "Bug", "Task")
  project: string;          // 2: 專案代碼 (e.g., "IHAIC")
  summary: string;          // 3: Issue 標題
  parent: string | null;    // 4: 父級 Issue Key（階層關係）

  // 工作流程 (索引 5-7)
  status: string;           // 5: 當前狀態（9 個預定義值之一）
  sprint: string | null;    // 6: Sprint 名稱或空值
  dueDate: string | null;   // 7: 預計完成日期 (ISO 8601)

  // 優先級與緊急度 (索引 8-9)
  priority: string;         // 8: 優先級等級
  urgency: string;          // 9: 緊急程度

  // 估算欄位 (索引 10-15)
  tSize: string;            // 10: T-Shirt 大小估算
  confidence: string;       // 11: 估算信心程度
  clients: string;          // 12: 相關客戶
  taskTags: string;         // 13: 任務標籤
  businessPoints: number;   // 14: 商業價值點數
  storyPoints: number;      // 15: 故事點數（支援小數，非數值視為 0）

  // 狀態追蹤 (索引 16-18)
  statusCategory: string;   // 16: 簡化狀態分類 (To Do / In Progress / Done)
  statusCategoryChanged: string | null;  // 17: 狀態變更時間戳
  timeSpent: number;        // 18: 實際花費時間（秒）

  // 時間軸 (索引 19-22)
  created: string;          // 19: Issue 建立時間
  updated: string;          // 20: 最後更新時間
  resolved: string | null;  // 21: 解決/完成時間
  projectName: string;      // 22: Jira 專案完整識別名稱
}

/**
 * 轉換函數: 將 CSV 列陣列轉換為 Issue 物件
 * 依賴: table-schema.md rawData 欄位順序
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
    storyPoints: parseFloat(row[15]) || 0,  // 非數值轉 0
    statusCategory: row[16] || '',
    statusCategoryChanged: row[17] || null,
    timeSpent: parseInt(row[18]) || 0,
    created: row[19] || '',
    updated: row[20] || '',
    resolved: row[21] || null,
    projectName: row[22] || '',
  };
}

/**
 * 驗證 Issue 物件的有效性
 */
export function validateIssue(issue: Issue): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  // 必填欄位檢查
  if (!issue.key) errors.push('Issue Key is required');
  if (!issue.status) errors.push('Status is required');

  // Status 值驗證（9 個預定義狀態之一，或允許無效值以滿足 FR-031）
  const validStatuses = [
    'Backlog', 'Evaluated', 'To Do', 'In Progress',
    'Waiting', 'Ready to Verify', 'Done', 'Invalid', 'Routine'
  ];
  // 注: 無效狀態允許（在狀態分布圖中排除），但在指標計算中計入

  return {
    valid: errors.length === 0,
    errors,
  };
}
```

**Python 模型定義**:

```python
# backend/src/models/issue.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Issue:
    """
    Issue 表示 Jira 系統中的單一工作項目
    資料來源: rawData 表的一列（索引 0-22）
    """

    # 核心識別 (索引 0-4)
    key: str                      # 0: Issue 唯一識別碼
    issue_type: str               # 1: 類型
    project: str                  # 2: 專案代碼
    summary: str                  # 3: Issue 標題
    parent: Optional[str] = None  # 4: 父級 Issue Key

    # 工作流程 (索引 5-7)
    status: str = ""              # 5: 當前狀態
    sprint: Optional[str] = None  # 6: Sprint 名稱
    due_date: Optional[str] = None  # 7: 預計完成日期

    # 優先級與緊急度 (索引 8-9)
    priority: str = ""            # 8: 優先級等級
    urgency: str = ""             # 9: 緊急程度

    # 估算欄位 (索引 10-15)
    t_size: str = ""              # 10: T-Shirt 大小
    confidence: str = ""          # 11: 估算信心程度
    clients: str = ""             # 12: 相關客戶
    task_tags: str = ""           # 13: 任務標籤
    business_points: float = 0.0  # 14: 商業價值點數
    story_points: float = 0.0     # 15: 故事點數

    # 狀態追蹤 (索引 16-18)
    status_category: str = ""     # 16: 簡化狀態分類
    status_category_changed: Optional[str] = None  # 17: 狀態變更時間
    time_spent: int = 0           # 18: 實際花費時間（秒）

    # 時間軸 (索引 19-22)
    created: str = ""             # 19: Issue 建立時間
    updated: str = ""             # 20: 最後更新時間
    resolved: Optional[str] = None  # 21: 解決時間
    project_name: str = ""        # 22: Jira 專案識別名稱

    @staticmethod
    def from_row(row: list) -> 'Issue':
        """從 CSV 列陣列轉換為 Issue 物件"""
        try:
            business_points = float(row[14]) if row[14] else 0.0
        except (ValueError, TypeError):
            business_points = 0.0

        try:
            story_points = float(row[15]) if row[15] else 0.0
        except (ValueError, TypeError):
            story_points = 0.0  # 非數值視為 0 (FR-032)

        try:
            time_spent = int(row[18]) if row[18] else 0
        except (ValueError, TypeError):
            time_spent = 0

        return Issue(
            key=row[0] or '',
            issue_type=row[1] or '',
            project=row[2] or '',
            summary=row[3] or '',
            parent=row[4] if row[4] else None,
            status=row[5] or '',
            sprint=row[6] if row[6] else None,
            due_date=row[7] if row[7] else None,
            priority=row[8] or '',
            urgency=row[9] or '',
            t_size=row[10] or '',
            confidence=row[11] or '',
            clients=row[12] or '',
            task_tags=row[13] or '',
            business_points=business_points,
            story_points=story_points,
            status_category=row[16] or '',
            status_category_changed=row[17] if row[17] else None,
            time_spent=time_spent,
            created=row[19] or '',
            updated=row[20] or '',
            resolved=row[21] if row[21] else None,
            project_name=row[22] or '',
        )

    def is_done(self) -> bool:
        """檢查 Issue 是否完成"""
        return self.status == 'Done'

    def has_valid_status(self) -> bool:
        """檢查 Status 是否在 9 個預定義值內"""
        valid_statuses = {
            'Backlog', 'Evaluated', 'To Do', 'In Progress',
            'Waiting', 'Ready to Verify', 'Done', 'Invalid', 'Routine'
        }
        return self.status in valid_statuses
```

### StatusDistribution 實體

**用途**: 表示 Issue 在各狀態的分布情況

```typescript
// frontend/src/types/dashboard.ts

export interface StatusDistribution {
  status: string;        // 狀態名稱（9 個固定值之一）
  count: number;         // 該狀態的 Issue 數量
  percentage: number;    // 該狀態佔比（%）
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
] as const;

export type FixedStatus = typeof FIXED_STATUSES[number];
```

```python
# backend/src/models/metric.py

from dataclasses import dataclass

@dataclass
class StatusDistribution:
    """表示 Issue 在各狀態的分布情況"""

    status: str          # 狀態名稱
    count: int           # Issue 數量
    percentage: float    # 佔比百分比

FIXED_STATUSES = [
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
```

### MetricCard 實體

**用途**: 表示儀表板上的統計卡片（4 種）

```typescript
// frontend/src/types/dashboard.ts

export interface MetricCard {
  title: string;          // 卡片標題 (e.g., "Total Issue Count")
  value: number | string; // 統計數值
  icon: string;           // 圖標（emoji 或 SVG）
  unit?: string;          // 單位 (可選)
}

export interface DashboardMetrics {
  totalIssueCount: number;      // 指標 1: 總 Issue 數
  totalStoryPoints: number;     // 指標 2: 總故事點數（支援小數）
  totalDoneItemCount: number;   // 指標 3: 已完成 Issue 數
  doneStoryPoints: number;      // 指標 4: 已完成故事點數
}

// 轉換為卡片顯示
export function toMetricCards(metrics: DashboardMetrics): MetricCard[] {
  return [
    {
      title: 'Total Issue Count',
      value: metrics.totalIssueCount,
      icon: '📄',
    },
    {
      title: 'Total Story Points',
      value: metrics.totalStoryPoints.toFixed(1),
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
      value: metrics.doneStoryPoints.toFixed(1),
      icon: '🕐',
      unit: 'pts',
    },
  ];
}
```

```python
# backend/src/models/metric.py

from dataclasses import dataclass

@dataclass
class DashboardMetrics:
    """表示儀表板四個統計卡片的數據"""

    total_issue_count: int        # 指標 1: 總 Issue 數（包含所有記錄）
    total_story_points: float     # 指標 2: 總故事點數（支援小數）
    total_done_item_count: int    # 指標 3: 已完成 Issue 數
    done_story_points: float      # 指標 4: 已完成故事點數
```

### Sprint 實體

**來源**: Google Sheets `GetJiraSprintValues` 工作表（9 欄位 A:I）

```typescript
// frontend/src/types/dashboard.ts

export interface Sprint {
  boardId: number;           // A: 看板 ID
  boardName: string;         // B: 看板名稱
  sprintName: string;        // C: Sprint 名稱（用於篩選）
  sprintId: number;          // D: Sprint ID
  state: 'future' | 'active' | 'closed';  // E: 當前狀態
  startDate: string;         // F: 開始日期
  endDate: string;           // G: 結束日期
  completeDate?: string;     // H: 完成日期（可選）
  goal: string;              // I: Sprint 目標
}
```

```python
# backend/src/models/sprint.py

from dataclasses import dataclass
from typing import Optional
from enum import Enum

class SprintState(str, Enum):
    """Sprint 生命週期狀態"""
    FUTURE = 'future'      # 未來計劃
    ACTIVE = 'active'      # 進行中
    CLOSED = 'closed'      # 已結束

@dataclass
class Sprint:
    """表示 GetJiraSprintValues 工作表的一列"""

    board_id: int                    # A: 看板 ID
    board_name: str                  # B: 看板名稱
    sprint_name: str                 # C: Sprint 名稱（用於篩選）
    sprint_id: int                   # D: Sprint ID
    state: SprintState               # E: 當前狀態
    start_date: str                  # F: 開始日期
    end_date: str                    # G: 結束日期
    complete_date: Optional[str] = None  # H: 完成日期
    goal: str = ""                   # I: Sprint 目標

    @staticmethod
    def from_row(row: list) -> 'Sprint':
        """從 CSV 列陣列轉換為 Sprint 物件"""
        return Sprint(
            board_id=int(row[0]) if row[0] else 0,
            board_name=row[1] or '',
            sprint_name=row[2] or '',
            sprint_id=int(row[3]) if row[3] else 0,
            state=SprintState(row[4]) if row[4] in ['future', 'active', 'closed'] else SprintState.FUTURE,
            start_date=row[5] or '',
            end_date=row[6] or '',
            complete_date=row[7] if row[7] else None,
            goal=row[8] or '',
        )
```

---

## 資料驗證規則

### Issue 驗證

```typescript
// frontend/src/types/dashboard.ts

export function validateIssue(issue: Issue): ValidationResult {
  const errors: string[] = [];

  // 必填欄位
  if (!issue.key?.trim()) {
    errors.push('Issue Key 必填');
  }

  // Story Points 非數值驗證（應已在解析時處理為 0）
  if (typeof issue.storyPoints !== 'number' || isNaN(issue.storyPoints)) {
    errors.push('Story Points 必須為數值');
  }

  // Status 驗證（允許無效值，但在分布圖中排除）
  // 無強制驗證 - 所有值都被接受

  return {
    valid: errors.length === 0,
    errors,
  };
}
```

### Sprint 驗證

```python
# backend/src/models/sprint.py

@dataclass
class SprintValidator:
    """Sprint 資料驗證"""

    @staticmethod
    def validate(sprint: Sprint) -> list[str]:
        """驗證 Sprint 物件"""
        errors = []

        # 必填欄位
        if not sprint.sprint_name:
            errors.append('Sprint Name is required')
        if not sprint.sprint_id:
            errors.append('Sprint ID is required')

        return errors
```

---

## 資料關聯與映射

### Issue → Sprint 映射

```
Issue.sprint (string) === Sprint.sprint_name (string)
```

**邏輯**:
- rawData 的 `sprint` 欄位（索引 6）存放 Sprint Name
- GetJiraSprintValues 的 `sprint_name` 欄位（Column C）用於匹配
- "No Sprints" 篩選顯示空 `sprint` 欄位的 Issue

### 狀態分布計算流程

```
Raw Issues (CSV 列)
    ↓ [parseIssueFromRow]
Issue Objects
    ↓ [filterBySprint]
Filtered Issues
    ↓ [groupByStatus]
StatusDistribution[]
    ↓ [calculatePercentage]
Metric Display
```

---

## 資料型別映射表

### CSV → TypeScript 型別轉換

| rawData 欄位 | 索引 | CSV 類型 | TypeScript 型別 | 空值處理 |
|-------------|------|---------|-----------------|---------|
| Key | 0 | string | string | '' |
| Issue Type | 1 | string | string | '' |
| Projects | 2 | string | string | '' |
| Summary | 3 | string | string | '' |
| parent | 4 | string | string \| null | null |
| Status | 5 | string | string | '' |
| Sprint | 6 | string | string \| null | null |
| Due date | 7 | date | string \| null | null |
| Priority | 8 | string | string | '' |
| Urgency | 9 | string | string | '' |
| T-Size | 10 | string | string | '' |
| Confidence | 11 | string | string | '' |
| Clients | 12 | string | string | '' |
| TaskTags | 13 | string | string | '' |
| BusinessPoints | 14 | number | number | 0 |
| Story Points | 15 | number | number | 0 (非數值時) |
| Status Category | 16 | string | string | '' |
| Status Category Changed | 17 | datetime | string \| null | null |
| Time Spent | 18 | number | number | 0 |
| Created | 19 | datetime | string | '' |
| Updated | 20 | datetime | string | '' |
| Resolved | 21 | datetime | string \| null | null |
| Project.name | 22 | string | string | '' |

### CSV → Python 型別轉換

| 欄位 | CSV 類型 | Python 型別 | 空值處理 |
|-----|---------|-----------|---------|
| 字串欄位 | string | str | '' |
| 數值欄位（BusinessPoints, Story Points, Time Spent） | number | float / int | 0 (非數值時) |
| 日期欄位 | datetime | str | None |
| 可選欄位（parent, Sprint, Due date 等） | any | Optional[str] | None |

---

## 狀態轉換流程

### Issue 工作流程狀態

```
Backlog → Evaluated → To Do → In Progress → Waiting → Ready to Verify → Done
             ↓
          Invalid (特殊狀態)

Routine (例行作業，可能出現在任何階段)
```

**在系統中的使用**:
1. **指標計算**: 計算 `status == 'Done'` 的 Issue
2. **狀態分布**: 顯示所有 9 個狀態的計數（包括 Invalid 和 Routine）
3. **無效狀態處理**: 不在 9 個預定義值內的狀態
   - 在 `totalIssueCount` 中計入
   - 在 `statusDistribution` 圖表中排除（FR-031）

### Sprint 生命週期狀態

```
future → active → closed
```

**在系統中的使用**:
- 顯示在 Sprint 篩選器中
- 用於時程管理（startDate → endDate → completeDate）

---

## 相關文件

- [table-schema.md](../../docs/table-schema.md) - Google Sheets 欄位定義
- [spec.md](./spec.md) - 功能需求與驗收標準
- [API 契約](./contracts/api-endpoints.md) - 資料交換格式

