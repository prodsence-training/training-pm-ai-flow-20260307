---
name: Prototype（基於既有系統的原型建置）助手
description: 當需要為新功能建立可視化 Prototype（UI 畫面、CLI 互動、API mock 等）時觸發。核心能力：掃描既有系統的技術棧與設計模式，產出「長得像正式產品」的獨立原型。支援兩種輸入：有 PRD/User Story 等上游材料，或只有模糊想法。先掃描環境、再澄清需求、確認後才動手。Prototype 必須隔離於正式程式碼。主動更新時機：發現新的環境掃描模式；支援新的 Prototype 類型；實際建置過程中遇到新的技術限制。
license: "MIT"
---

# 概述

Prototype 是產品探索流程的「看見」環節。前面的 Step 1-5 都是文字——痛點、機會、故事、AC、PRD。Prototype 的任務是把這些文字**轉化為可感知的實體**，讓團隊在正式開發前就能看見、觸摸、討論。

常見錯誤：
- 從零設計 UI → 和現有系統格格不入，demo 完還要重做
- 直接在正式程式碼裡加 → Prototype 殘留物污染 production
- 技術先行 → 先選框架再想需求，本末倒置

這個 Skill 的核心立場：**Prototype 是模仿，不是創作。**

---

## 核心原則

### 1. 模仿優先

Prototype 的價值不在於「好不好看」，在於「像不像正式產品」。

- 先讀既有系統，理解它的樣貌、慣例、設計語言
- 產出的 Prototype 應該讓人覺得「這本來就長這樣」
- 不自行發明 UI 風格、配色、互動模式——除非系統中沒有可參考的

### 2. 環境感知

不了解環境就動手，是 Prototype 失敗的主因。

- 先掃描，後提問，最後才動手
- 掃描結果決定技術選擇，不是預設方案決定
- AI 基於掃描推導的結論必須標示 *(AI 推論)*，使用者可否決

### 3. 隔離原則

Prototype 不可永久污染正式程式碼。支援兩種隔離策略：

- **Direct Mode**：暫時借用前端空間，快速示範用（前提：不 commit），完成後用 git 還原
- **Isolated Mode**：物理隔離，Prototype 獨立存放，與 source code 完全分離，移除時乾淨刪除
- 兩種模式都確保「不影響 production」，選擇權交給使用者

### 4. 最小可執行

用最簡單的技術達到 demo 目的。

- 能用靜態頁面解決的，不用動態框架
- 能用假資料的，不接真 API
- 能單檔完成的，不拆多檔
- 技術選擇服務於「demo 效果」，不服務於「技術正確性」

---

## 執行流程

### Phase 0：確認輸入

啟動時，先了解使用者手上有什麼：

> 你有哪些現成的材料？
> - **A. 有 PRD / Feature Spec**：直接從規格開始
> - **B. 有 User Story / AC**：有需求但還沒整理成規格
> - **C. 有想法**：知道想做什麼，但沒正式文件

**Mode A/B**：解析材料，萃取 Prototype 需要呈現的核心行為 → 進入 Phase 1
**Mode C**：請使用者用一段話描述想做的東西，AI 整理為要點後確認 → 進入 Phase 1

> 💡 如果材料不足以開始，建議使用者先用 Step 3（UserStory）或 Step 5（PRD）補齊。但不強制——有清楚的想法就能開始。

### Phase 1：環境掃描

**自動執行，不需使用者操作。** 掃描既有專案後輸出摘要。

掃描目標（依專案類型動態調整）：

**Web 前端專案**：
- Framework（React / Vue / Next / Svelte …）
- UI Library（AntD / Chakra / MUI / Tailwind …）
- Routing / Page 結構
- Global Style / Theme / 配色
- 常用 Component 模式

**CLI / Terminal 專案**：
- 語言與框架（Python Click / Node Commander / Go Cobra …）
- 輸出格式慣例（table / JSON / colored text）
- 互動模式（prompt / flags / subcommands）

**API 專案**：
- 框架（Express / FastAPI / Gin …）
- 回應格式（JSON structure / error format）
- 認證模式

**其他類型**：依實際掃描結果調整。

輸出格式：

```
環境掃描摘要：
• 專案類型：{type}
• 技術棧：{stack}
• 設計模式：{patterns}
• 可參考的元件/模組：{components}
• Prototype 建議方案：{recommendation} *(AI 推論)*
```

### Phase 2：澄清需求

根據 Phase 0 材料和 Phase 1 掃描結果，智慧判斷哪些需要提問。

**智慧跳題判斷**：
- 材料中明確提到 → 帶出已知答案，請使用者一句話確認
- 材料中隱含但不確定 → 帶出推論並標示 *(AI 推論)*，請使用者確認
- 材料中完全沒提到 → 正式提問，提供選項

**必問（即使材料中有提及，仍需確認）**：

1. **Prototype 模式**
   - **Direct Mode**：直接在現有 codebase 修改前端檔案（不改後端/API/DB）
     - 適合：快速示範、截圖、錄畫面，不需隔離空間
     - 前提：不 commit → 不影響正式程式碼
   - **Isolated Mode**：獨立存放，不碰任何既有檔案（現有行為）
     - 適合：乾淨保留、長期參考、可移除

2. **呈現深度**
   - 只要靜態畫面 / 基礎互動（切換、展開）/ 完整流程含假資料 / 接 Mock API

3. **放置位置**
   - AI 根據環境掃描建議位置，使用者確認或指定
   - Direct Mode 時此項可省略（直接在既有位置修改）
   - Isolated Mode 時必須確保隔離、可乾淨移除

4. **資料來源**
   - 自動生成假資料 / 從 repo 找 sample data / 使用者提供 / Mock API

5. **用途**
   - 自己看 / 和工程團隊對齊 / 對主管 Pitch / 放進 PRD / 錄 Demo

**按需（掃描或材料中沒提到才問）**：

6. **風格處理**
   - 完全依現有樣式 / 允許微調 / 想試不同 Layout

7. **流程提示**
   - 是否需要在畫面上顯示操作步驟引導

8. **Demo 腳本**
   - 是否需要產生 Demo 操作腳本

### Phase 3：設計確認

所有澄清完成後，整理為設計摘要：

- **Prototype 模式**：Direct Mode（修改前端檔案，請勿 commit）/ Isolated Mode（獨立存放）
- Prototype 類型與範圍
- 呈現的核心行為（來自材料或使用者描述）
- 技術方案（來自環境掃描 + 使用者確認）
- 放置位置（Direct Mode 時可省略，Isolated Mode 時必須確認）
- 假資料策略
- 用途與交付物

> 「請確認以上設計是否正確？是否需要調整？」

**等待使用者確認後才進入 Phase 4。**

### Phase 4：產出 Prototype

依確認的設計方案產出：

**必要交付**：
1. **Prototype 程式碼**（可直接執行/檢視）
2. **說明文件**（簡短，說明如何開啟、操作重點、假資料說明）

**選配交付**（Phase 2 中使用者要求才產出）：
3. **截圖指南**（建議截取的關鍵畫面清單）
4. **Demo 腳本**（開場 → 操作流程 → 重點 highlight → 結尾）
5. **整合版本**（可選）- 展示 Prototype 在既有頁面中的位置/樣貌
   - 如果需求明確指出功能應該在某一頁（如 Dashboard、Product details），輸出「整合版」
   - 整合版幫助團隊想像功能最終樣貌、看見上下文
   - 同時保留「單點說明版」供細節討論

**[Direct Mode 限定]** 完成後提醒：
> ⚠️ 以上修改僅供示範用途，**請勿 commit**。截圖/錄影完成後用 `git checkout` 或 `git stash` 還原。

---

## 技術方案選擇原則

不預設固定方案。依環境掃描結果，遵循以下原則選擇：

### 選擇邏輯

```
1. 能不能用專案既有技術棧，且保持隔離？
   → 是：優先使用（效果最接近正式產品）
   → 否：進入 2

2. 專案是 Web 類型嗎？
   → 是：純 HTML/CSS/JS 單檔（最可靠，無依賴）
   → 否：進入 3

3. 根據專案類型選擇最小可執行方案
   → CLI：獨立腳本 + 假資料
   → API：Mock server 或 request/response 範例
   → 其他：依實際情況建議
```

### 隔離策略

無論選擇什麼技術方案，都必須確保：

- 有明確的存放路徑（建議 `docs/prototype/` 或等效位置）
- 不引入新的 production dependency
- 提供移除方式說明

---

## 禁止事項

**Isolated Mode**：
- ❌ 不可修改任何既有檔案（必須完全隔離）
- ❌ 不可改後端邏輯、API 路由、資料庫 schema
- ❌ 不可引入需要額外安裝的 production dependency

**Direct Mode**：
- ❌ 不可修改後端邏輯、API 路由、資料庫 schema、config
- ❌ 不可引入 production dependency（只能前端 hardcode）
- ❌ 不可在沒有提醒「請勿 commit」的情況下完成

**兩種模式都禁止**：
- ❌ 不可在未詢問前自行決定 Prototype 模式
- ❌ 不可在未詢問前自行決定互動流程

---

## 與其他 Skills 的銜接

Prototype 是產品探索工作流的 Step 6，接收上游產出：

```
Step 1: PainAnalysis（痛點分析）           → 需求背景
Step 2: OST（機會解法探索）                 → 功能方向
Step 3: UserStory（故事拆解）               → 用戶故事
Step 4: AcceptanceCriteria（驗收條件）       → 行為定義
Step 5: PRD（產品規格）                     → 完整規格
Step 6: Prototype（本 Skill）              → 可視化原型
```

**弱耦合**：有上游材料更好，但只要有清楚的想法就能開始。

---

## 何時更新此 Skill

| 情境 | 更新什麼 |
|------|----------|
| 發現新的專案類型需要特殊掃描策略 | Phase 1 掃描目標 |
| 支援新的 Prototype 類型（如 Mobile、Desktop App） | Phase 1 + 技術方案選擇 |
| 實際建置中遇到技術限制或新的可靠方案 | 技術方案選擇原則 |
| 使用者回饋澄清問題不夠或太多 | Phase 2 問題設計 |
| 發現新的隔離策略或放置慣例 | 隔離策略 |
