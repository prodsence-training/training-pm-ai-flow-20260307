# OpportunitySolutionTree Gem 版本歷史

## v2（當前版本）

**發布日期**：2026-02-23
**檔案**：`gemini-gem-PM-2-ost-prompts-v2.md`

### 改進說明

相較於 v1 版本，v2 進行了以下重新結構化：

- ✅ **5-Section 標準模板化**：重新組織為 Gemini Gem 官方標準（Role → Goal → Principles → Execution → Output）
  - 更易識別和維護
  - 便於在不同平台（Claude Code、Antigravity 等）重新適配

- ✅ **強化防呆機制**：
  - 在「絕對禁區」部分明確列出 4 個禁止項目
  - 每個原則都包含「說明」和「執行方式」兩層

- ✅ **清晰的 Stage 流程**：
  - Stage 1：資訊檢查與探索式提問（先問後答）
  - Stage 2：需求澄清與協作對話
  - Stage 3：生成完整 OST 報告

- ✅ **完整的 Output Format**：
  - 文字版本：Markdown 樹狀結構
  - 視覺化版本：Mermaid 樹狀圖
  - 使用範例：敏捷團隊 Sprint 進度的完整 OST 案例

- ✅ **保留原始設計邏輯**：
  - 所有核心概念（Outcome Calibration、Opportunity Clustering、Solution Diversity、Experiments）保持不變
  - 只是重新組織為結構更清晰的格式，更易在 Gemini 中執行

### 使用方式

直接複製 `gemini-gem-PM-2-ost-prompts-v2.md` 的完整內容（Role 到 Output Format），貼入 Google Gemini 的系統提示詞設定。

---

## v1（歷史版本）

**檔案**：`gemini-gem-PM-2-ost-prompts.md`

原始版本，包含完整的 OST 方法論和概念示例。v2 是基於 v1 重新結構化而成。
