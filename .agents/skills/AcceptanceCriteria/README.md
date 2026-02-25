# Acceptance Criteria（Step 4）

從 User Story 撰寫驗收條件，確保需求清晰可測試。

## 用途

為 User Story 定義驗收標準，確保開發與測試能精確理解需求。AC 由 PM 撰寫，以非技術的行為語言表達，放入 PRD 或 Prototype，供 RD 和 QA 參考。

## 觸發時機

- 完成 User Story，需要定義驗收條件
- 開發前需要明確「完成的定義」
- 要撰寫 Gherkin scenario 或 BDD 測試
- 需要產生 Story → AC 對應表確保需求覆蓋

## 核心特性

- **Clarification First 流程**：禁止直接寫 AC，必須先釐清需求
- **四階段執行**：釐清問題 → 列出情境 → 生成 Mapping 表 → 撰寫 AC
- **六大釐清角度**：角色前置狀態、使用情境、邊界條件、異常狀況、格式規則、成功條件
- **PM 導向文件**：非技術語言，禁止出現 API path、函數名、資料庫欄位
- **可測試的 Gherkin scenarios**：支援自動化測試

## 檔案說明

| 檔案 | 用途 |
|------|------|
| `SKILL.md` | Skill 核心指令與執行流程 |
| `examples/` | 輸入/輸出範例（建置中） |
| `references/` | Gemini Gem 版本參考（建置中） |
