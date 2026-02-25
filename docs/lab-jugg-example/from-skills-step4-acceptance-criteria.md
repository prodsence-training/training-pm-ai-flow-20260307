# ✅ Acceptance Criteria 報告 — Step 4

基於 `from-skills-step3-user-story.md` 的 User Stories，經釐清討論後撰寫。

---

## 📌 Epic: Sprint 健康度視覺化與風險預警

### ⚙️ 系統前置條件與限制

| 項目 | 說明 |
|------|------|
| **資料來源** | rawData（Google Sheets）、GetJiraSprintValues、rawStatusTime |
| **資料延遲** | 5 分鐘快取，資料可能延遲最多 5 分鐘 |
| **前置需求** | rawData 表需**新增 Assignee 欄位**（AC04 個人進度功能依賴此欄位） |
| **固定參數（V1）** | 安全閾值固定 15%、停滯時間固定 3 個工作天，下一版再開放配置 |

---

## Story 1: B1 雙重進度條的宏觀預警 (The Pacing Bar)

> **As a** 正在參加 Daily Standup 的開發工程師（Andy/Bob）
> **I want** 在 Dashboard 頂端同時看到「Sprint 理想應達成進度」與「目前實際累積完成進度」的對比，並且當落後超過安全閾值時（15%）進度條會轉為紅色警示，
> **So that** 我能立刻意識到整個團隊或我個人的進度已經嚴重落後，進而在站會中聚焦討論落後的原因，並更有底氣地拒絕臨時的插單。

---

### AC01: 團隊整體進度條正常顯示

```gherkin
場景：使用者查看有 active Sprint 的團隊整體進度
  Given 目前有一個 active 狀態的 Sprint
  And 該 Sprint 內有 Ticket 且部分 Ticket 有設定 Story Points
  When 使用者開啟 Dashboard
  Then Dashboard 頂端應顯示兩條水平進度條
  And 第一條為「理想進度條」，顯示基於 Sprint 工作天流逝的應達成百分比
  And 第二條為「實際進度條」，顯示 Status Category 為 Done 的 Story Points 佔總 Story Points 的百分比
```

### AC02: 進度落後未超過閾值時顯示綠色

```gherkin
場景：團隊實際進度落後但在安全範圍內
  Given 目前有一個 active 狀態的 Sprint
  And 理想進度為 50%
  And 實際完成進度為 40%（落後 10%，未超過 15% 閾值）
  When 使用者查看 Dashboard 進度條
  Then 實際進度條應顯示為綠色
```

### AC03: 進度落後超過閾值時轉紅

```gherkin
場景：團隊實際進度嚴重落後
  Given 目前有一個 active 狀態的 Sprint
  And 理想進度為 50%
  And 實際完成進度為 30%（落後 20%，超過 15% 閾值）
  When 使用者查看 Dashboard 進度條
  Then 實際進度條應顯示為紅色

場景：團隊實際進度超前或持平
  Given 目前有一個 active 狀態的 Sprint
  And 理想進度為 50%
  And 實際完成進度為 55%（超前）
  When 使用者查看 Dashboard 進度條
  Then 實際進度條應顯示為綠色
```

### AC04: 切換為特定 Assignee 的個人進度

> ⚠️ **前置條件**：此 AC 需要 rawData 表新增 Assignee 欄位後才能實作。

```gherkin
場景：使用者查看特定成員的個人進度
  Given 目前有一個 active 狀態的 Sprint
  And rawData 表已包含 Assignee 欄位
  And 該 Sprint 內有多位 Assignee 的 Ticket
  When 使用者點選特定 Assignee
  Then 進度條應切換為該 Assignee 被指派的 Ticket 的理想 vs 實際進度
  And 閾值判斷邏輯與團隊整體一致（落後 > 15% 轉紅）
```

### AC05: Sprint 總 Story Points 為零

```gherkin
場景：Sprint 內所有 Ticket 都沒有設定 Story Points
  Given 目前有一個 active 狀態的 Sprint
  And 該 Sprint 內所有 Ticket 的 Story Points 皆為空值或 0
  When 使用者查看 Dashboard 進度條
  Then 實際進度條應顯示為 0%
  And 不進行落後百分比的計算
```

### AC06: 無 active Sprint 時顯示空白

```gherkin
場景：目前不在任何 Sprint 週期內
  Given GetJiraSprintValues 中沒有 state 為 active 的 Sprint
  When 使用者開啟 Dashboard
  Then 進度條區域應顯示空白（不顯示任何進度條）
```

### AC07: 理想進度排除週末計算

```gherkin
場景：理想進度以工作天線性計算，排除週末
  Given 一個 Sprint 為期 10 個日曆天（含 2 天週末，共 8 個工作天）
  And 目前為 Sprint 開始後的第 4 個工作天
  When 系統計算理想進度
  Then 理想進度應為 50%（4 / 8 工作天）
  And 週六與週日不計入工作天
```

---

## Story 2: B2 停滯票的個體風險識別 (Idle Tracker)

> **As a** 正在參加 Daily Standup 的 Scrum Master 或開發工程師
> **I want** 讓 Jira 上狀態為 `In Progress` 超過「3 個工作天」沒有任何狀態變動的 Ticket，在看板上顯示明顯的紅色警示，
> **So that** 我能在站會指著那張「停滯的票」直接尋求技術支援或說明阻礙，不再把時間浪費在流水帳的工作回報上，進而縮短單一任務的 Cycle Time。

---

### AC08: 停滯超過 3 個工作天顯示紅色警示

```gherkin
場景：Ticket 在 In Progress 狀態停滯超過 3 個工作天
  Given 一張 Ticket 的 Status 為 "In Progress"
  And 該 Ticket 在 rawStatusTime 中最後一次狀態變更距今已超過 3 個工作天
  When 使用者查看 Dashboard 看板
  Then 該 Ticket 應顯示紅色警示標記
```

### AC09: 未滿 3 個工作天不顯示警示

```gherkin
場景：Ticket 在 In Progress 狀態但尚未停滯
  Given 一張 Ticket 的 Status 為 "In Progress"
  And 該 Ticket 在 rawStatusTime 中最後一次狀態變更距今為 2 個工作天
  When 使用者查看 Dashboard 看板
  Then 該 Ticket 不應顯示任何紅色警示標記
```

### AC10: 狀態變更後警示立即消失

```gherkin
場景：停滯 Ticket 的狀態發生變更
  Given 一張 Ticket 原本因停滯超過 3 個工作天而顯示紅色警示
  And 該 Ticket 的狀態從 "In Progress" 變更為其他狀態（如 "Ready to Verify"）
  When 系統重新載入資料後使用者查看 Dashboard
  Then 該 Ticket 的紅色警示應消失
```

### AC11: 停滯時間排除週末

```gherkin
場景：跨越週末的停滯時間計算
  Given 一張 Ticket 在週五進入 "In Progress" 狀態
  And 週六、週日不計入工作天
  When 下週一時系統計算該 Ticket 的停滯時間
  Then 停滯時間應為 1 個工作天（非 3 個日曆天）
  And 該 Ticket 不應顯示紅色警示
```

### AC12: 停滯時間排除台灣國定假日

```gherkin
場景：跨越國定假日的停滯時間計算
  Given 一張 Ticket 在國定假日前一個工作天進入 "In Progress" 狀態
  And 接下來有 1 天為台灣國定假日
  When 系統計算該 Ticket 的停滯時間
  Then 國定假日不應計入工作天
  And 停滯天數應排除該國定假日後重新計算
```

### AC13: 無狀態變更記錄時不顯示警示

```gherkin
場景：Ticket 在 rawStatusTime 中無任何狀態變更記錄
  Given 一張 Ticket 的 Status 為 "In Progress"
  And rawStatusTime 表中沒有該 Ticket 的任何狀態變更記錄
  When 使用者查看 Dashboard 看板
  Then 該 Ticket 不應顯示紅色警示（因無法判斷停滯時間）
```

---

## 📊 Story → AC Mapping Table

### Story 1: The Pacing Bar

| User Story 需求點 | 對應 AC | 情境數 |
|---|---|---|
| Dashboard 頂端顯示理想 vs 實際進度對比 | AC01 | 1 |
| 落後超過 15% 時進度條轉紅 | AC02, AC03 | 3 |
| 可切換為特定 Assignee 的個人進度 | AC04 | 1 |
| Sprint 總 Story Points 為 0 的處理 | AC05 | 1 |
| 無 active Sprint 的處理 | AC06 | 1 |
| 理想進度排除週末（線性計算） | AC07 | 1 |

### Story 2: Idle Tracker

| User Story 需求點 | 對應 AC | 情境數 |
|---|---|---|
| In Progress 超過 3 工作天無 status 變動 → 紅色警示 | AC08 | 1 |
| 未滿 3 個工作天 → 無警示 | AC09 | 1 |
| 狀態變更後 → 警示立即消失 | AC10 | 1 |
| 停滯時間排除週末 | AC11 | 1 |
| 停滯時間排除台灣國定假日 | AC12 | 1 |
| 無狀態變更記錄 → 不顯示警示 | AC13 | 1 |

---

## 📝 V1 固定參數備註（下一版可配置化）

| 參數 | V1 固定值 | 下一版方向 |
|------|----------|-----------|
| 安全閾值（The Pacing Bar） | 15% | 開放使用者或管理者配置 |
| 停滯時間（Idle Tracker） | 3 個工作天 | 開放使用者或管理者配置 |

---

*產出時間：2026-02-25 · 基於 User Story Step 3 與 Clarification First 流程*
