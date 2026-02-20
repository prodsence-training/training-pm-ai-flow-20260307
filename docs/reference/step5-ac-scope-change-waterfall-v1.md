# 🎯 Acceptance Criteria: Scope Change Waterfall Widget（Step 4）

## 對應 User Story

本文件為 [step3-userstory-v1.md](./step3-userstory-v1.md) 中 **Solution A: Scope Change Waterfall Widget（範疇變更瀑布圖）** 的 Acceptance Criteria。

---

## 前置條件：新增 SprintBaseline 資料表

為支援「初始承諾」與「插單/移除」的計算，需新增以下資料結構：

| 欄位 | 類型 | 說明 |
|------|------|------|
| Sprint Name | string | Sprint 名稱（對應 GetJiraSprintValues） |
| Snapshot Date | date | 快照時間（Sprint startDate） |
| Issue Key | string | 初始分配的 Issue Key |
| Story Points | number | 該 Issue 當時的 Story Points |
| Issue Type | string | Bug / Story / Task |

### 計算邏輯定義

| 術語 | 計算方式 |
|------|----------|
| **初始承諾** | SprintBaseline 中該 Sprint 所有 Issue 的 Story Points 總和 |
| **新增插單** | 現在在 Sprint 中，但不在 SprintBaseline 中的 Issue 總點數 |
| **移除項目** | 在 SprintBaseline 中，但現在不在 Sprint 中的 Issue 總點數 |
| **最終狀態** | 初始承諾 + 新增插單 - 移除項目 |

### Issue Type 分類對應

| Issue Type | 分類名稱 |
|------------|----------|
| Story | Feature |
| Task | Operation |
| Bug | Bug |

---

## Story 1: 檢視 Sprint 範疇變動全貌 (The Overview)

### AC1-1: 成功顯示瀑布圖

```gherkin
場景：PM 查看 Sprint 範疇變動瀑布圖
Given 使用者已進入儀表板
And SprintBaseline 已記錄該 Sprint 的初始項目
When 使用者進入 Scope Change Waterfall Widget
Then 系統應顯示瀑布圖，包含：
  | 區塊     | 顏色 | 計算邏輯                              |
  | 初始承諾 | 藍色 | Baseline 總點數                       |
  | 新增插單 | 紅色 | 現在在 Sprint 但不在 Baseline 的總點數 |
  | 移除項目 | 黃色 | 在 Baseline 但現在不在 Sprint 的總點數 |
  | 最終狀態 | 綠色 | 初始承諾 + 新增插單 - 移除項目         |
```

### AC1-2: 空值 Story Points 處理

```gherkin
場景：Issue 的 Story Points 為空值
Given 某 Issue 的 Story Points 欄位為空
When 系統計算瀑布圖數據
Then 該 Issue 的 Story Points 應視為 0
```

### AC1-3: Sprint 無 Issue 時顯示空狀態

```gherkin
場景：選定的 Sprint 沒有任何 Issue
Given 該 Sprint 無任何 Issue
When 瀑布圖載入完成
Then 系統應顯示空的瀑布圖（所有區塊數值為 0）
```

---

## Story 2: 分析插單來源與類型 (The Drill-down)

### AC2-1: Tooltip 顯示插單分類統計

```gherkin
場景：PM 查看新增插單的類型分布
Given 新增插單（紅色區塊）包含多個 Issue
When 使用者懸停在紅色區塊上
Then Tooltip 應顯示：
  | 類型      | 說明                    |
  | Feature   | Story 類型的總點數      |
  | Operation | Task 類型的總點數       |
  | Bug       | Bug 類型的總點數        |
  | 總計      | 所有類型的總點數        |
```

### AC2-2: 無插單時的 Tooltip

```gherkin
場景：Sprint 沒有新增插單
Given 新增插單點數為 0
When 使用者懸停在紅色區塊上
Then Tooltip 應顯示「無新增項目」
```

---

## Story 3: 展示交換與取捨的代價 (The Trade-off)

### AC3-1: Tooltip 顯示移除項目統計

```gherkin
場景：PM 查看移除項目的類型分布
Given 移除項目（黃色區塊）包含多個 Issue
When 使用者懸停在黃色區塊上
Then Tooltip 應顯示：
  | 類型      | 說明                    |
  | Feature   | Story 類型的總點數      |
  | Operation | Task 類型的總點數       |
  | Bug       | Bug 類型的總點數        |
  | 總計      | 所有類型的總點數        |
```

### AC3-2: 無移除項目時的 Tooltip

```gherkin
場景：Sprint 沒有移除項目
Given 移除項目點數為 0
When 使用者懸停在黃色區塊上
Then Tooltip 應顯示「無移除項目」
```

---

## Story 4: 切換不同 Sprint 的歷史數據 (Context Switching)

### AC4-1: Sprint 下拉選單顯示所有 Sprint

```gherkin
場景：PM 查看 Sprint 下拉選單
Given 使用者進入 Widget
When Widget 載入完成
Then 下拉選單應包含：
  - 「ALL」選項（預設選中）
  - 所有 Sprint（包含 future、active、closed 狀態）
```

### AC4-2: 切換 Sprint 更新瀑布圖

```gherkin
場景：PM 切換到特定 Sprint
Given 瀑布圖已顯示
When 使用者選擇「Sprint 12」
Then 瀑布圖應更新為 Sprint 12 的數據
```

### AC4-3: 選擇 ALL 顯示彙總數據

```gherkin
場景：PM 選擇 ALL 查看全部 Sprint 彙總
Given 使用者已選擇某特定 Sprint
When 使用者選擇「ALL」
Then 瀑布圖應顯示所有 Sprint 的加總數據
```

---

## 通用：錯誤處理

### AC-ERR-1: API 讀取失敗

```gherkin
場景：API 讀取失敗
Given 使用者進入 Widget
When API 請求失敗
Then 系統應顯示錯誤訊息「資料載入失敗，請稍後再試」
And 不應顯示舊的 cached 資料
```

---

## User Story → AC 對應表

| User Story | AC 編號 | 情境類型 |
|------------|---------|----------|
| Story 1: The Overview | AC1-1 | ✅ 正常流程 |
| Story 1: The Overview | AC1-2 | ⚠️ 邊界條件 |
| Story 1: The Overview | AC1-3 | ⚠️ 邊界條件 |
| Story 2: The Drill-down | AC2-1 | ✅ 正常流程 |
| Story 2: The Drill-down | AC2-2 | ⚠️ 邊界條件 |
| Story 3: The Trade-off | AC3-1 | ✅ 正常流程 |
| Story 3: The Trade-off | AC3-2 | ⚠️ 邊界條件 |
| Story 4: Context Switching | AC4-1 | ✅ 正常流程 |
| Story 4: Context Switching | AC4-2 | ✅ 正常流程 |
| Story 4: Context Switching | AC4-3 | ✅ 正常流程 |
| 通用 | AC-ERR-1 | ❌ 異常情況 |

---

## 不包含的內容（Out of Scope）

延續 User Story 的 Out of Scope 定義，以下情境本次 **不撰寫 AC**：

- 插單的「提出者（Requester）」歸因顯示
- 「移除項目」與「插單」的一對一對應關係
- 靜態報表匯出功能（PDF/Excel）
- 跨 Sprint 的歷史趨勢比較圖

---

## 相關文件

| 文件 | 說明 |
|------|------|
| [step3-userstory-v1.md](./step3-userstory-v1.md) | 對應的 User Story |
| [acceptance-criteria-guide.md](../template/acceptance-criteria-guide.md) | AC 撰寫指引 |
| [table-schema.md](../table-schema.md) | 資料表架構說明 |
| [tech-overview.md](../tech-overview.md) | 技術架構概覽 |
