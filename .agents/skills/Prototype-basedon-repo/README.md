# Prototype（Step 6）

基於既有系統建立可視化原型，讓團隊在正式開發前看見功能的樣貌。

## 用途

讀取既有專案的技術棧與設計模式，產出「長得像正式產品」的獨立 Prototype。支援 Web UI、CLI、API mock 等各類可視化原型。

## 觸發時機

- 完成 PRD / User Story，想在開發前先看見畫面或互動流程
- 需要 demo 給主管或團隊對齊方向
- 想快速驗證 UI 想法，但不想動到正式程式碼

## 核心特性

- **模仿優先**：掃描既有系統，產出風格一致的原型
- **環境感知**：自動偵測技術棧，建議最適合的 Prototype 方案
- **隔離原則**：Prototype 獨立存放，不污染正式程式碼
- **弱耦合**：有 PRD 最好，有想法也能開始
- **智慧跳題**：掃描後只問缺少的資訊

## 檔案說明

| 檔案 | 用途 |
|------|------|
| `SKILL.md` | Skill 核心指令與執行流程 |
| `examples/002-scope-change-waterfall.html` | 完整 Prototype 範例（Scope Change Waterfall Widget） |
| `examples/002-scope-change-waterfall.md` | 範例的說明文件（含截圖指南、PRD 對應表） |
| `references/prototype-guide-v1.2.md` | 原始 System Prompt 參考 |
