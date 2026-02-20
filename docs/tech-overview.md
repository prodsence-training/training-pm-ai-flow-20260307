# 技術架構概覽

本文件提供 Training Jira Dashboard MVP v1.0 專案的技術架構深度解析，旨在協助工程師快速理解系統設計、技術選型和實作細節。

## 專案概述

這是一個功能完整的 Jira Dashboard MVP v1.0 應用，採用現代化技術堆疊建構敏捷開發儀表板。專案整合 Google Sheets 作為真實資料來源，支援 Docker 容器化部署，專注於核心的統計視覺化功能。

### 專案定位
- **Jira Dashboard MVP v1.0**：生產就緒的 Dashboard 應用，整合 Google Sheets 真實資料
- **核心功能**：4 個關鍵指標卡片 + 1 個狀態分布圖表 + Sprint 篩選
- **Google Sheets Table**：完整的資料表格檢視功能
- **目標**：展示在嚴格資料限制下的 vibe coding 開發流程

## 系統架構圖

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Google Sheets     │────>│   Backend API    │────>│    Frontend     │
│ ┌─────────────────┐ │ CSV │  ( Python  )     │ API │   (Next.js)     │
│ │ rawData (23欄) │ │     │                  │     │                 │
│ │ GetJiraSprintV. │ │     │                  │     │                 │
│ └─────────────────┘ │     │                  │     │                 │
└─────────────────────┘     └──────────────────┘     └─────────────────┘
                                    │                           │
                                    ▼                           ▼
                              ┌──────────┐               ┌──────────┐
                              │  Cache   │               │Dashboard │
                              │ (5 min)  │               │Components│
                              └──────────┘               └──────────┘
                                                                │
                                                                ▼
                                                         ┌──────────┐
                                                         │4 Cards + │
                                                         │1 Chart + │
                                                         │Sprint    │
                                                         └──────────┘
```

## 技術堆疊

### 前端技術

| 技術 | 版本 | 用途 |
|------|------|------|
| **Next.js** | 15.2.4 | React 框架，使用 App Router |
| **React** | 19.0.0 | UI 函式庫 |
| **TypeScript** | 5.x | 型別安全 |
| **shadcn/ui** | latest | UI 元件庫（基於 Radix UI） |
| **Tailwind CSS** | 3.4.x | 實用優先的 CSS 框架 |
| **Recharts** | 2.x | 資料視覺化圖表 |
| **React Hook Form** | 7.x | 表單管理 |
| **Zod** | 3.x | Schema 驗證 |

#### 前端測試工具
| 技術 | 版本 | 用途 |
|------|------|------|
| **Jest** | 29.x | JavaScript 測試框架 |
| **React Testing Library** | 14.x | React 元件測試 |
| **@testing-library/jest-dom** | 6.x | DOM 測試擴充匹配器 |

### 後端技術

| 技術 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.11 | 執行環境 |
| **FastAPI** | 0.104.1 | 備用 Web 框架 |
| **Uvicorn** | 0.24.0 | ASGI 伺服器 |
| **Pandas** | 2.1.3 | 資料處理 |

#### 後端測試工具
| 技術 | 版本 | 用途 |
|------|------|------|
| **pytest** | 7.4.3 | Python 測試框架 |
| **pytest-asyncio** | 0.21.1 | 非同步測試支援 |
| **httpx** | 0.25.2 | 測試用 HTTP 客戶端 |

### 基礎設施

| 技術 | 用途 |
|------|------|
| **Docker** | 容器化 |
| **Docker Compose** | 容器編排 |
| **npm workspaces** | Monorepo 管理 |
| **Makefile** | 自動化指令 |

## Google Sheets 整合

### 資料存取機制

1. **無需 API 金鑰**：使用公開分享的 Google Sheets CSV 匯出 URL
2. **自動更新**：透過 5 分鐘快取機制平衡效能與即時性
3. **資料處理**：
   - CSV 格式自動解析
   - 日期時間欄位自動轉換
   - 數值型別智慧偵測
   - 欄位限制（僅讀取到 Column W）

## 資料來源架構

1. **資料表結構** (詳見 [table-schema.md](./table-schema.md))：
   - **rawData (23 欄位)**：主要 Issue 資料，從 Column A 到 W
   - **GetJiraSprintValues (9 欄位)**：Sprint 管理資料，從 Column A 到 I

### 嚴格資料架構限制

#### rawData 資料表（23 欄位嚴格限制）
**Vibe Coding 開發限制**：
- **欄位順序固定**：必須按照 1-23 順序存取，使用 `row[index]` 模式
- **禁止結構修改**：不可新增、刪除或重新排列欄位
- **類型安全**：string, number, date 三種類型，空值必須妥善處理
- **業務邏輯限制**：Status 必須為 9 個預定義狀態之一

### 狀態值順序

rawData 中的 Status 欄位限制為以下 **9 個固定狀態**（必須按此順序）：

| 順序 | 狀態值 | 說明 |
|------|--------|------|
| 1 | Backlog | 待處理工作項 |
| 2 | Evaluated | 已評估 |
| 3 | To Do | 待做 |
| 4 | In Progress | 進行中 |
| 5 | Waiting | 等待中 |
| 6 | Ready to Verify | 待驗證 |
| 7 | Done | 已完成 |
| 8 | Invalid | 無效 |
| 9 | Routine | 日常工作 |

**重要**：
- 任何不在此清單中的狀態值視為「無效狀態」
- 無效狀態會被計入 Total Issue Count，但排除於狀態分布圖表之外
- 狀態值順序不可改變

### 快取策略

為平衡效能與即時性，系統採用 **5 分鐘 TTL（Time To Live）** 的 in-memory 快取：

**快取配置**：
- **TTL**: 300 秒（5 分鐘）
- **儲存方式**: 記憶體內（進程重啟後清除）

**快取鍵格式**：
- `metrics:{sprint}` - 指標卡片資料
- `status-distribution:{sprint}` - 狀態分布資料
- `sprints:list` - Sprint 選項列表

**快取行為**：
- **自動過期**: 達到 TTL 時自動刪除
- **無手動清除機制**: 5 分鐘後自動更新資料
- **跨 Sprint 隔離**: 不同 Sprint 的快取獨立管理

**效能影響**：
- 首次請求：直接從 Google Sheets 讀取（較慢）
- 後續請求（5 分鐘內）：從快取讀取（快速）
- 5 分鐘後：自動重新從 Google Sheets 讀取

## 部署架構

### Docker 容器配置

```yaml
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8001
    
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - GoogleSheets__SheetId=1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM
      - GoogleSheets__RawDataSheet=rawData
      - GoogleSheets__SprintSheet=GetJiraSprintValues
      - CacheDuration=300
    
```

### 技術限制

1. **Google Sheets API 限制**：
   - 公開分享的安全性考量
   - 無法寫入資料（唯讀）
   - 大量請求可能觸發限流

2. **效能限制**：
   - 大量資料（>10,000 筆）的處理效能
   - 即時更新延遲（5 分鐘快取）

3. **功能限制**：
   - 無使用者認證機制
   - 無資料寫入功能
   - 無即時協作功能

4. **Vibe Coding 設計限制**：
   - 嚴格限制資料架構，不可修改 rawData 23 欄位結構
   - 強制使用 `row[index]` 存取模式，避免欄位名稱依賴
   - MVP 功能範圍限制：僅 4 個 Score Cards + 1 個 Bar Chart
   - 展示在真實約束條件下的快速開發能力

## 開發最佳實踐

### 程式碼規範

1. **前端**：
   - 使用 TypeScript 確保型別安全
   - 遵循 React Hooks 規則
   - 元件拆分保持單一職責

2. **後端**：
   - 使用 Python
   - 使用 FastAPI
   - 適當的錯誤處理和記錄

### Git 工作流程

1. 功能分支開發
2. 提交訊息遵循約定式提交
3. Code Review 流程
4. CI/CD 整合（GitHub Actions）

## 測試架構

### 測試策略

專案採用 Docker 容器內執行測試的策略，確保測試環境的一致性，學員無需在本地安裝測試工具。

## 相關文件

- [Table Schema 文件](./table-schema.md) - 詳細的資料表欄位說明
- [測試指南](./testing-guide.md) - 完整的測試框架說明與執行方式
- [CLAUDE.md](../CLAUDE.md) - AI 開發助手指引