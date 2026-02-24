# 產品背景上下文示例：Web Dashboard

**用途**：Web Dashboard（資料來源：Google Sheet）的產品邊界定義
**對象**：供 OST Gem 或 User Story Gem 上傳使用

## 產品基本資訊

**產品名稱**：Web Dashboard（Jira 進度監控板）

**產品簡述**：展示 Jira 資料的 Web Dashboard，資料來源為 Google Sheet。幫助敏捷團隊實時掌握 Sprint 進度、風險和 Roadmap 狀態。

**核心用戶**：敏捷團隊中的工程師、PM、Scrum Master、管理層

---

## ✅ 你應該探索的解法範圍

在 OST 分析中，可以建議以下方向的解決方案（在此範圍內發散）：

- Dashboard UI 設計改進（版面、配置、視覺階層、色彩編碼）
- 新增的進度指標和可視化方式（如 Burndown、Roadmap 進展、風險指示、插單影響）
- 資料轉換與呈現邏輯（如何從 Google Sheet 的原始 Jira 資料轉換為有意義的指標）
- 資料篩選、分組、排序邏輯
- 實時更新、重整機制（與 Google Sheet 的同步策略）
- 不同角色的檢視客製化（Engineer view vs PM view vs Manager view）
- Dashboard 與原始資料的可追蹤性（使用者可清楚看到資料的來源）
- 在 Google Sheet 中新增計算欄位或衍生資料（若 Dashboard 需要新的指標或資料維度）

**具體例子**：
- 建立「各角色專用的 Dashboard 檢視」，讓工程師看到自己的進度，PM 看到 Roadmap 進展
- 設計「風險預警指標」，在 Day 3-5 就能識別 Sprint 延遲
- 建立「插單影響可視化」，量化插單對 Sprint 容量的侵蝕
- 設計「進度 vs 預期」的對比展示，讓偏差一目了然

---

## ❌ 絕對禁止建議超出範圍的解法

以下方向應該完全避免（超出產品邊界）：

- ❌ 改變客戶的 Jira 工作流程（如：改 ticket 狀態、改 sprint 定義、改優先度規則）
- ❌ 改變客戶的組織流程（如：改 standup 時間、改 sprint 長度、改工作方式）
- ❌ 客戶系統層面的改動（如：Jira 外掛設定、第三方工具整合、API 架構修改）
- ❌ 超出 Dashboard 展示與資料加工層的技術決策

**為什麼禁止**：
- 這些決策超出我們的產品邊界
- 我們無法控制客戶的組織流程或 Jira 設定
- 我們的價值在於「可視化」而非「改變工作方式」

---

## 核心問題框架

在 OST 分析中，始終聚焦於以下核心問題：

> 「**我們的 Dashboard 如何將 Google Sheet 中的 Jira 資料轉化為可理解、可操作的視覺化資訊，幫助用戶及時發現風險、做出更好的決策？**」

而非「Jira 或 Google Sheet 或客戶的工作方式應該怎麼改」。

