# Prototype 開發指南

## 📚 說明

此目錄用於 **課程教學示範**。所有 prototype 都在 `[slug]/page.tsx` 中統一管理，而非分散在多個資料夾。

**⚠️ 重要：這是教學設計，不是生產標準。** 職場中應遵循貴公司的 repository 規則。

---

## 📝 如何新增 Prototype

### 步驟 1：編輯 `[slug]/page.tsx`

在檔案頂部創建你的 **Prototype 組件**：

```tsx
// ── 你的新 Prototype ──
function YourFeaturePrototype() {
  const [state, setState] = useState('')

  return (
    <main className="min-h-screen bg-gray-50">
      {/* 根據 PRD 和 AC 開發你的 UI */}
      <h1>Your Feature Name</h1>
      {/* ... 代碼 */}
    </main>
  )
}
```

### 步驟 2：在 switch 語句中註冊

找到 `PrototypePage` 函數中的 switch 語句，添加新的 case：

```tsx
export default function PrototypePage({ params }: { params: { slug: string } }) {
  const { slug } = params

  switch (slug) {
    case 'pacing-bar':
      return <PacingBarPrototype />

    case 'your-feature-name':  // ← 添加這行
      return <YourFeaturePrototype />

    default:
      return <NotFoundPrototype slug={slug} />
  }
}
```

### 步驟 3：訪問你的 Prototype

```
http://localhost:3000/prototype/your-feature-name
```

---

## ✅ 現有 Prototype

| 路由 | 功能 | 位置 |
|------|------|------|
| `/prototype/pacing-bar` | Sprint 雙重進度條 | 同檔案內 |
| `/prototype/[新功能]` | 學員創建 | 同檔案內 |

---

## 📋 檢查清單

創建新 prototype 時，確認：

- [ ] 在 `[slug]/page.tsx` 頂部創建組件（不新建資料夾）
- [ ] 在 switch 語句中添加 case 映射
- [ ] 路由名稱使用 `kebab-case`（如 `dashboard-integrated`）
- [ ] 添加 `'use client'` directive（如果使用 React hooks）
- [ ] 根據 PRD 和 AC 開發功能
- [ ] 測試 http://localhost:3000/prototype/[name]

---

## 🚀 開發後清理

完成課程後，還原所有改動：

```bash
git checkout frontend/src/app/prototype/
```

---

## ⚠️ 職場應用

**本結構僅限教學使用。** 在實際工作中：

- 遵循貴公司的 repository 規則
- 可能需要獨立資料夾、分支或 repo
- 詢問團隊的代碼組織習慣
- 不要直接複製此教學結構

**目標是學習「如何開發 prototype」，而不是「如何組織代碼結構」。**
