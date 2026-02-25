# 產品背景配置模板

> 使用此模板來定義你的產品邊界和能力範圍
>
> 將此文件複製並重命名，然後填入你的產品資訊
> 例如：`product-context-my-dashboard.md`

---

## 產品基本資訊

**產品名稱**：[你的產品名稱，例如：Web Dashboard]

**產品簡述**：[一句話描述你的產品做什麼，例如：展示 Jira 資料的 Web Dashboard，資料來源為 Google Sheet]

**核心用戶**：[你的主要用戶是誰？例如：敏捷團隊、PM、工程師]

---

## ✅ 你應該探索的解法範圍

在 OST 分析中，可以建議以下方向的解決方案（在此範圍內發散）：

- [解法方向 1：例如 UI/UX 改進]
- [解法方向 2：例如 功能增強]
- [解法方向 3：例如 資料呈現方式]
- [解法方向 4：例如 整合能力]
- [解法方向 5：...]

**具體例子**：
- [詳細例子 1]
- [詳細例子 2]
- [詳細例子 3]

---

## ❌ 絕對禁止建議超出範圍的解法

以下方向應該完全避免（超出產品邊界）：

- ❌ [禁止範圍 1：例如 改變客戶的工作流程]
- ❌ [禁止範圍 2：例如 改變上游系統]
- ❌ [禁止範圍 3：例如 改變組織結構]
- ❌ [禁止範圍 4：...]

**為什麼禁止**：[解釋邊界約束的原因]

---

## 核心問題框架

在 OST 分析中，始終聚焦於以下核心問題：

> 「**[你的產品] 如何 [幫助用戶解決什麼問題] ？**」

例如：
> 「Web Dashboard 如何將 Google Sheet 中的 Jira 資料轉化為可理解、可操作的視覺化資訊，幫助用戶及時發現風險、做出更好的決策？」

請定義你自己的核心問題：
> 「**[你的產品] 如何 [你的使命] ？**」

---

## 使用說明

1. **複製此模板**：
   ```
   cp product-context-template.md product-context-my-product.md
   ```

2. **填入你的產品資訊**：
   - 產品名稱
   - 應該探索的解法範圍
   - 禁止的解法範圍
   - 核心問題框架

3. **在使用 OST Skill 時指定配置**：

   **方式 A（靈活）**：直接上傳配置文件到 Gemini
   ```
   上傳此 .md 文件，Gem 會自動讀取
   ```

   **方式 B（自動 - 推薦）**：放在 **用戶級別** 全局目錄

   **Claude Code：**
   ```bash
   # macOS / Linux
   cp product-context-my-product.md ~/.claude/skills/OpportunitySolutionTree/examples/

   # Windows
   copy product-context-my-product.md %USERPROFILE%\.claude\skills\OpportunitySolutionTree\examples\
   ```

   **Antigravity：**
   ```bash
   # macOS / Linux
   cp product-context-my-product.md ~/.agents/skills/OpportunitySolutionTree/examples/

   # Windows
   copy product-context-my-product.md %USERPROFILE%\.agents\skills\OpportunitySolutionTree\examples\
   ```

   之後任何項目都能使用

   **方式 C（自動）**：放在 **項目級別** 目錄

   **Claude Code：**
   ```bash
   cp product-context-my-product.md /my-project/.claude/skills/OpportunitySolutionTree/examples/
   ```

   **Antigravity：**
   ```bash
   cp product-context-my-product.md /my-project/.agents/skills/OpportunitySolutionTree/examples/
   ```

   只在此項目中使用

4. **Skill 會自動應用你的配置**，開始探索 OST

---

**配置優先度**（同一平台內）：
```
項目級配置（最高）→ 用戶級配置（中） → 一次性上傳（最低）
```

**選擇哪個方式？**
- 課程標準配置 / 團隊共用 → 用戶級別（方式 B）
- 特定項目的配置 → 項目級別（方式 C）
- 一次性使用 / 快速測試 → 直接上傳（方式 A）

---

## 模板範例

詳見 `product-context-example.md`（Web Dashboard 的完整範例）
