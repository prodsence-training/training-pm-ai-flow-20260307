# 🚀 AI Agent Product Discovery Framework

### —— Problem → Opportunity → Story → Criteria → PRD 的五階段探索流程

本框架是一套以 **AI 協作（ChatGPT / Claude / Gemini）** 為核心的
「產品探索與規格驗收（Product Discovery & Acceptance Criteria Definition）」方法論，用於協助 PM、設計師、與跨職能團隊：

* 更快釐清使用者問題
* 更深入探索機會與解法
* 更清楚拆解需求
* 更順利定義驗收條件
* 更有效串接到實作階段

Framework 共由 **五個對談式 AI Agent** 組成：

1. **Pain Point & Hypothesis Agent（問題探索）**
2. **OST Agent（機會探索）**
3. **User Story Agent（需求切片）**
4. **Acceptance Criteria Agent（驗收條件定義）**
5. **PRD Draft Agent（規格撰寫）**

這五個 Agent 串起來，就是一套完整的
**AI 版 Product Discovery + Specification Pipeline。**

---

# 🧩 Framework Overview（總覽）

產品探索與規格驗收通常分成五大階段：

1. **Problem Space（問題空間）**
2. **Opportunity Space（機會空間）**
3. **Solution Definition（需求定義）**
4. **Criteria Definition（驗收條件定義）**
5. **Specification Writing（規格撰寫）**

此 Framework 剛好將五個階段拆成五個 AI Agent。

---

# 🌱 Stage 1：Pain Point Discovery

### （AI Agent：痛點假設對談 Agent）

**目的：**
釐清使用者真正遇到的問題，而不是功能需求。

**輸入：**

* 訪談筆記
* 使用者抱怨
* PM 假設
* 行為紀錄
* 觀察

**輸出（Markdown 格式）：**

* 問題需求（Problem / Need）
* 使用者是誰（Target User）
* 痛點情境（Context）
* 痛點來源（Evidence）
* 痛點強度（Severity）
* 痛點對用戶的影響（Impact）
* 初步問題假設（Initial Hypothesis）

**定位：**
本階段只做「問題理解」
不做機會探索、不做解法、不寫指標。

---

# 🌳 Stage 2：Opportunity Solution Tree（OST）

### （AI Agent：OST 機會探索 Agent）

**目的：**
透過 Outcome → Opportunities → Solutions → Experiments
探索「問題背後的機會」，並避免跳到功能。

**輸入：**

* Step 1 的「痛點分析報告」

**輸出（Markdown 格式）：**

* Outcome（期望改善方向）
* Opportunities（使用者未被滿足的需求）
* Solutions（多元解法方向）
* Experiments（驗證方式）

**定位：**
本階段只做「機會探索與方向發散」

❌ 不決定功能
❌ 不寫 User Story
❌ 不寫 PRD
❌ 不寫驗收條件

👉 這些會在下一階段進行。

---

# 🧱 Stage 3：User Story Definition

### （AI Agent：User Story 對談 Agent）

**目的：**
將 OST 中 PM 選擇的「解法方向」
切成明確的 User Stories，作為之後 PRD & AC 的基礎。

**輸入：**

* Step 1（問題）
* Step 2（機會與解法方向）
* PM 所選擇的 Solution Area

**輸出（Markdown 格式）：**

* Selected Solution Area
* User Stories（As a / I want / so that）
* 使用情境（Scenarios）
* 任務流程（High-level Task Flow）
* Out of Scope

**定位：**
本階段只進行「需求切片」。

❌ 不寫 PRD
❌ 不寫 Acceptance Criteria（AC 交給下一階段）
❌ 不寫解法細節

---

# ✅ Stage 4：Acceptance Criteria Definition

### （AI Agent：AC 驗收條件對談 Agent）

**目的：**
根據 User Story，透過結構化的釐清對談（Clarification First Mode），
定義明確的驗收條件（Gherkin 格式），確保「何謂完成」。

**輸入：**

* Step 3 的「User Stories」
* 系統架構與資料結構文檔
* 專案的技術約束與限制

**輸出（Markdown 格式）：**

* 前置條件（Pre-conditions）
* AC 釐清問題（3-6 個具體問題）
* 場景列舉（Scenario Enumeration）
  * ✅ 正常流程
  * ⚠️ 邊界條件
  * ❌ 異常情況
  * 🔒 安全控制
* User Story → AC 對應表
* Gherkin 格式的 AC（Given-When-Then）

**流程方法：**

1. **Clarification First Mode（AC 前釐清模式）**
   - 先閱讀 User Story 與系統架構
   - 提出 3-6 個具體的釐清問題
   - 等待 PM/stakeholder 回答
   - 才能進入 AC 撰寫階段

2. **SMART 原則**
   - **S - Specific**: 具體明確的行為描述
   - **M - Measurable**: 可驗證的結果
   - **T - Testable**: 可執行的測試步驟

3. **場景覆蓋**
   - 涵蓋正常流程、邊界條件、異常狀況、安全控制

**定位：**
本階段只進行「驗收條件定義」。

❌ 不做實作設計
❌ 不寫 PRD
❌ 不決定 UI 細節

👉 AC 交給開發團隊作為實作基準。

---

# 📋 Stage 5：PRD Draft Definition

### （AI Agent：PRD 草稿撰寫 Agent）

**目的：**
將 Step 1-4 的成果（痛點分析、OST、User Story、AC）整合為完整的 PRD Draft，
並透過「逐題澄清模式」收斂所有關鍵決策，產出交付工程團隊實作的規格文檔。

**輸入：**

* Step 1 的「痛點分析報告」
* Step 2 的「OST 報告」
* Step 3 的「User Story 套件」
* Step 4 的「Acceptance Criteria」
* 技術架構與資料結構文檔

**輸出（Markdown 格式）：**

* 功能概述（需求背景、功能描述、預期影響）
* 用戶故事（直接引用 Step 3）
* Acceptance Criteria（直接引用 Step 4）
* 產品規格
  * 功能邊界（包含/不包含/影響範圍）
  * 業務邏輯（計算規則、判斷標準、狀態定義）
  * 業務邏輯流程圖（Mermaid）
  * 相關文件連結
* 成效追蹤（核心指標、觀察指標）
* 變更記錄

**流程方法：**

1. **逐題澄清模式（One-question-at-a-time）**
   - 一次只問一個關鍵決策問題
   - 提供 3～5 個可選項目
   - 等待 PM 回答後才進下一題
   - 確保所有決策都經過確認

2. **整合式檢查清單**
   - 綜合前四個階段的成果
   - 標記來源與引用關係
   - 確認無遺漏或衝突

3. **可操作性驗證**
   - 確保規格足夠清楚讓工程師理解
   - 確保每個 AC 都對應到規格中的相應邏輯
   - 確保業務邏輯流程圖與 AC 場景相符

**定位：**
本階段進行「規格整合與最終確認」。

❌ 不做進一步的需求發現
❌ 不寫實作代碼
❌ 不決定 UI 設計細節

👉 PRD Draft 交給設計與工程團隊，作為設計評審與開發實作的基準。

---

# 🔗 Framework Flow Diagram（Mermaid）

```mermaid
flowchart TD

    A[Step 1\nPain Point Analysis\n(問題探索)] --> B[Step 2\nOST\n(機會探索)]
    B --> C[Step 3\nUser Story Definition\n(需求切片)]
    C --> D[Step 4\nAcceptance Criteria\n(驗收條件)]
    D --> E[Step 5\nPRD Draft Definition\n(規格撰寫)]

    style A fill:#FFE2E2,stroke:#FF8A8A,stroke-width:2px
    style B fill:#FFF4CC,stroke:#FFC700,stroke-width:2px
    style C fill:#E2F5FF,stroke:#32A8FF,stroke-width:2px
    style D fill:#F0E8FF,stroke:#A56CFF,stroke-width:2px
    style E fill:#E8FFEF,stroke:#40C463,stroke-width:2px
```

---

# 📌 Responsibilities（五個 Agent 的分工）

| 階段     | Agent            | 任務        | 禁區（不做的事）                  |
| ------ | ---------------- | --------- | ------------------------- |
| Step 1 | Pain Point Agent | 問題分析、痛點定義 | 不產生解法、不寫 AC、不寫 PRD        |
| Step 2 | OST Agent        | 機會探索、解法發散 | 不寫 User Story、不做決策、不做技術規格 |
| Step 3 | User Story Agent | 需求切片、使用情境 | 不寫 PRD、不寫 AC、不寫 UI        |
| Step 4 | AC Agent         | 驗收條件定義、釐清對談 | 不做實作設計、不寫 PRD、不決定 UI   |
| Step 5 | PRD Draft Agent  | 規格整合、決策澄清、流程圖設計 | 不做需求發現、不寫實作代碼、不決定 UI |

---

# 🎯 Why This Framework Works（為什麼有效？）

* 📌 **避免 PM 一開始就跳功能**
* 📌 **讓問題、機會、需求三層分得清楚**
* 📌 **對接 AI 的能力（GenAI → AI IDE）**
* 📌 **每步都有清楚的 Input/Output**
* 📌 **能完全轉換成你的 SDD（Spec-Driven Development）流程**
* 📌 **非常適合教 PM（初學者、跨職能、企業內訓）**

---

# 🧩 Summary（全流程簡述）

1. **Step 1：痛點探索**
   → 找出問題本質：誰、在哪、為何痛？

2. **Step 2：OST**
   → 釐清問題背後有什麼機會可以改善？
   → 有什麼多元解法方向？

3. **Step 3：User Story**
   → 將選定的解法方向拆成可執行需求。

4. **Step 4：Acceptance Criteria**
   → 透過「釐清對談」確保「何謂完成」。
   → 用 Gherkin 定義可驗證的驗收條件。
   → 作為開發實作的明確基準。

5. **Step 5：PRD Draft Definition**
   → 整合 Step 1-4 的成果，透過「逐題澄清模式」收斂決策。
   → 撰寫完整的 Feature Spec，包含功能概述、規格、業務邏輯流程圖。
   → 確保工程團隊有明確的實作基準。
   → 交付設計評審與開發實作階段。

---

# 🎉 This is the AI-Agent Product Discovery Framework v3

現已支援 **PRD Draft Definition 階段**（Step 5）。

完整流程：Problem → Opportunity → Story → Criteria → PRD（五階段完整閉環）

歡迎在工作坊、顧問案、內訓或影片教學中直接使用。
