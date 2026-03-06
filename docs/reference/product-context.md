# Jira Dashboard MVP - 產品背景

**用途**：教學示例產品的產品邊界定義和背景介紹
**對象**：PM 學員、開發人員快速瞭解產品

---

## 產品基本資訊

**產品名稱**：Jira Dashboard（敏捷團隊進度監控板）

**產品簡述**：
一個實時展示 Jira 資料的 Web Dashboard，資料來源為 Google Sheet。幫助敏捷團隊快速掌握 Sprint 進度、Issue 分布和團隊容量狀態。

**核心用戶**：敏捷團隊中的工程師、PM、Scrum Master、管理層

---

## 核心功能

### 4 個統計指標卡片
- **Total Issue Count**：總 Issue 數量
- **Total Story Points**：總故事點數
- **Total Done Item Count**：已完成 Issue 數量
- **Done Story Points**：已完成故事點數

### Issue 狀態分布圖表
- 長條圖展示 9 個固定狀態的 Issue 分布
- 互動式 tooltip 顯示詳細數值和百分比

### Sprint 篩選器
- 支援「All Sprints」、特定 Sprint、「No Sprints」篩選
- 即時更新所有指標和圖表

---

## 技術特性

| 面向 | 說明 |
|------|------|
| **資料來源** | Google Sheets（無需 API 金鑰，CSV 公開分享） |
| **更新頻率** | 5 分鐘快取，自動同步 |
| **技術棧** | Next.js 15 + React 19（前端），FastAPI（後端） |
| **部署** | Docker Compose，一鍵啟動 |

---

## 核心價值主張

> 「幫助敏捷團隊通過**簡潔的可視化**，快速掌握 Sprint 進度和風險，支援更好的決策」

**關鍵特點**：
- ✅ 一目了然：核心指標和狀態分布一屏展示
- ✅ 即時篩選：按 Sprint 動態更新所有資料
- ✅ 零配置：直接連接 Google Sheet，無需複雜設定
- ✅ 易於擴展：基於清晰的資料 schema 和 API 結構
