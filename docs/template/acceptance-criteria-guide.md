# Acceptance Criteria 撰寫指引

## 與 User Story 的關係

Acceptance Criteria（驗收條件）是 **User Story 的具體化**，將抽象的使用者需求轉換為可驗證的具體條件。

### User Story → Acceptance Criteria 流程
```
User Story: 作為 [角色]，我希望 [功能]，以便 [價值]
       ↓
Acceptance Criteria: 具體描述「功能」如何運作的情境
```

**核心價值**：
- 明確定義 User Story 的「完成條件」
- 確保開發團隊理解需求細節
- 提供開發和驗收的共同基準

### 撰寫 AC 的好處
- **聚焦價值**：幫助 PO 與團隊聚焦於「使用者價值」與「行為預期」
- **避免誤解**：協助開發團隊避免過度詮釋或誤解需求
- **驗收基準**：提供明確的功能驗收條件，提供測試基礎
- **溝通橋樑**：成為產品、開發、QA 團隊的共同語言



## 撰寫原則

### 涵蓋情境
- **正常流程**：主要使用路徑
- **邊界條件**：數值上下限、空值處理
- **異常情況**：錯誤狀況、權限不足
- **安全控制**：未登入、權限驗證

### SMART 原則
| 原則 | 說明 |
|------|------|
| **S - Specific** | 具體明確的行為描述 |
| **M - Measurable** | 可驗證的結果 |
| **T - Testable** | 可執行的測試步驟 |

## 從 User Story 到 AC 的步驟

### 步驟 1：分析 User Story
```
User Story: 作為登入用戶，我希望能重設密碼，以便恢復帳戶存取權限
           ↓
分析要素：角色（登入用戶）、功能（重設密碼）、價值（恢復存取）
```

### 步驟 2：Clarification First Mode（AC 前釐清模式）

AI 不得直接產生 AC
必須先釐清再寫

在撰寫 Acceptance Criteria 前，AI 必須：
	1.	先閱讀 User Story
	2.	檢查是否存在資訊缺口
	3.	若有不足，提出 3–6 個具體釐清問題
	4.	等待使用者回答
	5.	才能進入 AC 撰寫階段

釐清問題應包含：
	•	角色前置狀態（登入？資料準備？權限？）
	•	使用情境（有哪些流程分支？）
	•	邊界條件（上限、下限、空值）
	•	異常狀況（錯誤、例外、API fail）
	•	格式規則（資料驗證）
	•	成功條件（什麼叫完成？）

範例（AI 應該提出的釐清問題）
	•	使用者需要先登入嗎？
	•	此功能是否涉及權限？
	•	有哪些可能的失敗情況？
	•	是否有資料格式或欄位限制？
	•	成功後系統需要呈現哪些資訊？

### 步驟 3：撰寫 AC，撰寫格式：Gherkin
```gherkin
場景：[簡要描述情境]
Given [前置條件]
And [額外前置條件]
When [用戶操作]
Then [預期結果]
And [額外驗證點]
```

## 範例

### User Story
```
作為註冊使用者，我希望能透過帳號密碼登入系統，以便存取我的個人儀表板
```

### 對應的 Acceptance Criteria

#### AC01: 成功登入
```gherkin
場景：使用者成功登入系統
Given 用戶已註冊帳號
And 用戶位於登入頁面
When 用戶輸入正確的帳號密碼
And 點擊登入按鈕
Then 系統應導向至儀表板頁面
And 顯示歡迎訊息
```

#### AC02: 帳號不存在
```gherkin
場景：登入不存在的帳號
Given 用戶位於登入頁面
When 用戶輸入不存在的帳號
And 點擊登入按鈕
Then 系統應顯示錯誤訊息 "帳號或密碼錯誤"
And 使用者停留在登入頁面
```

#### AC03: 密碼錯誤
```gherkin
場景：輸入錯誤密碼
Given 用戶已註冊帳號
And 用戶位於登入頁面
When 用戶輸入錯誤密碼
And 點擊登入按鈕
Then 系統應顯示錯誤訊息
And 密碼欄位應清空
```

## QA / RD / PM 的共同使用方式

AC 不是 QA 文件
是：
	•	PM 澄清需求的工具
	•	RD 理解範圍的工具
	•	QA 撰寫 test cases 的基礎

## AI 使用規則（Cursor / Claude Code 必備）

當 AI 實作 Acceptance Criteria 時，必須：

### Step 1：提出釐清問題（Clarification First）

→ 必問：資料、流程、邊界、異常、權限、成功條件

### Step 2：列出所有情境（Scenario Enumeration）

→ 正常 / 邊界 / 異常 / 權限 / 格式 / 空值

### Step 3：生成 Mapping 表（User Story → AC）

→ 確保需求全面覆蓋

### Step 4：經使用者確認後再寫 AC（Gherkin）

## 🔗 相關文件

| 文件 | 用途 |
|------|------|
| [feature-spec-template.md](./feature-spec-template.md) | 輕量功能規格模板（含 AC 撰寫） |
| [user-story-guide.md](./user-story-guide.md) | User Story 撰寫指引 |
| [testcase-guide.md](./testcase-guide.md) | 測試案例撰寫指引 |