# Research: Jira Dashboard MVP v1.0 Implementation

**Date**: 2025-10-29 | **Phase**: Phase 0 - Research & Technical Analysis

## Overview

本文件詳細記錄 Jira Dashboard MVP v1.0 實作過程中的研究發現、技術選型決策及解決方案。所有研究基於 spec.md、tech-overview.md 和 table-schema.md 的規格要求進行。

---

## 1. Google Sheets CSV API 整合策略

### Decision: Public CSV Export URL (無需 API 金鑰)

**選型**:
- ✅ Google Sheets 公開分享的 CSV 匯出 URL
- ❌ 不使用 Google Sheets API（需要 OAuth2 認證）
- ❌ 不使用直接 HTTP 請求（複雜度高）

**理由**:
1. **簡化部署**: 無需維護 API 金鑰、OAuth2 流程、服務帳戶認證
2. **MVP 特性**: 專案已是公開分享，直接使用 CSV 匯出即可
3. **零管理成本**: 不涉及 API 配額、速率限制複雜度
4. **一致性**: spec.md FR-020 已明確規定「無需 API 金鑰」

**實作方案**:
```python
# Google Sheets CSV export URL format
BASE_URL = "https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

# Example:
# rawData sheet: gid=0
# GetJiraSprintValues sheet: gid=1234567

# 後端使用 httpx 或 requests 庫直接下載 CSV
async def fetch_google_sheets_csv(sheet_id: str, gid: int) -> str:
    url = f"{BASE_URL.format(SHEET_ID=sheet_id, GID=gid)}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30)
    return response.text
```

**優缺點分析**:

| 優點 | 缺點 |
|-----|-----|
| 無認證複雜度 | 公開連結失效需要手動更新 |
| CSV 格式易解析 | 無法寫入資料 |
| 降低部署風險 | 大量請求可能被限流 |
| 完全免費 | 無實時協作支援 |

---

## 2. 5 分鐘 TTL In-Memory 快取實現

### Decision: 簡單 TTL 快取 + 後台預取

**選型**:
- ✅ In-memory TTL cache（5 分鐘）
- ⚠️ 異步後台重新整理（可選）
- ❌ 不使用 Redis（增加部署複雜度）
- ❌ 不使用 Database cache（超過 MVP 範疇）

**理由**:
1. **效能與簡化平衡**: 5 分鐘快取足以滿足 50 個並發使用者
2. **MVP 特性**: 無需複雜分散式快取
3. **符合規格**: spec.md FR-021 明確要求 5 分鐘快取
4. **無狀態設計**: 便於容器化部署（無狀態 Pod）

**實作方案**:

```python
# FastAPI + Python 實現
from datetime import datetime, timedelta
from typing import Optional, Any

class CacheService:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self.cache: dict[str, tuple[Any, datetime]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None

        data, timestamp = self.cache[key]
        if datetime.utcnow() - timestamp > timedelta(seconds=self.ttl_seconds):
            del self.cache[key]
            return None

        return data

    def set(self, key: str, value: Any) -> None:
        self.cache[key] = (value, datetime.utcnow())

    def clear(self, key: str = None) -> None:
        if key:
            self.cache.pop(key, None)
        else:
            self.cache.clear()

# 使用方式
cache_service = CacheService(ttl_seconds=300)  # 5 minutes

@app.get("/api/dashboard/metrics")
async def get_metrics(sprint_filter: str = "All") -> MetricsResponse:
    cache_key = f"metrics:{sprint_filter}"

    # 檢查快取
    cached_data = cache_service.get(cache_key)
    if cached_data:
        return cached_data

    # 計算指標
    raw_data = await fetch_and_parse_google_sheets()
    metrics = calculate_metrics(raw_data, sprint_filter)

    # 儲存到快取
    cache_service.set(cache_key, metrics)

    return metrics
```

**快取策略**:

| 鍵名 | TTL | 更新觸發 |
|-----|-----|---------|
| `metrics:All` | 5 min | 定時或手動清除 |
| `metrics:{SprintName}` | 5 min | 定時或手動清除 |
| `status-distribution:All` | 5 min | 定時或手動清除 |
| `sprints:list` | 5 min | 定時或手動清除 |

**限制與假設**:
1. **單一進程限制**: 如果後端水平擴展（多個 Pod），每個 Pod 有獨立快取
2. **解決方案**: 使用分散式快取（Redis）或接受短期資料不一致
3. **MVP 決策**: 假設單一後端實例（Docker Compose 運行環境）

---

## 3. 原始 23 欄位資料轉換為指標計算

### Decision: 直接索引存取 + Pandas 轉換

**選型**:
- ✅ 使用 `row[index]` 模式存取 rawData（按規格要求）
- ✅ Pandas DataFrame 用於批量計算
- ❌ 不使用欄位名稱依賴（容易出錯）
- ❌ 不嘗試修改 schema（嚴格限制）

**理由**:
1. **遵守規格**: spec.md FR-007 要求使用 `row[index]` 模式
2. **資料安全**: 避免欄位對應錯誤導致的計算偏差
3. **效能**: Pandas 優化的向量化操作
4. **教育價值**: 展示 "Vibe Coding" 下的嚴格約束開發

**實作方案**:

```python
import pandas as pd
from typing import List, Dict

class DataProcessor:
    # rawData 欄位索引（0-based）
    FIELD_KEY = 0           # Issue Key
    FIELD_ISSUE_TYPE = 1    # Issue Type
    FIELD_PROJECT = 2       # Projects
    FIELD_SUMMARY = 3       # Summary
    FIELD_PARENT = 4        # parent
    FIELD_STATUS = 5        # Status
    FIELD_SPRINT = 6        # Sprint
    FIELD_DUE_DATE = 7      # Due date
    FIELD_PRIORITY = 8      # Priority
    FIELD_URGENCY = 9       # Urgency
    FIELD_T_SIZE = 10       # T-Size
    FIELD_CONFIDENCE = 11   # Confidence
    FIELD_CLIENTS = 12      # Clients
    FIELD_TASK_TAGS = 13    # TaskTags
    FIELD_BUSINESS_POINTS = 14  # BusinessPoints
    FIELD_STORY_POINTS = 15     # Story Points
    FIELD_STATUS_CATEGORY = 16  # Status Category
    FIELD_STATUS_CATEGORY_CHANGED = 17  # Status Category Changed
    FIELD_TIME_SPENT = 18   # Time Spent
    FIELD_CREATED = 19      # Created
    FIELD_UPDATED = 20      # Updated
    FIELD_RESOLVED = 21     # Resolved
    FIELD_PROJECT_NAME = 22 # Project.name

    # 固定 9 個狀態順序
    FIXED_STATUSES = [
        'Backlog', 'Evaluated', 'To Do', 'In Progress',
        'Waiting', 'Ready to Verify', 'Done', 'Invalid', 'Routine'
    ]

    def parse_csv(self, csv_content: str) -> pd.DataFrame:
        """解析 Google Sheets CSV 為 DataFrame"""
        df = pd.read_csv(StringIO(csv_content))
        # 僅保留前 23 列 (A:W)
        df = df.iloc[:, :23]
        return df

    def calculate_metrics(self, df: pd.DataFrame, sprint_filter: str = "All") -> Dict:
        """計算 4 個指標卡片"""

        # 應用 Sprint 篩選
        if sprint_filter != "All":
            df = self._filter_by_sprint(df, sprint_filter)

        # 處理 Story Points：非數值視為 0
        df['story_points_numeric'] = pd.to_numeric(
            df.iloc[:, self.FIELD_STORY_POINTS],
            errors='coerce'
        ).fillna(0)

        # 指標 1: Total Issue Count（包含所有記錄，即使 Status 無效）
        total_issues = len(df)

        # 指標 2: Total Story Points（包含所有記錄）
        total_story_points = df['story_points_numeric'].sum()

        # 指標 3: Total Done Item Count
        done_count = len(df[df.iloc[:, self.FIELD_STATUS] == 'Done'])

        # 指標 4: Done Story Points
        done_df = df[df.iloc[:, self.FIELD_STATUS] == 'Done']
        done_story_points = done_df['story_points_numeric'].sum()

        return {
            'totalIssueCount': int(total_issues),
            'totalStoryPoints': float(total_story_points),
            'totalDoneItemCount': int(done_count),
            'doneStoryPoints': float(done_story_points)
        }

    def calculate_status_distribution(self, df: pd.DataFrame, sprint_filter: str = "All") -> List[Dict]:
        """計算狀態分布（只顯示 9 個固定狀態）"""

        # 應用 Sprint 篩選
        if sprint_filter != "All":
            df = self._filter_by_sprint(df, sprint_filter)

        total_issues = len(df)
        distribution = []

        for status in self.FIXED_STATUSES:
            count = len(df[df.iloc[:, self.FIELD_STATUS] == status])
            percentage = (count / total_issues * 100) if total_issues > 0 else 0

            distribution.append({
                'status': status,
                'count': int(count),
                'percentage': round(percentage, 2)
            })

        return distribution

    def _filter_by_sprint(self, df: pd.DataFrame, sprint_name: str) -> pd.DataFrame:
        """按 Sprint Name 篩選"""
        if sprint_name == "No Sprints":
            # 篩選空 Sprint 欄位
            return df[df.iloc[:, self.FIELD_SPRINT].isna() |
                     (df.iloc[:, self.FIELD_SPRINT] == '')]
        else:
            # 篩選指定 Sprint Name
            return df[df.iloc[:, self.FIELD_SPRINT] == sprint_name]
```

**邊界情況處理**:

| 情況 | 處理方式 | 依據 |
|-----|--------|------|
| Story Points 非數值 | 視為 0 | FR-032 |
| Status 無效值 | 計入 Issue 計數，排除於狀態分布圖 | FR-031 |
| 空 Sprint 欄位 | 透過 "No Sprints" 篩選顯示 | FR-018 |
| CSV 解析失敗 | 返回快取資料或空回應 | FR-024 |

---

## 4. 載入指示器實作（慢速網路處理）

### Decision: 持續顯示 Spinner，無超時限制

**選型**:
- ✅ 持續顯示 Loading Spinner（無超時）
- ❌ 不實作超時機制
- ❌ 不顯示「取消」按鈕（完全依賴使用者耐心）

**理由**:
1. **規格要求**: spec.md FR-034 明確要求「持續顯示直到完成」
2. **使用者友善**: 即使 5 秒仍是顯示載入狀態（比無反應更好）
3. **邊界情況**: SC-006 要求 5 秒內回應，但不硬性超時

**實作方案 (React/Next.js)**:

```typescript
// frontend/src/components/LoadingSpinner.tsx
'use client';

import { useEffect, useState } from 'react';

interface LoadingSpinnerProps {
  isLoading: boolean;
}

export function LoadingSpinner({ isLoading }: LoadingSpinnerProps) {
  return isLoading ? (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center">
        <div className="inline-block animate-spin">
          <svg
            className="w-12 h-12 text-blue-500"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        </div>
        <p className="mt-4 text-gray-600">正在載入儀表板...</p>
      </div>
    </div>
  ) : null;
}

// frontend/src/hooks/useDashboardData.ts
'use client';

import { useEffect, useState } from 'react';

export function useDashboardData(selectedSprint: string) {
  const [metrics, setMetrics] = useState(null);
  const [statusDistribution, setStatusDistribution] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        setError(null);

        // 並行請求所有 API 端點
        const [metricsRes, distributionRes] = await Promise.all([
          fetch(`/api/dashboard/metrics?sprint=${encodeURIComponent(selectedSprint)}`),
          fetch(`/api/dashboard/status-distribution?sprint=${encodeURIComponent(selectedSprint)}`),
        ]);

        if (!metricsRes.ok || !distributionRes.ok) {
          throw new Error('Failed to fetch dashboard data');
        }

        const metricsData = await metricsRes.json();
        const distributionData = await distributionRes.json();

        setMetrics(metricsData);
        setStatusDistribution(distributionData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, [selectedSprint]);

  return { metrics, statusDistribution, isLoading, error };
}

// frontend/src/app/dashboard/page.tsx
'use client';

import { useState } from 'react';
import { LoadingSpinner } from '@/components/LoadingSpinner';
import { MetricCard } from '@/components/MetricCard';
import { StatusDistributionChart } from '@/components/StatusDistributionChart';
import { SprintFilter } from '@/components/SprintFilter';
import { useDashboardData } from '@/hooks/useDashboardData';

export default function DashboardPage() {
  const [selectedSprint, setSelectedSprint] = useState('All');
  const { metrics, statusDistribution, isLoading, error } = useDashboardData(selectedSprint);

  return (
    <div className="min-h-screen bg-gray-50">
      <LoadingSpinner isLoading={isLoading} />

      {!isLoading && (
        <div className="container mx-auto p-6">
          <h1 className="text-3xl font-bold mb-6 text-blue-600">Jira Dashboard</h1>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              錯誤: {error}
            </div>
          )}

          <SprintFilter
            selectedSprint={selectedSprint}
            onSprintChange={setSelectedSprint}
          />

          {metrics ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 my-6">
                <MetricCard
                  title="Total Issue Count"
                  value={metrics.totalIssueCount}
                  icon="📄"
                />
                <MetricCard
                  title="Total Story Points"
                  value={metrics.totalStoryPoints}
                  icon="🎯"
                />
                <MetricCard
                  title="Total Done Item Count"
                  value={metrics.totalDoneItemCount}
                  icon="✓"
                />
                <MetricCard
                  title="Done Story Points"
                  value={metrics.doneStoryPoints}
                  icon="🕐"
                />
              </div>

              <StatusDistributionChart data={statusDistribution} />
            </>
          ) : (
            <div className="text-center py-8 text-gray-500">
              沒有可用資料
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

**關鍵實作細節**:
1. **無超時**: 不使用 `AbortController` 或超時邏輯
2. **持續顯示**: 只要 `isLoading === true`，Spinner 保持顯示
3. **網路錯誤處理**: 顯示錯誤訊息，但仍然關閉 Spinner

---

## 5. Sprint 篩選器去重邏輯（重複 Sprint Name）

### Decision: Sprint Name + (Sprint ID) 格式

**選型**:
- ✅ 格式: "Sprint Name (Sprint ID)"
- ❌ 不使用純 ID
- ❌ 不合併重複項目（保留完整資訊）

**理由**:
1. **規格要求**: spec.md FR-033 明確指定格式
2. **使用者友善**: 顯示名稱同時保留唯一識別
3. **篩選正確性**: 確保篩選邏輯使用正確的 Sprint Name

**實作方案**:

```python
# backend/src/services/sprint_service.py

class SprintService:
    async def get_sprint_options(self, sprint_data: pd.DataFrame) -> List[str]:
        """
        從 GetJiraSprintValues 生成 Sprint 篩選選項

        Column C (index 2): Sprint Name
        Column D (index 3): Sprint ID
        """

        options = ['All']  # 預設選項

        # 提取 Sprint Name 和 Sprint ID
        sprint_names = sprint_data.iloc[:, 2].astype(str)
        sprint_ids = sprint_data.iloc[:, 3].astype(str)

        # 建立 (Name, ID) 對應表
        sprint_pairs = list(zip(sprint_names, sprint_ids))

        # 檢測重複的 Sprint Name
        name_counts = {}
        for name, sprint_id in sprint_pairs:
            if pd.isna(name) or name.strip() == '':
                continue  # 跳過空值
            if name not in name_counts:
                name_counts[name] = []
            name_counts[name].append(sprint_id)

        # 生成顯示選項
        for name, ids in sorted(name_counts.items()):
            if len(ids) > 1:
                # 有重複：顯示 "Name (ID)" 格式
                for sprint_id in ids:
                    options.append(f"{name} ({sprint_id})")
            else:
                # 無重複：只顯示名稱
                options.append(name)

        options.append('No Sprints')  # 最後選項

        return options

    def parse_sprint_name_from_option(self, option: str) -> str:
        """
        從顯示選項反解出真實 Sprint Name

        Examples:
        - "Sprint 1 (11)" -> "Sprint 1"
        - "Current Sprint" -> "Current Sprint"
        """

        if option == 'All' or option == 'No Sprints':
            return option

        # 檢查是否包含 (ID) 後綴
        import re
        match = re.match(r'^(.+)\s+\((\d+)\)$', option)

        if match:
            return match.group(1)  # 返回括號前的部分
        else:
            return option  # 沒有後綴，直接返回
```

**前端使用方式**:

```typescript
// frontend/src/components/SprintFilter.tsx
'use client';

import { useEffect, useState } from 'react';

interface SprintFilterProps {
  selectedSprint: string;
  onSprintChange: (sprint: string) => void;
}

export function SprintFilter({ selectedSprint, onSprintChange }: SprintFilterProps) {
  const [options, setOptions] = useState<string[]>(['All']);

  useEffect(() => {
    async function fetchSprintOptions() {
      try {
        const res = await fetch('/api/sprints');
        const data = await res.json();
        setOptions(data.options);
      } catch (err) {
        console.error('Failed to fetch sprint options:', err);
      }
    }

    fetchSprintOptions();
  }, []);

  return (
    <div className="mb-6">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Sprint 篩選:
      </label>
      <select
        value={selectedSprint}
        onChange={(e) => onSprintChange(e.target.value)}
        className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
}
```

**邊界情況**:

| 情況 | 處理 | 範例 |
|-----|-----|------|
| Sprint Name 重複 1 次 | 顯示 "(ID)" | "Sprint 1 (11)" |
| Sprint Name 重複 2+ 次 | 顯示 "(ID)" | "Sprint 1 (11)", "Sprint 1 (15)" |
| Sprint Name 無重複 | 不顯示 "(ID)" | "Current Sprint" |
| Sprint Name 為空 | 跳過此項 | (不列在選項中) |

---

## 6. 技術限制與風險評估

### 已知限制

| 限制 | 影響 | 緩解方案 |
|-----|-----|---------|
| Google Sheets 公開連結失效 | API 無法連接 | 展示錯誤訊息 + 使用快取資料 |
| 大量並發請求 | Google 限流 | 5 分鐘快取 + 假設 50 使用者上限 |
| CSV 欄位順序變更 | 資料對應錯誤 | spec 假設 schema 穩定（MVP 不處理） |
| 單一 Python 進程 | 快取不同步 | 水平擴展時使用 Redis（Phase 2+） |
| Story Points 非數值 | 計算偏差 | 視為 0 (FR-032) |

### 假設與驗證

| 假設 | 驗證方法 | 優先級 |
|-----|--------|--------|
| Google Sheets URL 保持有效 | 定期監控 | P0 |
| 50 使用者足以測試 | 負載測試 | P1 |
| 5 分鐘快取足夠 | 使用者反饋 | P1 |
| rawData schema 穩定 | 文件確認 | P1 |

---

## 7. 依賴技術總結

### 核心依賴

**後端**:
- **FastAPI** (0.104.1): 高效的 Python 非同步 Web 框架，選擇理由：快速開發、自動 API 文檔
- **Pandas** (2.1.3): CSV 解析 + 資料轉換，選擇理由：優化的向量化操作、易於 GroupBy 操作
- **httpx** (0.25.2): 非同步 HTTP 客戶端，選擇理由：async/await 支援、與 FastAPI 搭配完善
- **Uvicorn** (0.24.0): ASGI 伺服器，選擇理由：FastAPI 官方推薦

**前端**:
- **Next.js** (15.2.4): React 全棧框架，選擇理由：內建路由、伺服器元件、最小化客戶端 JS
- **React** (19.0.0): UI 元件庫，選擇理由：hooks API、宣告式語法
- **Recharts** (2.x): 資料視覺化，選擇理由：簡單易用、無依賴 D3
- **Tailwind CSS** (3.4.x): CSS 框架，選擇理由：快速原型設計、預定義樣式
- **shadcn/ui**: 元件庫，選擇理由：高品質 Radix UI 包裝、易客製化

**測試**:
- **pytest** (7.4.3): Python 測試框架，選擇理由：簡潔語法、豐富外掛
- **Jest** (29.x): JavaScript 測試框架，選擇理由：無配置、快速執行
- **React Testing Library** (14.x): React 元件測試，選擇理由：測試行為而非實作細節

---

## 8. 實作路徑建議

### Phase 1: 資料層 (優先)

1. **GoogleSheetsService**: CSV 取得 + 解析
2. **CacheService**: TTL 快取實現
3. **DataProcessor**: 23 欄位轉換 + 指標計算

✅ **優點**: 後端獨立可測試，前端可以 Mock API

### Phase 2: API 層

1. **FastAPI 路由**: 3 個端點 (/metrics, /status-distribution, /sprints)
2. **錯誤處理**: 例外捕獲 + 日誌
3. **契約測試**: API 回應驗證

### Phase 3: 前端層

1. **React 元件**: MetricCard, StatusDistributionChart, SprintFilter
2. **資料鉤子**: useDashboardData 狀態管理
3. **載入狀態**: LoadingSpinner, ErrorBoundary

### Phase 4: 整合與測試

1. **端到端測試**: 完整流程驗證
2. **效能測試**: 3 秒載入目標
3. **並發測試**: 50 使用者情景

---

## 8. 測試策略與工具選型

### Decision: 多層次測試金字塔

**選型**:
- ✅ 單元測試（Unit Tests）: Jest + React Testing Library (前端), pytest (後端)
- ✅ E2E 測試（End-to-End）: Playwright
- ✅ 負載測試（Load Testing）: k6 或 Locust
- ✅ API Mock: Mock Service Worker (MSW)

**理由**:
1. **完整覆蓋 testcases.md**: 20 個測試案例對應不同測試層級
2. **自動化優先**: 16/20 測試案例可全自動執行
3. **CI/CD 友善**: Playwright 和 k6 支援無頭模式
4. **真實使用者場景**: E2E 測試模擬完整流程

**測試分層策略**:

```
           ▲
          / \
         /   \        E2E Tests (Playwright)
        /     \       TC-DASHBOARD-*, TC-CHART-*, TC-FILTER-*
       /_______\      4 spec files, ~15 test scenarios
      /         \
     /           \    Integration Tests (Jest + RTL)
    /   API Mock  \   Component 互動、資料流測試
   /      (MSW)    \  TC-EDGE-001 (API 失敗模擬)
  /_________________\
 /                   \ Unit Tests (Jest/pytest)
/   快速、孤立測試    \ 元件邏輯、資料處理、計算函數
/_____________________\ 覆蓋率目標: 80%+
```

**測試案例對應**:

| 測試類型 | 工具 | 覆蓋測試案例 | 執行時機 |
|---------|------|-------------|---------|
| 單元測試 | Jest/pytest | 資料計算邏輯、狀態分布統計 | 每次 commit |
| 元件測試 | React Testing Library | MetricCard, SprintFilter 渲染 | 每次 commit |
| E2E 測試 | Playwright | TC-DASHBOARD-001~004, TC-CHART-001~005, TC-FILTER-001~008 | 每次 PR |
| 負載測試 | k6/Locust | TC-EDGE-005 (100 concurrent users) | 發布前 |
| API Mock | MSW | TC-EDGE-001 (Google Sheets 失敗) | 開發階段 |

**測試資料管理**:

```
backend/tests/fixtures/
├── test_data_tc_dashboard_002.csv  # 10 筆 Issue, 預期 Total=10, Done=4
├── test_data_edge_002.csv          # 包含 3 筆無效 Status
├── test_data_edge_003.csv          # 包含非數值 Story Points
└── sprint_duplicate_names.csv      # 重複 Sprint Name 測試資料

使用方式：
1. 單元測試: 直接讀取 fixture CSV
2. E2E 測試: 透過環境變數切換測試 Google Sheet
3. 負載測試: 使用真實 Google Sheet (但資料量較大)
```

**自動化測試執行流程**:

```yaml
# CI/CD Pipeline (GitHub Actions)
on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - Frontend: npm test (Jest + RTL)
      - Backend: pytest tests/unit

  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - Backend: pytest tests/integration
      - Frontend: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - npx playwright test
      - 上傳測試報告和截圖

  load-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    steps:
      - k6 run tests/load/k6-script.js
      - 驗證 p95 < 5s, 成功率 > 95%
```

**測試優先級 (基於 testcases.md)**:

**P0 (阻礙發布)**:
- TC-DASHBOARD-001, 002 (核心統計)
- TC-CHART-001, 002 (長條圖核心)
- TC-FILTER-005, 006 (Sprint 篩選核心)
- TC-EDGE-001 (錯誤處理)

**P1 (重要)**:
- TC-DASHBOARD-003 (空狀態)
- TC-CHART-003, 005 (互動與空狀態)
- TC-FILTER-008 (即時更新)
- TC-EDGE-002, 003 (資料品質)

**P2 (次要)**:
- TC-DASHBOARD-004 (快取)
- TC-FILTER-003, 004, 007 (進階篩選)
- TC-EDGE-004, 005 (邊界情況與效能)

**測試覆蓋率目標**:

| 專案 | 單元測試 | 整合測試 | E2E 測試 | 總覆蓋率目標 |
|-----|---------|---------|---------|------------|
| 前端 | 80%+ | 60%+ | 主流程 100% | 75%+ |
| 後端 | 85%+ | 70%+ | API 100% | 80%+ |

---

## 結論

所有技術選型基於 **簡化、有效、符合規格** 的原則。特別強調：

1. **無 API 金鑰依賴** → 簡化部署
2. **5 分鐘 In-Memory 快取** → 平衡效能與即時性
3. **嚴格遵守 23 欄位索引存取** → 展示 MVP 約束下的開發
4. **持續載入指示器** → 改善使用者體驗
5. **重複 Sprint 名稱去重** → 保留資料完整性
6. **多層次測試策略** → 確保 20 個測試案例完整覆蓋

這些決策為 Phase 1 設計和 Phase 2 實作奠定了堅實基礎。

