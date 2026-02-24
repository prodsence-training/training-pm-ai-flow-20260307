# 📖 User Story 拆解報告 — Step 3

基於 `from-skills-step2-ost.md` 的機會解決方案，轉化為開發可執行的 User Stories。

---

## 📌 Epic: Sprint 健康度視覺化與風險預警

### Story 1: B1 雙重進度條的宏觀預警 (The Pacing Bar)

> **As a** 正在參加 Daily Standup 的開發工程師（Andy/Bob）  
> **I want** 在 Dashboard 頂端同時看到「Sprint 理想應達成進度」與「目前實際累積完成進度」的對比，並且當落後超過安全閾值時（如 15%）進度條會轉為紅色警示，  
> **So that** 我能立刻意識到整個團隊或我個人的進度已經嚴重落後，進而在站會中聚焦討論落後的原因，並更有底氣地拒絕臨時的插單。

### Story 2: B2 停滯票的個體風險識別 (Idle Tracker)

> **As a** 正在參加 Daily Standup 的 Scrum Master 或開發工程師  
> **I want** 讓 Jira 上狀態為 `In Progress` 超過「設定的停滯時間（預設為 3 個工作天）」沒有任何進展的 Ticket，在看板上顯示明顯的紅色警示或閃爍效果，  
> **So that** 我能在站會指著那張「停滯的票」直接尋求技術支援或說明阻礙，不再把時間浪費在流水帳的工作回報上，進而縮短單一任務的 Cycle Time。

*(註：排除週末與國定假日等計算邏輯，將列入此功能的 Acceptance Criteria 中。)*

---

**後續行動建議：**
這兩份 User Story 已經具備清晰的使用者價值與邊界，您可以將其帶入 **Step 4: Acceptance Criteria (AC) 撰寫與規格展開**。
