# Isolated Mode Prototypes

## 📍 說明

此目錄存放 **Isolated Mode** 生成的 Prototype。這些是 **自動生成的獨立頁面**，完全隔離於 codebase，用於快速示範和 Demo。

---

## 🏗️ 結構

```
frontend/public/prototypes/
├── pacing-bar.html                 # Prototype 獨立 HTML 檔
├── dashboard-integrated.html       # Prototype 獨立 HTML 檔
└── README.md                       # 本文件
```

---

## 🚀 使用方式

### 直接在瀏覽器打開

```
http://localhost:3000/prototypes/pacing-bar.html
http://localhost:3000/prototypes/dashboard-integrated.html
```

### 或在專案運行時訪問

確保 frontend 開發伺服器運行中：
```bash
cd frontend
npm run dev
```

然後訪問上述 URL。

---

## ⚠️ 重要說明

**這些檔案由 Prototype Skill 自動生成，請勿手動編輯。**

### 如果需要修改：
1. **在代碼層面修改**：回到 `frontend/src/app/prototype/[slug]/page.tsx` 編輯 Direct Mode Prototype
2. **重新生成**：使用 Prototype Skill 重新產出

### 如果要刪除：
```bash
# 刪除整個目錄
rm -rf frontend/public/prototypes/

# 或刪除單個 prototype
rm frontend/public/prototypes/pacing-bar.html
```

---

## 🔗 Prototype 模式說明

| 模式 | 位置 | 用途 | 特點 |
|------|------|------|------|
| **Direct Mode** | `frontend/src/app/prototype/[slug]/` | 學員手動編輯 | 集中管理，易於迭代 |
| **Isolated Mode** | `frontend/public/prototypes/` | 自動生成示範 | 完全隔離，乾淨刪除 |

---

## 📝 Prototype 清單

| 檔案 | 功能 | 生成方式 |
|------|------|---------|
| `pacing-bar.html` | Sprint 雙重進度條 | Skill 自動生成（Isolated）或手動（Direct） |
| `dashboard-integrated.html` | Dashboard 整合版 | Skill 自動生成（Isolated） |

---

## 🎯 何時使用 Isolated Mode？

- ✅ 需要快速生成示範，不想改 codebase
- ✅ 要完整獨立的 HTML，方便分享
- ✅ 完成後乾淨刪除，零污染
- ✅ 用於 Demo、截圖、Pitch

---

## 🎯 何時使用 Direct Mode？

- ✅ 學員學習如何開發 Prototype
- ✅ 需要長期保留和迭代
- ✅ 要在課程中展示代碼結構

詳見 `frontend/src/app/prototype/README.md`
