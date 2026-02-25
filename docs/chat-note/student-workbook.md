# Sciwork 工作坊 操作步驟
## Step 0 AI IDE 練習讓 Agent 編輯程式
1, 這是第一個請 Agent 幫我編輯程式的練習
請在 @AI-IDE-practice-notes.md 放入我的名字跟日期
2, 請簡單描述這個專案的重點
3, 安裝 Extensions
    - Antigravity Quota
    - Mermaid
## Step 1 痛點分析

### Given
1, 參考 docs/reference/step0-painpoint-ref.md 痛點

### 操作
- 建立 Gemini Gem：建立 Gemini Gem
    - system prompts:
    - docs/template/gemini-gem-PM-1-painpoint-analysis-prompts.md
- 對話，貼上痛點，貼上至 Gemini Gem PM-1-用戶痛點分析助手
    - 痛點：
    - docs/reference/step0-painpoint-ref.md
- 回答 AI 詢問的問題
    - 舉例：還能生成其他假設嗎？
- 經過對話，複製最終版的痛點分析至
    - 痛點分析結果：
    - docs/lab-20260307/step1-painpoints-analysis.md

### 筆記
N/A

## Step 2 OST

### Given
1, 參考 step1-painpoints-analysis.md

### 操作
- 建立 Gemini Gem：建立 Gemini Gem
    - system prompts:
    - docs/template/gemini-gem-PM-2-ost-prompts.md
- 對話，貼上痛點分析報告，貼上至 Gemini Gem PM-2-Opportunity Solution Tree 助手
    - (1) 痛點分析報告：
    - docs/reference/step1-painpoints-analysis.md
    - 範例對話：
        - 以下是這次的痛點分析：貼上 (1) 痛點分析報告
        - 回答 AI 詢問的問題，也收斂至設計好的情境
    - 經過對話，複製最終版的 OST 至
        - OST 結果：
            - docs/lab-20260307/step2-ost-v1-all.md
        - 範圍再縮小：
            - (例如)我想先針對 Scope Change Waterfall（解決「老闆問為什麼做不完」的痛點，針對 PM/Lead）進行發想
            - 生成：docs/lab-20260307/step2-ost-v2-focus.md

### 筆記
OST 不要使用一次性的結果，請多跟 AI 對談，收斂出最終的版本

## Step 3 User Story

### Given
- 選項 A：已有 docs/reference/step2-ost-v2-focus.md
- 選項 B：自由想法（無需 OST 報告）

### 操作
- 建立 Gemini Gem：建立 Gemini Gem
    - system prompts: docs/template/gemini-gem-PM-3-userstory-prompts.md

- **對話模式選擇**：
    - **模式 A（結構化 OST）**：
        - 貼上 OST 報告至 Gemini Gem PM-3-User Story 助手
        - 範例對話：「這是最終版方案，請參考 (docs/reference/step2-ost-v2-focus.md)，跟我討論 User Story」

    - **模式 B（自由對話）**：
        - 直接說出想法，Gem 會提 4 個深層提問：使用者角色、優先級條件、使用情境、價值與成功
        - 無需提供 OST 報告

- 回答 AI 詢問的問題，檢查壞味道
    - 如品質不佳，請對 AI 說：「請針對 [特定痛點] 再深化價值的描述」

- 經過對話，複製最終版的 User Story 至
    - docs/lab-20260307/step3-userstory-v1.md

- 回填：User Story 結果貼在「小組 Google Sheet」

### 筆記
- User Story 不要使用一次性的結果，請多跟 AI 對談，收斂出最終版本
- **v2 支援雙軌模式**：可選 OST 結構化輸入或自由想法對話，彈性配合不同工作流程

## Step 4 問 AI 一個技術細節

**核心目的：** 體驗「之前只能問工程師，現在可以問 AI」

### 操作
1. 打開 AI IDE（Claude Code）

2. 帶著 User Story，**問 AI 一個具體的技術問題**
   - 例：「Status 在系統中的排序順序是什麼？」
   - 例：「Jira 資料轉移到 Google Sheet 時，各欄位的資料格式和儲存方式是什麼？」
   - 或選擇你在 User Story 中有疑問的其他技術細節

3. 與 AI 對話，記錄答案

4. 儲存筆記至 docs/lab-20260307/step4-askAI.md

### 筆記
- 這是一個短暫的「釐清體驗」，只需花 5-10 分鐘
- 目的是感受 AI 能回答工程相關的具體問題，為後續 Step 5 打基礎


## Step 5 Acceptance Criteria

### Given
1, 已有 `docs/lab-20260307/step3-userstory-v1.md`

### 操作

- **打開 AI IDE (Antigravity Claude Code / Cursor)**

- **對話**
    - 「我已經討論好的 User Story 在 `@docs/lab-20260307/step3-userstory-v1.md`，接下來請跟我討論 Acceptance Criteria。

- **釐清階段 (Clarification First)**
    - AI 會針對系統限制、邊界條件、異常狀況提出 3-6 個問題。

- **人工審查與產出 (Output)**
    - 確認 Mapping Table 覆蓋了所有 Story 需求點。
    - 正式產出 Gherkin 格式的 AC 文件：`docs/lab-20260307/step4-ac-v1.md`

### 筆記
- **不要直接生成 AC**：透過對話釐清系統限制，讓 AI 一步一步引導你完成 AC 的討論
- **Gherkin 格式**：使用 Given-When-Then 讓規格可測試且業務邏輯清晰。
- **系統限制對齊**：在產出 AC 前，先對齊系統限制，再產出規格。

## Step 6 PRD Draft

### Given
1, 已有完整的痛點分析 (step1-painpoints-analysis.md)
2, 已有 OST 報告 (step2-ost-v2-focus.md)
3, 已有 User Story (step3-userstory-v1.md)
4, 已有 Acceptance Criteria (step4-ac-scope-change-waterfall-v1.md)
5, 已有 PRD 製作指南 (docs/template/feature-spec-template-v2.md)

### 操作
1, 回到 AI IDE (Claude Code)

2, 提供所有前置文件的路徑，要求使用「逐題提問模式」協助產生 PRD
   - 格式：提供 @file 路徑引用
   - 說明使用的模板：feature-spec-template-v2.md
   - 範例：
   我想產出這個功能的 PRD，請用逐題提問模式協助我。
   這是痛點分析： @docs/reference/step1-painpoints-analysis.md 
   這是機會解決方案樹（OST）報告: @docs/reference/step2-ost-v2-focus.md 
   這是 User Story: @docs/reference/step3-userstory-v1.md 
   這是 Acceptance Criteria: @docs/reference/step4-ac-scope-change-waterfall-v1.md 
   PRD 的製作方式請參考 @docs/template/feature-spec-template-v2.md 

3, AI 將進行 7 個澄清問題（逐題提問）：
    3-1, 功能的核心目標 (Feature Goal)
    3-2, 主要使用者 (Primary User)
    3-3, 功能範圍 Scope
    3-4, Out-of-Scope
    3-5, 使用流程 Flow
    3-6, 系統行為 (System Behavior)
    3-7, 資料需求 (Data Requirements)

4, 對每個問題回答（可複選）
   - 格式：A, B, C 等字母或其他選項

5, 確認資訊整理結果

6, AI 將產生完整的 PRD Draft，包含：
   - 📝 功能概述（需求背景、功能描述、預期影響）
   - 📋 用戶故事（直接引用 User Story）
   - ✅ Acceptance Criteria（直接引用 AC）
   - 🎯 產品規格（功能邊界、業務邏輯、流程圖、相關文件）
   - 📊 成效追蹤（追蹤指標）
   - 📝 變更記錄

7, 將 PRD Draft 寫入 specs/{SPEC-ID}-{功能名稱}.md 檔案

### 筆記
- 逐題提問模式確保需求完整性，避免遺漏重要決策
- PRD Draft 應直接引用已確認的 User Story 和 AC，不要改寫
- 最終 PRD 需包含業務邏輯流程圖（使用 Mermaid）
- 完成後執行 git commit 儲存變更

## Step 7 Prototype

### Given
1, 已有 PRD

### 操作
我已經完成這一功能的 PRD。
現在請你協助我建立 Prototype，請依照 @docs/template/prototype-guide.md 的流程與規範來進行。
Prototype 請建立在獨立的 `docs/prototype/` 目錄下，並且不要影響正式程式碼。

請先：
1. 自動掃描專案前端架構（Framework / UI Library / Common Components）
2. 根據 PRD @PRD 整理 Prototype 的核心行為（但先不要寫 code）
3. 啟動「逐題釐清模式」，一次問我一個問題，並提供 A/B/C/D 選項讓我選擇。

等我回答完所有問題後，你再開始產生 Prototype

### 筆記

**重要發現：Prototype 放置位置的考量**

1. **不要放在 frontend/src/app/ 下**
   - 即使放在 `/prototype/` 子目錄，仍會被 Next.js 編譯
   - 會出現在 production build 中，影響正式程式碼

2. **正確做法：放在 docs/prototype/ 目錄**
   - 使用純 HTML/CSS/JavaScript
   - 不依賴任何 CDN 或外部資源
   - 可直接雙擊開啟，不需要 Python 或任何伺服器

3. **技術選擇**
   - 第一版用 React + Recharts CDN → 失敗（CORS 問題）
   - 第二版用 htm 替代 Babel → 仍失敗
   - 最終版用純 HTML/CSS/JS → 成功

4. **Prototype 檔案位置**
   - HTML 頁面：`docs/prototype/002-scope-change-waterfall.html`
   - 說明文件：`docs/prototype/002-scope-change-waterfall.md`

5. **互動功能**
   - Sprint 下拉選單切換
   - 懸停 Tooltip 顯示分類統計
   - 多種資料場景（正常/邊界/空狀態）

---

**Agent 會問的決策問題（共 7 題）**

| 問題 | 選項範例 |
|------|----------|
| Q1：Prototype 的呈現深度？ | A. 靜態 UI / B. 基礎互動 / C. 完整流程 / D. Mock API |
| Q2：畫面要如何安置？ | A. 獨立 HTML 於 docs/prototype/ / B. 放在 frontend/src/app/prototype/ / C. PM 指定 |
| Q3：風格希望如何處理？ | A. 完全依現有樣式 / B. 允許微調 / C. 試不同 Layout |
| Q4：假資料來源？ | A. 自動生成 / B. Mock API / C. 從 repo 找 / D. PM 提供 |
| Q5：是否需要流程提示？ | A. 不需要 / B. 需要 / C. 需要並顯示在 UI 上 |
| Q6：Prototype 用途？（可複選） | A. Demo 給自己 / B. 與工程 Alignment / C. 對主管 Pitch / D. 放進 PRD |
| Q7：是否需要 Demo 影片腳本？ | A. 要 / B. 不需要 / C. 等看到再決定 |

---

**Agent 執行的技術操作（學員不需自己執行）**

Agent 會自動執行以下技術操作，學員只需確認結果：

| 操作類型 | 指令範例 | 說明 |
|----------|----------|------|
| 建立目錄 | `mkdir -p docs/prototype` | 建立 prototype 目錄 |
| 刪除目錄 | `rm -rf frontend/src/app/prototype` | 刪除錯誤放置的檔案 |
| 編譯驗證 | `npm run build` | 確認程式碼正確 |
| 讀取檔案 | Read 工具 | 了解現有程式碼風格 |
| 建立檔案 | Write 工具 | 建立 HTML/MD 檔案 |
| 修改檔案 | Edit 工具 | 修改現有檔案 |

> **學員須知**：不需要自己執行這些指令！只需要：
> 1. 回答 Agent 的提問（選 A/B/C/D）
> 2. 確認產出是否符合預期
> 3. 遇到問題時告訴 Agent（例如「打開是空的」）
>
> Agent 會自己處理技術細節，包括除錯和修復。

---

## 環境變數設定

> ⚠️ **重要**: `.env` 檔案被 `.gitignore` 忽略，不會提交到 Git。以下是預設設定值。

### 後端環境變數 (`backend/.env`)

```bash
# Google Sheets 配置
GoogleSheets__SheetId=1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM
GoogleSheets__RawDataSheet=rawData
GoogleSheets__SprintSheet=GetJiraSprintValues

# 快取設定（秒數）
CacheDuration=300

# 伺服器配置
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

### 前端環境變數 (`frontend/.env`)

```bash
# API 端點
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# 應用程式名稱
NEXT_PUBLIC_APP_TITLE=Jira Dashboard
```

### 開發環境差異

**開發模式** (`docker-compose.dev.yml`)：
- Frontend API: `http://backend:8000/api`（容器內通訊）

**示範模式** (`docker-compose.yml`)：
- Frontend API: `http://localhost:8000/api`（本機連線）

### 修改環境變數的步驟

1. 編輯對應的 `.env` 檔案（`backend/.env` 或 `frontend/.env`）
2. 修改環境變數值
3. 重啟 Docker 容器：`docker-compose down && docker-compose up`
4. 確認變更生效