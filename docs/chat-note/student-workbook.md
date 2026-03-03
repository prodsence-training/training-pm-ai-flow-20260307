# Sciwork 工作坊 操作步驟

---

## ⚡ 課堂快速指令（保存此頁面！）

### 啟動示範應用

```bash
docker compose -f docker-compose.prod.yml up
```

### 訪問儀表板

瀏覽器打開：`http://localhost:3000`

### 關閉應用

Terminal 按 `Ctrl + C`

---

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

## Step 6 PRD Draft (Skill 版)

### Given
1. **前置材料（越多越好）**：痛點分析 (Step 1)、User Story (Step 3)、Acceptance Criteria (Step 4)。
2. **PRD Draft Skill**：確保 AI 已載入對應的專用 Skill。

### 操作
1. **啟動 PRD Skill**：
   直接告知 AI 你想開始討論 PRD 並引用相關材料。
   *範例：*「我想針對這個功能討論 PRD，請根據 `@docs/lab-jugg-example/` 裡的 step1, step3, step4 材料來引導我。」

2. **智慧澄清與跳題 (Smart Clarification)**：
   - AI 會自動解析現有材料，**自動跳過**已知的背景資訊。
   - 對於材料中隱含的邏輯，AI 會標註 **(AI 推論)** 並請你確認。
   - AI 只會針對真正缺少的關鍵資訊（如：Metrics、具體邊界、Out-of-Scope）提出澄清問題。

3. **確認資訊整理摘要**：
   在正式產出文件前，AI 會整理一份結構化摘要，包含功能目標、主要使用者、Scope、成效指標等。請確認摘要是否正確。

4. **產出正式 PRD Draft**：
   確認摘要後，AI 會依照 `SPEC-XXX Feature Spec` 模板產出正式文件。
   *建議存放路徑：* `docs/lab-jugg-example/from-skills-step5-prd.md`

### 筆記
- **PRD 是翻譯而非創作**：核心價值在於將探索成果轉化為工程規格，應**原文引用** User Story 與 AC，不隨意改寫。
- **透明推論**：留意 AI 的「(AI 推論)」，如果不符合業務現況應立即修正。
- **規格優先 (Spec-Driven)**：完成後檢查 PRD 是否包含業務邏輯流程圖（Mermaid），這對開發釐清 if-else 邏輯非常有幫助。

## Step 7 Prototype

### Given
1, 已有 PRD

### 操作
- **啟動 Prototype Skill**：
  直接告知 Agent 你想針對 PRD 建立 Prototype。
  *範例對話*：「我已經完成這一功能的 PRD @[PRD 文件路徑]，現在請協助我建立 Prototype。」

- **Phase 1：環境掃描（自動執行）**
  AI 會自動掃描技術棧（Framework、UI Library）與現有設計模式。

- **Phase 2 & 3：需求澄清與確認**
  AI 會啟動「逐題釐清模式」，詢問模式選擇（Direct/Isolated）、呈現深度、假資料策略等。請根據需求回答。

- **Phase 4：產出 Prototype**
  確認設計摘要後，AI 會自動產出程式碼、說明文件以及 Demo 腳本。

### 筆記

**1. 模式與位置提醒（重要！）**
根據 Skill 的設計，請遵循以下存放路徑以確保隔離：

- **Direct Mode (直接修改模式)**
  - 路徑：`frontend/src/app/prototype`
  - 適合：快速示範、React 元件對齊。
  - **⚠ 注意**：會被 Next.js 編譯，**完成後必須 Git 還原，請勿 commit**。
- **Isolated Mode (獨立隔離模式)**
  - 路徑：`frontend/public/`
  - 適合：零污染、長期保留、純 HTML 預覽。
  - **🚀 訪問**：`http://localhost:3000/[filename].html`

**2. 核心原則：模仿與隔離**
- **不要從零開發**：優先掃描系統既有設計語言（如 shadow-md, blue-600）與卡片組件。
- **資料策略**：優先使用假資料 (Hardcoded)，避免動到後端 API 或資料庫。
- **Demo 腳本**：產出的 Demo 腳本對與工程師進行「技術對齊 (Alignment)」非常有幫助。

---

**Agent 會問的決策問題（共 7 題）**

根據 Prototype Skill 的 Phase 2 澄清需求，Agent 會詢問以下問題。其中 Q1-Q4 為必問，Q5-Q7 為按需提問：

| 問題 | 必問 | 選項範例 |
|------|------|----------|
| Q1：Prototype 的呈現深度？ | ✅ | A. 只要靜態畫面 / B. 基礎互動（切換、展開） / C. 完整流程含假資料 / D. 接 Mock API |
| Q2：Prototype 要放在哪裡？ | ✅ | A. Isolated Mode（frontend/public/） / B. Direct Mode（frontend/src/app/prototype/） / C. 其他位置 |
| Q3：假資料來源？ | ✅ | A. 自動生成假資料 / B. 從 repo 找 sample data / C. 自己提供 / D. Mock API |
| Q4：Prototype 用途？（可複選） | ✅ | A. 自己看 / B. 和工程團隊對齊 / C. 對主管 Pitch / D. 放進 PRD / E. 錄 Demo |
| Q5：風格處理？ | 按需 | A. 完全依現有樣式 / B. 允許微調 / C. 試不同 Layout |
| Q6：是否需要流程提示？ | 按需 | A. 不需要 / B. 需要（無提示） / C. 需要並顯示在 UI 上 |
| Q7：是否需要 Demo 操作腳本？ | 按需 | A. 需要 / B. 不需要 / C. 先看 Prototype 再決定 |

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

## 課堂快速啟動

> 📌 **給 PM 學員**：你只需要看著現有系統運行。最快的方式是使用預構建版本。

### 課堂啟動（推薦 ⭐）

```bash
# 進入專案資料夾
cd training-pm-ai-flow-20260307

# 啟動預構建版本（最快）
docker compose -f docker-compose.prod.yml up
```

✅ **優點**：
- 不需要重新構建，啟動快
- 適合課堂演示和教學環境

### 首次使用前提準備（講師或開發者執行一次）

如果是第一次使用，講師可能需要先構建 images：

```bash
# 構建預構建版本的 images（一次性）
./scripts/build-docker.sh v1.0

# 之後課堂上就可以快速啟動
docker compose -f docker-compose.prod.yml up
```

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
3. 重啟 Docker 容器：`docker compose down && docker compose up`
4. 確認變更生效