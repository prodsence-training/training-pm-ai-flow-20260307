# API 契約: Jira Dashboard MVP v1.0

**Date**: 2025-10-29 | **Version**: 1.0.0

---

## 概述

本文件定義前後端之間的 REST API 契約。所有端點均基於 spec.md 的功能需求實作。

**Base URL**: `http://localhost:8000/api` (開發環境) 或由環境變數 `NEXT_PUBLIC_API_URL` 指定

**認證**: 無（MVP 階段）

**錯誤處理**: 所有端點在失敗時返回 HTTP 錯誤狀態碼 + JSON 錯誤訊息

---

## API 端點

### 1. GET /api/dashboard/metrics

**功能**: 取得四個統計卡片的數據（總 Issue 數、總故事點數、已完成 Issue 數、已完成故事點數）

**參數**:

| 參數 | 型別 | 必填 | 預設值 | 說明 |
|-----|------|------|--------|------|
| `sprint` | string | No | "All" | Sprint 篩選（"All"、特定 Sprint 名稱、或 "No Sprints"） |

**請求範例**:

```bash
# 取得所有 Sprint 的指標
curl "http://localhost:8000/api/dashboard/metrics"

# 取得特定 Sprint 的指標
curl "http://localhost:8000/api/dashboard/metrics?sprint=DEMO1-Sprint%201"

# 取得無 Sprint 的 Issue
curl "http://localhost:8000/api/dashboard/metrics?sprint=No%20Sprints"
```

**回應格式 (200 OK)**:

```json
{
  "totalIssueCount": 45,
  "totalStoryPoints": 128.5,
  "totalDoneItemCount": 12,
  "doneStoryPoints": 34.0,
  "timestamp": "2025-10-29T10:30:45Z",
  "cacheHit": true
}
```

**回應欄位說明**:

| 欄位 | 型別 | 說明 |
|-----|------|------|
| `totalIssueCount` | integer | 總 Issue 數（包含所有 Status，即使無效值） |
| `totalStoryPoints` | number | 總故事點數（支援小數，非數值視為 0） |
| `totalDoneItemCount` | integer | Status 為 "Done" 的 Issue 數 |
| `doneStoryPoints` | number | Status 為 "Done" 的 Issue 的故事點數總和 |
| `timestamp` | string | 響應時間戳（ISO 8601） |
| `cacheHit` | boolean | 是否從快取返回（用於除錯） |

**計算邏輯**:

```
totalIssueCount = COUNT(所有 Issue)
totalStoryPoints = SUM(Story Points) 或 0（非數值）
totalDoneItemCount = COUNT(Status == 'Done')
doneStoryPoints = SUM(Story Points WHERE Status == 'Done')
```

**錯誤回應 (500 Internal Server Error)**:

```json
{
  "detail": "Failed to fetch Google Sheets data",
  "error": "HTTPError",
  "timestamp": "2025-10-29T10:30:45Z"
}
```

**性能目標**: < 3 秒（含快取）(SC-001)

**相關需求**: FR-001, FR-006, FR-008, FR-009, FR-010, FR-011, FR-032

---

### 2. GET /api/dashboard/status-distribution

**功能**: 取得 Issue 狀態分布數據（9 個固定狀態的計數與百分比）

**參數**:

| 參數 | 型別 | 必填 | 預默值 | 說明 |
|-----|------|------|--------|------|
| `sprint` | string | No | "All" | Sprint 篩選 |

**請求範例**:

```bash
curl "http://localhost:8000/api/dashboard/status-distribution?sprint=All"
```

**回應格式 (200 OK)**:

```json
{
  "data": [
    {
      "status": "Backlog",
      "count": 10,
      "percentage": 22.22
    },
    {
      "status": "Evaluated",
      "count": 5,
      "percentage": 11.11
    },
    {
      "status": "To Do",
      "count": 8,
      "percentage": 17.78
    },
    {
      "status": "In Progress",
      "count": 12,
      "percentage": 26.67
    },
    {
      "status": "Waiting",
      "count": 3,
      "percentage": 6.67
    },
    {
      "status": "Ready to Verify",
      "count": 2,
      "percentage": 4.44
    },
    {
      "status": "Done",
      "count": 4,
      "percentage": 8.89
    },
    {
      "status": "Invalid",
      "count": 0,
      "percentage": 0.0
    },
    {
      "status": "Routine",
      "count": 1,
      "percentage": 2.22
    }
  ],
  "totalIssueCount": 45,
  "timestamp": "2025-10-29T10:30:45Z",
  "cacheHit": true
}
```

**回應欄位說明**:

| 欄位 | 型別 | 說明 |
|-----|------|------|
| `data` | array | 狀態分布陣列（9 個固定狀態） |
| `data[].status` | string | 狀態名稱 |
| `data[].count` | integer | 該狀態的 Issue 計數 |
| `data[].percentage` | number | 該狀態的百分比（保留 2 位小數） |
| `totalIssueCount` | integer | 總 Issue 數（用於百分比計算基準） |
| `timestamp` | string | 響應時間戳 |
| `cacheHit` | boolean | 快取命中標誌 |

**邊界情況**:
- **無效狀態排除**: rawData 中 Status 欄位不在 9 個預定義值內的記錄被排除於此計數（FR-031）
- **總計不一致**: `totalIssueCount` 可能大於 `data[].count` 總和（因為無效狀態被排除）
- **零計數**: 當無該狀態的 Issue 時，count = 0，percentage = 0

**性能目標**: < 3 秒（含快取）(SC-001)

**相關需求**: FR-003, FR-004, FR-012, FR-031, FR-034

---

### 3. GET /api/sprints

**功能**: 取得 Sprint 篩選器選項（從 GetJiraSprintValues 工作表讀取）

**參數**: 無

**請求範例**:

```bash
curl "http://localhost:8000/api/sprints"
```

**回應格式 (200 OK)**:

```json
{
  "options": [
    "All",
    "DEMO1-Sprint 1",
    "DEMO1-Sprint 2 (12)",
    "DEMO1-Sprint 2 (15)",
    "Sprint 2024-Q1",
    "No Sprints"
  ],
  "totalSprints": 4,
  "duplicateHandled": 1,
  "timestamp": "2025-10-29T10:30:45Z",
  "cacheHit": true
}
```

**回應欄位說明**:

| 欄位 | 型別 | 說明 |
|-----|------|------|
| `options` | array[string] | Sprint 篩選選項清單 |
| `options[0]` | string | 固定值 "All" |
| `options[1..-2]` | string | Sprint 名稱（重複時附加 Sprint ID） |
| `options[-1]` | string | 固定值 "No Sprints" |
| `totalSprints` | integer | 去重後的 Sprint 總數 |
| `duplicateHandled` | integer | 處理的重複 Sprint Name 計數 |
| `timestamp` | string | 響應時間戳 |
| `cacheHit` | boolean | 快取命中標誌 |

**重複名稱處理邏輯** (FR-033):

```
如果 Sprint Name 重複：
  "Sprint Name (Sprint ID)" - 例如 "DEMO1-Sprint 2 (12)"

如果 Sprint Name 無重複：
  "Sprint Name" - 例如 "DEMO1-Sprint 1"
```

**排序規則**:
1. "All" (首)
2. Sprint Names（字母排序）
3. "No Sprints" (末)

**空 Sprint 處理**:
- GetJiraSprintValues 中空 Sprint Name 的列被忽略
- 無 Sprint 的 Issue 透過 "No Sprints" 選項顯示

**性能目標**: < 2 秒（含快取）

**相關需求**: FR-013, FR-014, FR-015, FR-016, FR-033

---

## 錯誤回應

所有端點在發生錯誤時使用統一的錯誤格式：

**4xx 客戶端錯誤範例**:

```json
{
  "detail": "Invalid sprint parameter",
  "error": "ValidationError",
  "statusCode": 400,
  "timestamp": "2025-10-29T10:30:45Z"
}
```

**5xx 伺服器錯誤範例**:

```json
{
  "detail": "Failed to connect to Google Sheets",
  "error": "ExternalServiceError",
  "statusCode": 500,
  "timestamp": "2025-10-29T10:30:45Z"
}
```

**常見錯誤碼**:

| HTTP 狀態 | 錯誤類型 | 說明 |
|---------|---------|------|
| 400 | ValidationError | 參數無效 |
| 500 | ExternalServiceError | Google Sheets API 連接失敗 |
| 500 | DataProcessingError | CSV 解析或資料轉換失敗 |
| 503 | ServiceUnavailable | 後端服務暫時無法使用 |

**客戶端錯誤處理** (FR-024):
- 顯示友善的錯誤訊息
- 不顯示技術細節（防止資訊洩露）
- 提供重試選項

---

## 快取策略

所有端點適用 5 分鐘 TTL 快取 (FR-021)：

**快取鍵結構**:

```
cache_key_metrics = "metrics:{sprint_name}"
cache_key_distribution = "status-distribution:{sprint_name}"
cache_key_sprints = "sprints:list"

TTL = 300 seconds (5 minutes)
```

**快取命中檢查**:
- 返回值中 `cacheHit: true` 表示從快取返回
- 返回值中 `cacheHit: false` 表示新鮮資料（剛從 Google Sheets 取得）

**快取失效時機**:
- TTL 過期（5 分鐘自動清除）
- 後端重啟（all caches cleared）
- 手動清除（未來版本可提供管理介面）

---

## 請求/回應範例

### 場景 1: 首次載入儀表板

```
前端: GET /api/dashboard/metrics?sprint=All
      GET /api/dashboard/status-distribution?sprint=All
      GET /api/sprints

後端: 從 Google Sheets 取得資料 (第一次，無快取)
      儲存到快取

前端: 接收資料，顯示四個卡片 + 長條圖 + Sprint 下拉選單
```

時間軸：
- 請求發送: 0ms
- 後端處理: ~1000-2500ms (Google Sheets I/O)
- 前端渲染: ~500ms
- 使用者可見: ~2000-3000ms ✅ (SC-001 目標)

### 場景 2: 切換 Sprint 篩選器

```
前端: 使用者選擇 "DEMO1-Sprint 1"
      前端立即發送: GET /api/dashboard/metrics?sprint=DEMO1-Sprint%201
                    GET /api/dashboard/status-distribution?sprint=DEMO1-Sprint%201
      (顯示 Loading Spinner)

後端: 檢查快取
      cache_key = "metrics:DEMO1-Sprint 1"
      如果快取命中: 返回快取資料 (~10-50ms)
      如果快取未命中: 重新計算 (~1000-2500ms)

前端: 接收新資料，更新卡片和圖表
```

時間軸 (快取命中)：
- 請求發送: 0ms
- 後端處理: ~50ms (快取查詢)
- 前端渲染: ~300ms
- 使用者可見: ~350ms ✅ (SC-002 目標: <2s)

### 場景 3: 網路緩慢

```
前端: 發送請求
      顯示 Loading Spinner (立即出現)

後端: 連接 Google Sheets 中...
      等待回應 (可能耗時 5+ 秒)

前端: Spinner 持續顯示
      無超時限制，等待後端回應

後端: 返回資料

前端: Spinner 消失，顯示資料
```

這符合 FR-034（持續顯示 Spinner，無超時）和 SC-011 要求。

---

## 資料轉換責任

| 操作 | 責任方 | 實作位置 |
|-----|--------|---------|
| 原始 CSV 解析 | 後端 | `backend/src/services/google_sheets_service.py` |
| 23 欄位 → Issue 物件 | 後端 | `backend/src/models/issue.py` |
| Issue 物件 → 指標計算 | 後端 | `backend/src/services/data_processor.py` |
| JSON 序列化 | 後端 | FastAPI (自動) |
| JSON 反序列化 | 前端 | `frontend/src/services/api.ts` |
| 資料顯示 | 前端 | React 元件 |

---

## 版本控制

**API 版本**: 1.0.0

**變更計畫**:
- v1.1.0: 新增資料匯出功能
- v2.0.0: 新增使用者認證和個人化篩選

**向後相容性**: 當前版本確保相同的回應格式，新欄位（如 `timestamp`、`cacheHit`）為非破壞性變更。

---

## 相關文件

- [data-model.md](../data-model.md) - 實體定義和驗證規則
- [spec.md](../spec.md) - 功能需求
- [quickstart.md](../quickstart.md) - API 測試指南

