# Test Case Overview: Jira Dashboard MVP v1.0

**Feature Branch**: `001-jira-dashboard-mvp`
**Created**: 2025-10-29
**Status**: Draft

本文件提供 Jira Dashboard MVP v1.0 所有測試案例的快速摘要，方便人為閱讀與追蹤測試進度。

---

## 測試案例總覽統計

| 項目 | 數量 |
|------|------|
| **總測試案例數** | 20 |
| **User Story 1 測試案例** | 4 |
| **User Story 2 測試案例** | 5 |
| **User Story 3 測試案例** | 8 |
| **Edge Cases 測試案例** | 5 |

### 測試類型分布

| 測試類型 | 數量 |
|---------|------|
| 功能測試（正常流程） | 13 |
| 異常測試（錯誤處理） | 4 |
| 邊界測試（特殊情況） | 3 |
| 效能測試 | 1 |

### 自動化程度分布

| 自動化程度 | 數量 |
|-----------|------|
| 全自動（E2E/API 測試） | 16 |
| 半自動（需手動設定） | 4 |

---

## User Story 1: 即時專案健康度監控（4 個測試案例）

### TC-DASHBOARD-001 | 驗證儀表板首頁顯示四個統計卡片
- **測試重點**: 頁面載入後顯示 Total Issue Count、Total Story Points、Total Done Item Count、Done Story Points 四個卡片
- **優先級**: P0
- **自動化**: 全自動（E2E）

### TC-DASHBOARD-002 | 驗證統計卡片顯示正確的計算數值
- **測試重點**: 基於 rawData 工作表資料，統計卡片數值計算準確率達 100%（包含小數點 Story Points）
- **優先級**: P0
- **自動化**: 全自動（E2E + API）

### TC-DASHBOARD-003 | 驗證無資料或無法連接時的空狀態處理
- **測試重點**: 空資料表顯示 0，連接失敗顯示友善錯誤訊息（3 秒內，不崩潰）
- **優先級**: P1
- **自動化**: 半自動（需手動模擬網路錯誤）

### TC-DASHBOARD-004 | 驗證資料更新後快取過期機制
- **測試重點**: Google Sheets 資料更新後，5 分鐘內顯示舊資料（快取），5 分鐘後重新整理顯示新資料
- **優先級**: P2
- **自動化**: 半自動（需等待 5 分鐘）

---

## User Story 2: Issue 狀態分布視覺化（5 個測試案例）

### TC-CHART-001 | 驗證 Issue 狀態分布長條圖顯示
- **測試重點**: 頁面載入後顯示長條圖，使用藍色主題，底部顯示總 Issue 數
- **優先級**: P0
- **自動化**: 全自動（E2E）

### TC-CHART-002 | 驗證長條圖按固定順序顯示 9 個狀態
- **測試重點**: 長條圖按固定順序顯示 Backlog → Evaluated → To Do → In Progress → Waiting → Ready to Verify → Done → Invalid → Routine
- **優先級**: P0
- **自動化**: 全自動（E2E）

### TC-CHART-003 | 驗證滑鼠懸停顯示詳細數值和百分比
- **測試重點**: 滑鼠懸停在長條上時，0.5 秒內顯示 Tooltip（包含狀態名稱、Issue 數量、百分比）
- **優先級**: P1
- **自動化**: 全自動（E2E）

### TC-CHART-004 | 驗證長條圖底部顯示總 Issue 數量統計
- **測試重點**: 長條圖底部或標題區域顯示總 Issue 數，與 Total Issue Count 卡片一致
- **優先級**: P2
- **自動化**: 全自動（E2E）

### TC-CHART-005 | 驗證無資料時的空狀態提示
- **測試重點**: rawData 工作表無資料時，長條圖區域顯示友善的空狀態提示訊息
- **優先級**: P1
- **自動化**: 全自動（E2E）

---

## User Story 3: Sprint 篩選功能（8 個測試案例）

### TC-FILTER-001 | 驗證 Sprint 篩選器下拉選單顯示
- **測試重點**: 頁面頂部顯示 Sprint 篩選器，預設值為「All」
- **優先級**: P0
- **自動化**: 全自動（E2E）

### TC-FILTER-002 | 驗證 Sprint 篩選器選項完整性
- **測試重點**: 下拉選單包含「All」、所有 Sprint 名稱、「No Sprints」選項
- **優先級**: P1
- **自動化**: 全自動（E2E）

### TC-FILTER-003 | 驗證 Sprint 選項從正確的工作表欄位讀取
- **測試重點**: 系統從 GetJiraSprintValues 工作表的 Column C（Sprint Name）和 Column D（Sprint ID）讀取資料
- **優先級**: P2
- **自動化**: 全自動（API + E2E）

### TC-FILTER-004 | 驗證重複 Sprint Name 的處理（顯示 Sprint ID）
- **測試重點**: 重複的 Sprint Name 以「Sprint Name (Sprint ID)」格式顯示（例如「Sprint 1 (11)」、「Sprint 1 (15)」）
- **優先級**: P2
- **自動化**: 全自動（E2E）

### TC-FILTER-005 | 驗證選擇「All」顯示所有 Issue
- **測試重點**: 選擇「All」時，統計卡片和長條圖顯示所有 Issue（不受 Sprint 欄位影響）
- **優先級**: P0
- **自動化**: 全自動（E2E）

### TC-FILTER-006 | 驗證選擇特定 Sprint 的篩選功能
- **測試重點**: 選擇特定 Sprint 時，只顯示該 Sprint 的 Issue 統計和分布（透過 rawData 的 Sprint 欄位篩選）
- **優先級**: P0
- **自動化**: 全自動（E2E）

### TC-FILTER-007 | 驗證選擇「No Sprints」的篩選功能
- **測試重點**: 選擇「No Sprints」時，只顯示 Sprint 欄位為空的 Issue
- **優先級**: P2
- **自動化**: 全自動（E2E）

### TC-FILTER-008 | 驗證切換 Sprint 時統計和圖表即時更新
- **測試重點**: 切換不同 Sprint 時，統計卡片和長條圖在 2 秒內即時同步更新（無需重新整理頁面）
- **優先級**: P1
- **自動化**: 全自動（E2E）

---

## Edge Cases: 邊界與異常情況（5 個測試案例）

### TC-EDGE-001 | 驗證 Google Sheets 連結失效時的錯誤處理
- **測試重點**: Google Sheets 無法連接時，3 秒內顯示友善錯誤訊息（不崩潰或白屏）
- **優先級**: P0
- **自動化**: 半自動（需手動設定或 Mock API）

### TC-EDGE-002 | 驗證 Status 欄位包含無效值時的處理
- **測試重點**: Status 包含非預定義狀態值時，Total Issue Count 仍包含這些記錄，但長條圖忽略它們
- **優先級**: P1
- **自動化**: 全自動（E2E）

### TC-EDGE-003 | 驗證 Story Points 欄位包含非數值資料時的處理
- **測試重點**: Story Points 包含非數值（文字、特殊符號等）時，視為 0 進行計算，Issue 仍計入統計
- **優先級**: P1
- **自動化**: 全自動（E2E）

### TC-EDGE-004 | 驗證 GetJiraSprintValues 工作表無資料時的處理
- **測試重點**: GetJiraSprintValues 工作表為空時，Sprint 篩選器只顯示「All」和「No Sprints」選項（不崩潰）
- **優先級**: P2
- **自動化**: 全自動（E2E）

### TC-EDGE-005 | 驗證大量使用者同時存取時的效能（快取機制）
- **測試重點**: 100 個並發使用者同時存取時，90% 載入時間不超過 5 秒，快取機制生效減少 API 呼叫
- **優先級**: P2
- **自動化**: 全自動（負載測試工具）

---

## 測試優先級分類

### P0（必須通過，阻礙發布）- 8 個測試案例

| 測試案例編號 | 測試目標 |
|------------|---------|
| TC-DASHBOARD-001 | 驗證儀表板首頁顯示四個統計卡片 |
| TC-DASHBOARD-002 | 驗證統計卡片顯示正確的計算數值 |
| TC-CHART-001 | 驗證 Issue 狀態分布長條圖顯示 |
| TC-CHART-002 | 驗證長條圖按固定順序顯示 9 個狀態 |
| TC-FILTER-001 | 驗證 Sprint 篩選器下拉選單顯示 |
| TC-FILTER-005 | 驗證選擇「All」顯示所有 Issue |
| TC-FILTER-006 | 驗證選擇特定 Sprint 的篩選功能 |
| TC-EDGE-001 | 驗證 Google Sheets 連結失效時的錯誤處理 |

### P1（重要，影響使用者體驗）- 7 個測試案例

| 測試案例編號 | 測試目標 |
|------------|---------|
| TC-DASHBOARD-003 | 驗證無資料或無法連接時的空狀態處理 |
| TC-CHART-003 | 驗證滑鼠懸停顯示詳細數值和百分比 |
| TC-CHART-005 | 驗證無資料時的空狀態提示 |
| TC-FILTER-002 | 驗證 Sprint 篩選器選項完整性 |
| TC-FILTER-008 | 驗證切換 Sprint 時統計和圖表即時更新 |
| TC-EDGE-002 | 驗證 Status 欄位包含無效值時的處理 |
| TC-EDGE-003 | 驗證 Story Points 欄位包含非數值資料時的處理 |

### P2（次要，可接受風險）- 5 個測試案例

| 測試案例編號 | 測試目標 |
|------------|---------|
| TC-DASHBOARD-004 | 驗證資料更新後快取過期機制 |
| TC-CHART-004 | 驗證長條圖底部顯示總 Issue 數量統計 |
| TC-FILTER-003 | 驗證 Sprint 選項從正確的工作表欄位讀取 |
| TC-FILTER-004 | 驗證重複 Sprint Name 的處理（顯示 Sprint ID） |
| TC-FILTER-007 | 驗證選擇「No Sprints」的篩選功能 |
| TC-EDGE-004 | 驗證 GetJiraSprintValues 工作表無資料時的處理 |
| TC-EDGE-005 | 驗證大量使用者同時存取時的效能（快取機制） |

---

## 自動化測試工具建議

| 測試類型 | 建議工具 | 適用測試案例 |
|---------|---------|------------|
| **E2E 測試** | Playwright 或 Cypress | TC-DASHBOARD-*, TC-CHART-*, TC-FILTER-* 系列（16 個） |
| **API 測試** | Postman 或 REST Assured | TC-FILTER-003（驗證資料讀取邏輯） |
| **負載測試** | k6 或 Apache JMeter | TC-EDGE-005（效能測試） |
| **Mock API** | Mock Service Worker (MSW) | TC-EDGE-001（模擬 API 失敗） |

---

## CI/CD 整合建議

### 每次 Commit（快速驗證）
執行所有 **P0 測試案例**（8 個），預計執行時間：5-8 分鐘
- 核心功能驗證：統計卡片、長條圖、Sprint 篩選器基本功能

### 每次 Pull Request（完整驗證）
執行 **P0 + P1 測試案例**（15 個），預計執行時間：12-15 分鐘
- 完整功能驗證 + UX 體驗驗證

### 發布前驗證（全面驗證）
執行 **所有測試案例**（20 個），預計執行時間：18-25 分鐘
- 包含邊界情況、效能測試、快取機制驗證

### 定期回歸測試（每週）
執行 **完整測試套件 + 效能測試**
- 確保系統穩定性與效能表現

---

## 測試資料準備建議

### Google Sheets 測試環境設定

建議準備 **3 組測試資料集**：

#### 1. 最小資料集（快速測試）
- **rawData**: 10 筆 Issue（涵蓋所有 9 種狀態）
- **GetJiraSprintValues**: 3 個 Sprint
- **用途**: 快速驗證核心功能（P0 測試案例）

#### 2. 標準資料集（完整測試）
- **rawData**: 50 筆 Issue（包含邊界情況：無效 Status、非數值 Story Points、空 Sprint）
- **GetJiraSprintValues**: 10 個 Sprint（包含重複 Sprint Name）
- **用途**: 完整功能驗證（P0 + P1 測試案例）

#### 3. 壓力測試資料集（效能測試）
- **rawData**: 500 筆 Issue
- **GetJiraSprintValues**: 50 個 Sprint
- **用途**: 效能與負載測試（TC-EDGE-005）

---

## 測試執行檢查清單

### 測試前準備
- [ ] 確認測試環境 Google Sheets 資料已準備完成
- [ ] 確認應用程式已部署至測試環境
- [ ] 確認測試工具（Playwright/Cypress）已安裝並設定完成
- [ ] 確認瀏覽器版本符合需求（Chrome/Firefox/Safari/Edge 最新版）

### P0 測試案例執行（發布前必須全部通過）
- [ ] TC-DASHBOARD-001
- [ ] TC-DASHBOARD-002
- [ ] TC-CHART-001
- [ ] TC-CHART-002
- [ ] TC-FILTER-001
- [ ] TC-FILTER-005
- [ ] TC-FILTER-006
- [ ] TC-EDGE-001

### P1 測試案例執行（建議通過，影響 UX）
- [ ] TC-DASHBOARD-003
- [ ] TC-CHART-003
- [ ] TC-CHART-005
- [ ] TC-FILTER-002
- [ ] TC-FILTER-008
- [ ] TC-EDGE-002
- [ ] TC-EDGE-003

### P2 測試案例執行（可選，風險可接受）
- [ ] TC-DASHBOARD-004
- [ ] TC-CHART-004
- [ ] TC-FILTER-003
- [ ] TC-FILTER-004
- [ ] TC-FILTER-007
- [ ] TC-EDGE-004
- [ ] TC-EDGE-005

---

## 缺陷追蹤建議

當測試案例執行失敗時，建議記錄以下資訊：

| 欄位 | 說明 |
|------|------|
| **測試案例編號** | 例如 TC-DASHBOARD-002 |
| **缺陷描述** | 簡述實際行為與預期行為的差異 |
| **重現步驟** | 參考測試案例的測試步驟 |
| **環境資訊** | 瀏覽器版本、作業系統、測試資料集 |
| **嚴重程度** | Critical（P0）、High（P1）、Medium（P2） |
| **相關螢幕截圖或日誌** | 協助開發人員快速定位問題 |

---

## 相關文件

| 文件 | 用途 |
|------|------|
| [testcases.md](./testcases.md) | 詳細測試案例（包含完整欄位與測試步驟） |
| [spec.md](./spec.md) | 功能規格文件（包含 User Stories 和 Acceptance Criteria） |
| [user-story-guide.md](../../docs/template/user-story-guide.md) | User Story 撰寫指引 |
| [acceptance-criteria-guide.md](../../docs/template/acceptance-criteria-guide.md) | Acceptance Criteria 撰寫指引 |
| [testcase-guide.md](../../docs/template/testcase-guide.md) | Test Case 撰寫指引 |

---

**注意**: 本文件為測試案例的快速摘要，完整的測試步驟、測試資料、預期結果請參考 [testcases.md](./testcases.md)。
