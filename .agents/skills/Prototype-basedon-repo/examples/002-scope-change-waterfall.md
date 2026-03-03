# Prototype 說明：Scope Change Waterfall Widget

**SPEC-002** | 範疇變更瀑布圖

---

## 概述

此 Prototype 展示 Sprint 期間的範疇變動，讓 PM 能在 Sprint Review 會議中用一張圖證明工作量變化。

### 放置位置

| 項目 | 路徑 |
|------|------|
| Prototype 頁面 | `docs/prototype/002-scope-change-waterfall.html` |
| 說明文件 | `docs/prototype/002-scope-change-waterfall.md` |

**特點**：
- 完全獨立於 Production Code，不影響 `frontend/src` 任何檔案
- 使用純 HTML/CSS/JavaScript，不依賴外部 CDN
- 可直接雙擊開啟，不需要伺服器或網路連線

---

## 啟動方式

直接用瀏覽器開啟 HTML 檔案：

```bash
open docs/prototype/002-scope-change-waterfall.html
```

或在 Finder 中雙擊 `002-scope-change-waterfall.html`

---

## 功能說明

### 瀑布圖四個區塊

| 區塊 | 顏色 | 說明 |
|------|------|------|
| 初始承諾 | 藍色 | Sprint 開始時 Baseline 的總點數 |
| 新增插單 | 紅色 | 現在在 Sprint 但不在 Baseline 的總點數 |
| 移除項目 | 黃色 | 在 Baseline 但現在不在 Sprint 的總點數 |
| 最終狀態 | 綠色 | 初始承諾 + 新增插單 - 移除項目 |

### 互動功能

1. **Sprint 下拉選單**：切換不同 Sprint 或選擇 ALL 查看彙總
2. **Tooltip 明細**：
   - 懸停紅色區塊 → 顯示插單的 Feature/Operation/Bug 分類統計
   - 懸停黃色區塊 → 顯示移除項目的 Feature/Operation/Bug 分類統計
3. **數值摘要**：下方顯示各區塊的 Story Points 總數
4. **淨變動百分比**：右上角顯示相對於初始承諾的變動比例

---

## 假資料場景

| Sprint | 場景說明 | 用途 |
|--------|----------|------|
| Sprint 12 | 有插單（Bug 為主）+ 有移除項目 | 正常流程 |
| Sprint 11 | 只有插單，無移除項目 | 邊界條件 |
| Empty Sprint | 完全沒有 Issue | 空狀態 |
| ALL | 所有 Sprint 的彙總 | 全局視圖 |

---

## 截圖指南

建議擷取以下畫面放入 PRD：

- [ ] **主要 UI**：選擇 Sprint 12，顯示完整瀑布圖
- [ ] **插單 Tooltip**：懸停紅色區塊，顯示 Feature/Operation/Bug 分類
- [ ] **移除 Tooltip**：懸停黃色區塊，顯示 Feature/Operation/Bug 分類
- [ ] **ALL 彙總**：選擇 ALL，顯示全部 Sprint 的加總
- [ ] **空狀態**：選擇 Empty Sprint，顯示空數據情況

---

## 與 PRD 對應

| User Story | AC | Prototype 對應 |
|------------|-----|----------------|
| Story 1: The Overview | AC1-1 | 瀑布圖顯示四個區塊 |
| Story 1: The Overview | AC1-2 | 空值 Story Points 視為 0 |
| Story 1: The Overview | AC1-3 | Empty Sprint 場景 |
| Story 2: The Drill-down | AC2-1 | 紅色區塊 Tooltip |
| Story 2: The Drill-down | AC2-2 | 無插單時 Tooltip 顯示「無新增項目」|
| Story 3: The Trade-off | AC3-1 | 黃色區塊 Tooltip |
| Story 3: The Trade-off | AC3-2 | 無移除時 Tooltip 顯示「無移除項目」|
| Story 4: Context Switching | AC4-1 | Sprint 下拉選單 |
| Story 4: Context Switching | AC4-2 | 切換 Sprint 更新圖表 |
| Story 4: Context Switching | AC4-3 | ALL 選項顯示彙總 |

---

## 技術說明

### 使用技術

| 技術 | 說明 |
|------|------|
| HTML5 | 頁面結構 |
| CSS3 | 樣式（內嵌，參考 Tailwind 配色） |
| Vanilla JavaScript | 互動邏輯、假資料、圖表繪製 |

**不依賴任何外部資源**，所有程式碼都在單一 HTML 檔案中。

### Issue Type 對應

| Jira Issue Type | 顯示分類 |
|-----------------|----------|
| Story | Feature |
| Task | Operation |
| Bug | Bug |

### 計算邏輯

```
初始承諾 = sum(Baseline Issues 的 Story Points)
新增插單 = sum(Current Issues - Baseline Issues 的 Story Points)
移除項目 = sum(Baseline Issues - Current Issues 的 Story Points)
最終狀態 = 初始承諾 + 新增插單 - 移除項目
```

### 配色參考

| 用途 | 顏色代碼 |
|------|----------|
| 初始承諾（藍） | #3b82f6 |
| 新增插單（紅） | #ef4444 |
| 移除項目（黃） | #eab308 |
| 最終狀態（綠） | #22c55e |

---

## 後續步驟

此 Prototype 完成後，建議：

1. 確認視覺呈現符合預期
2. 截圖放入 PRD 文件
3. 與工程團隊討論實作細節
4. 規劃 SprintBaseline 資料表的建立時機

---

## 限制說明

- 此為 Prototype，使用假資料，不連接真實 API
- 僅供展示與對齊用途，非正式 Production Code
- 完全獨立於 `frontend/src`，可隨時刪除不影響正式功能
- 不需要網路連線，可離線使用
