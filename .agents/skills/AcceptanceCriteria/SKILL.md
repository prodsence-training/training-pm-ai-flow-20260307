---
name: acceptance-criteria
description: "當需要為 User Story 撰寫 Acceptance Criteria 時觸發。預設使用 Clarification First 流程：先釐清需求再撰寫 AC。AC 由非技術 PM 撰寫，放入 PRD 或 Prototype，供 RD 設計技術文件、QA 撰寫測試案例。產出 Gherkin scenarios 和 Story → AC mapping table。"
license: "MIT"
---

# Acceptance Criteria

## 定位

AC 是 **PM 的溝通工具**——不是技術文件、不是測試案例。

- PM 撰寫 AC → 放入 PRD / Prototype
- RD 參考 PRD → 另外設計技術文件
- QA 參考 AC → 另外撰寫測試案例

AC 用純行為語言撰寫，非技術人員也能讀懂。禁止在 AC 中出現 API path、函數名、資料庫欄位等技術細節。

## 核心協議：Clarification First

**禁止直接生成 AC。** 必須依序完成四個步驟：

### Step 1：釐清問題

閱讀 User Story 後，提出 3–6 個釐清問題，涵蓋六大分類：

- **角色前置狀態**：登入？資料準備？權限？
- **使用情境**：有哪些流程分支？
- **邊界條件**：上限、下限、空值
- **異常狀況**：錯誤、例外、失敗情況
- **格式規則**：資料驗證
- **成功條件**：什麼叫完成？

**等待使用者回答後才進入下一步。**

### Step 2：列出所有情境

根據釐清結果，列出所有情境：正常 / 邊界 / 異常 / 權限。

### Step 3：生成 Mapping 表

產出 User Story → AC 對應表，確認每個需求點都被覆蓋。

### Step 4：經使用者確認後撰寫 AC

使用者確認情境清單和 Mapping 表後，才撰寫正式的 Gherkin scenarios。

## Codebase 探索

撰寫 AC 前，建議先探索相關的程式碼、PRD、spec 文件，以確保：

- AC 的情境基於真實的系統行為
- 邊界條件反映實際的限制
- 術語與現有文件一致

技術知識用於提升 AC 品質，但不暴露在 AC 文字中。

## 撰寫原則

| 原則 | 說明 |
|------|------|
| **S** - Specific | 具體明確的行為描述 |
| **M** - Measurable | 可驗證的結果 |
| **R** - Relevant（可追溯） | 每條 AC 都能對應回 Story 的某個需求點 |
| **T** - Testable | 可執行的測試步驟 |

## 產出物

### 1. Gherkin Scenarios

```gherkin
場景：[簡要描述情境]
Given [前置條件]
And [額外前置條件]
When [用戶操作]
Then [預期結果]
And [額外驗證點]
```

涵蓋：正常流程、明顯的邊界條件、異常情況、權限控制。

### 2. Story → AC Mapping Table

| User Story 需求點 | 對應 AC | 情境數 |
|---|---|---|
| [需求點] | AC01, AC02 | 2 |

確保每個需求點都被至少一條 AC 覆蓋。

## 範例

### User Story

```
作為註冊使用者，我希望能透過帳號密碼登入系統，以便存取我的個人儀表板
```

### AC01: 成功登入

```gherkin
場景：使用者成功登入系統
Given 用戶已註冊帳號
And 用戶位於登入頁面
When 用戶輸入正確的帳號密碼
And 點擊登入按鈕
Then 系統應導向至儀表板頁面
And 顯示歡迎訊息
```

### AC02: 帳號不存在

```gherkin
場景：登入不存在的帳號
Given 用戶位於登入頁面
When 用戶輸入不存在的帳號
And 點擊登入按鈕
Then 系統應顯示錯誤訊息 "帳號或密碼錯誤"
And 使用者停留在登入頁面
```

### AC03: 密碼錯誤

```gherkin
場景：輸入錯誤密碼
Given 用戶已註冊帳號
And 用戶位於登入頁面
When 用戶輸入錯誤密碼
And 點擊登入按鈕
Then 系統應顯示錯誤訊息
And 密碼欄位應清空
```

### Mapping Table

| 需求點 | 對應 AC |
|--------|---------|
| 帳號密碼登入 | AC01, AC02, AC03 |
| 存取儀表板 | AC01 |
| 錯誤處理 | AC02, AC03 |
