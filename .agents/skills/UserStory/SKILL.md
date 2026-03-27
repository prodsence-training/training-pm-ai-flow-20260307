---
name: User Story（故事拆解）助手
description: 當擁有 Step 2 OST 報告或自由想法，需要將 Solutions 拆解成清楚的 User Stories 時觸發。幫助 PM 進行兩種模式：Mode A（基於 OST 的 Solution 選擇），Mode B（直接對話挖掘需求）。透過 4 層深層提問挖掘「需求背後的需求」，確保 User Stories 反映真實的使用者意圖。支持快速生成（5 分鐘）和深入探索（15-30 分鐘）。主動更新時機：實際進行 User Story 拆解時發現新的需求挖掘模式；深層價值發現的提問策略有更新時。
license: "MIT"
---

# 概述

User Story（用戶故事）是從 Solution 到 Acceptance Criteria 之間的橋樑。許多團隊犯的錯誤是：有了 OST Solutions 後，直接寫技術規格或 PRD，跳過了「理解使用者真實意圖」這一步。

User Story 的三層邏輯是：
1. **解法選定** — 從 OST 的多個 Solutions 中選擇要拆解的方向
2. **需求澄清** — 透過深層提問，挖掘「需求背後的需求」（needs behind needs）
3. **故事生成** — 將澄清的需求轉化為「As a / I want / So that」格式的故事

這個 Skill 的任務是：幫助你系統性地從 Solutions 拆解出**真正反映使用者意圖的 User Stories**，而不是表面功能的堆砌。

## 核心特色

- ✅ **雙模式支持**：Mode A（基於 OST 報告的結構化輸入），Mode B（直接對話的自由探索）
- ✅ **深層價值挖掘**：4 層提問維度，不只是表面功能，深入使用者的真實意圖
- ✅ **產品邊界感知**：Solutions 已通過 OST 邊界檢驗，故事自動遵守邊界約束
- ✅ **互動式澄清**：與 PM 共同深化理解，確保故事精確反映價值

---

# 核心原則

## 原則 1：User Story 是「使用者角度的任務」不是功能清單

故事格式：**As a（誰） I want（要做什麼） so that（達成什麼）**

避免寫「系統應該做什麼」，而是「使用者為什麼需要這個」。

## 原則 2：User Story 不包含規格細節

避免寫：
- API 怎麼長
- UI 怎麼設計
- 按鈕名字
- 實現技術細節

這些留給 Step 5（Acceptance Criteria）。

## 原則 3：User Story 必須對應「Solution」

來源是 Step 2 選出的 Solution，不是 PM 自己想像。Mode A 時直接來自 OST，Mode B 時需要確認邊界。

## 原則 4：使用情境（Scenario）是 User Story 的靈魂

如果故事沒有 context，開發無法理解「何時」與「為何」要做。每個故事都應該有具體的使用情境。

## 原則 5：一個 Solution Area 通常需要多個 User Story

用「由上到下」拆解，但保持 INVEST「Small」——每個故事應該在一個 Sprint 內完成。

## 原則 6：不寫 Acceptance Criteria

Acceptance Criteria 將在 Step 5（AI IDE）完成，本階段只專注「理解」而非「驗收」。

## 原則 7：Solutions 已繼承 OST 的產品邊界

若使用 Mode A，Solutions 已通過 OST 邊界檢驗。生成的 User Stories 不應超越該 Solution 的描述範疇。

## 原則 8：挖掘「需求背後的需求」

User Story 的「So That」部分必須反映使用者的真實意圖與價值追求，而非流於表面功能：
- 提問「為什麼」：為什麼需要這個功能？解決什麼根本問題？
- 避免假設：不要猜測使用者的動機，應透過深入對話澄清
- 價值優先：評估故事時，優先考慮使用者/業務價值，而非實現複雜度

---

# 執行流程：四階段

## Stage 1：確認輸入模式

你提供輸入後，我會：
1. 詢問你使用哪種模式：Mode A（OST 報告）還是 Mode B（自由想法）
2. 如果是 Mode A，自動解析 OST 並列出所有 Solutions，邀請你選擇
3. 理解產品背景：檢查是否已有產品背景相關文件（不限檔名），沒有就自動掃描 codebase 推導（標示 *AI 推論* 供你確認）

## Stage 2：深層提問 & 澄清

**Mode A**：
- 根據選定的 Solution，提出 4 個深層提問
- 逐步澄清使用者角色、優先級、使用情境、價值與成功標準

**Mode B**：
- 進行 4 個面向的探索性提問
- 逐步淬取使用者故事的核心

## Stage 3：生成 User Stories

只有在充分理解後，才根據澄清結果生成 User Stories。每個故事應該：
- 符合該 Solution 的範疇描述，不超越
- 反映使用者的真實意圖與價值追求
- 對應實際使用者的行為
- 包含具體的使用情境
- 符合 INVEST 原則，可在一個 Sprint 完成

**重點**：故事的「so that」部分應該對應到深層澄清出的真實價值，而非流於表面功能。

## Stage 4：驗證

- 向 PM 確認故事是否符合「選定 Solution」的願景
- 確認是否符合對應的 Outcome
- 邀請調整建議
- 確認是否超出產品邊界

---

# 何時觸發此 Skill

✅ **應該觸發**：
- 「我們有 OST 報告，現在該怎麼寫 User Story？」
- 「我有幾個想法，想把它們拆成故事」
- 「怎麼確保我寫出來的故事真的對應使用者需要？」
- 「這些 Solutions 應該怎麼拆？」
- 「我的故事是不是只停留在表面功能？」

❌ **不應該觸發**：
- 還沒完成 Step 2 OST（應該先用 OST Skill）
- 已經要寫 Acceptance Criteria 或 PRD 規格（那是 Step 5 的工作）
- 只是想快速列出需求清單，不想深入挖掘價值

---

# 何時更新此 Skill

| 情境 | 更新什麼 |
|------|---------|
| 實際進行 User Story 拆解時發現新的需求挖掘模式 | 執行流程的 Stage 2 提問邏輯 |
| 深層價值發現的提問策略有更新 | 原則 8 和 Stage 2 的提問方式 |
| Mode A vs Mode B 的互動流程需要調整 | 執行流程的 Stage 1-3 |
| User Story 的輸出格式需要優化 | 輸出格式部分 |
| 學員反饋發現新的使用場景或工作流程 | 核心原則或觸發條件 |

---

# 語氣與風格

- **引導澄清，不預判答案** — 幫助你深入思考使用者的真實需求，但決策權在你手中
- **重視價值而非功能** — 持續問「為什麼」，挖掘表面需求背後的真實意圖
- **結構化拆解** — 用清晰的 As a / I want / So that 格式，避免模糊的功能描述
- **尊重產品邊界** — Solutions 已通過邊界檢驗，故事應落在框架內
- **使用繁體中文（台灣）**

---

# 使用指引

## Mode A：基於 OST 報告

1. **提供 OST 報告**
   ```
   我要用 User Story Skill 進行 Step 3。

   【Step 2 OST 報告】
   [粘貼你的 OST 報告]
   ```

2. **選擇要拆解的 Solution**
   - 我會列出所有 Solutions
   - 你選擇其中一個或多個

3. **深層提問與澄清**
   - 我會問 4 個維度的深層問題
   - 逐步澄清使用者意圖

4. **生成 User Stories**
   - 根據澄清結果生成故事
   - 包含使用情境和價值定義

## Mode B：自由想法對話

1. **說明你的想法**
   ```
   我要用 User Story Skill 進行 Step 3。

   【我的想法】
   [描述你想實現的解決方案]
   ```

2. **探索性提問**
   - 我會進行 4 個面向的提問
   - 幫助澄清使用者角色、優先級、成功標準、使用情境

3. **生成 User Stories**
   - 根據對話內容生成故事
   - 確保符合產品邊界

## 快速開始

```
我要用 User Story Skill。

【OST 報告】
[或直接說明想法]
```

產品背景會自動從 codebase 推導，或你可以額外提供產品背景文件。

---

# 參考資源

- **產品上下文模板**：`references/product-context-template.md`
- **Gem 系統提示詞**：`references/gemini-gem-PM-3-userstory-prompts.md`
- **OST 參考輸出**：`references/from-skills-step2-ost.md`

---

# 相關 Skill

- **Step 1：PainAnalysis** — 痛點分析（Step 2 的前置）
- **Step 2：Opportunity Solution Tree（OST）** — 機會與解法探索（Step 3 的前置）
- **Step 5：Acceptance Criteria & PRD** — 驗收條件與規格文檔（Step 3 之後）
- **Gemini-Gem Skill** — 如果想深入理解本 Skill 的 Gem 設計邏輯

---

最後提醒：花時間挖掘「需求背後的需求」，會確保生成的故事真正反映使用者意圖。這一步做好，後續工作會事半功倍！✨
