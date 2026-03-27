# Opportunity Solution Tree（OST）Skill

**機會解決方案樹探索助手** — 幫助團隊從痛點出發，系統性地探索完整的機會與解法空間。

---

## ⚠️ 重要概念區分

### 什麼是「Skill」？

Skill 是 Claude Code 和 Antigravity 的**內建功能啟動**機制。當你在對話中提到特定場景時，Skill 會自動載入相關的系統指令。

**使用方式**：在 Claude Code / Antigravity 對話中提及相關場景，Skill 會自動觸發。

### 什麼是「Gemini Gem」？

Gemini Gem 是 Google Gemini 中的**自定義 AI Agent**。你需要手動建立 Gem 並貼入系統提示詞。

**使用方式**：
1. 在 Google Gemini 中建立新的 Gem
2. 複製本 Skill 中的 Gem 系統提示詞（Role 到 Output Format）
3. 上傳產品背景上下文文件
4. 開始對話

---

## 用途

根據 Step 1（痛點分析）的輸出，協助 PM 完成 **OST 四層框架**：
**Outcome → Opportunities → Solutions → Experiments**

特點：
- ✅ **可配置**：根據你的產品背景進行約束
- ✅ **多模式**：支持「快速模式」和「探索模式」
- ✅ **互動式**：與團隊共同發現機會（不是單向輸出）

---

## 觸發時機

當你：
- ✅ 已完成 Step 1 痛點分析
- ✅ 想系統性地探索解法空間
- ✅ 需要幫助從痛點轉換到機會定義
- ✅ 想確保 Solutions 多樣化、不跳過 Opportunities

---

## 檔案結構

```
OpportunitySolutionTree/
│
├── SKILL.md                              # Claude Code Skill 標準格式
├── README.md                             # 本文件
│
├── references/
│   ├── gemini-gem-PM-2-ost-generic-template.md
│   │   └─ 通用 OST Gem 模板（不含具體產品約束）
│   │
│   ├── gemini-gem-PM-2-ost-prompts-v2.md
│   │   └─ 舊版本（Web Dashboard 示例，參考用）
│   │
│   ├── product-context-template.md
│   │   └─ 產品背景配置模板
│   │
│   └── CHANGELOG.md
│       └─ 版本歷史
│
└── examples/
    └── [你的 product-context-*.md]
        └─ 你的產品背景上下文（複製 template 後建立）
```

---

## 核心概念：產品背景配置

### 為什麼需要配置？

這個 Skill 是「**可配置的通用 Gem**」。不同產品有不同的邊界約束：
- **解決方案提供商**（如：Dashboard、CRM）→ 只能建議產品功能範圍內的解法
- **流程諮詢公司** → 可以建議組織流程改變
- **技術平台** → 可以建議架構改進

配置文件讓 Gem 知道「你的產品邊界在哪」。

### 配置包含什麼？

```markdown
產品名稱 & 簡述
├── ✅ 應該探索的解法 (在此範圍內發散)
├── ❌ 絕對禁止的範圍 (超出邊界)
└── 核心問題框架 (聚焦方向)
```

**例子**：
```
✅ 可以建議：UI 設計、新增指標、資料轉換
❌ 不能建議：改客戶流程、改組織方式
```

---

## 使用方式

### 方式 A：靈活指定配置 🚀

**最簡單，適合一次性使用或快速測試**

#### Step 1：準備產品背景

複製 `product-context-template.md`，填入你的產品資訊：

```bash
cp references/product-context-template.md product-context-my-product.md
# 編輯 product-context-my-product.md，填入你的產品信息
```

#### Step 2：使用 Skill 時指定配置

在 Claude Code 中：

```
我要用 OST Skill 進行產品探索。

【我的產品背景配置】
產品名稱：My Dashboard
應該探索：UI 設計、資料呈現、篩選邏輯
禁止範圍：改變客戶流程、系統架構決策
核心問題：我們的 Dashboard 如何幫助用戶更好地理解資料？

【Step 1 痛點分析】
[粘貼你的痛點分析報告]
```

Skill 會根據你的配置進行 OST 分析。

---

### 方式 B：自動使用本地配置 - 用戶級別 ⚙️

**最便利，推薦課程或團隊標準配置**

#### Claude Code：

```bash
# macOS / Linux
cp product-context-my-product.md ~/.claude/skills/OpportunitySolutionTree/examples/

# Windows
copy product-context-my-product.md %USERPROFILE%\.claude\skills\OpportunitySolutionTree\examples\
```

#### Antigravity：

```bash
# macOS / Linux
cp product-context-my-product.md ~/.agents/skills/OpportunitySolutionTree/examples/

# Windows
copy product-context-my-product.md %USERPROFILE%\.agents\skills\OpportunitySolutionTree\examples\
```

#### 使用：

```
我要用 OST Skill 進行產品探索。
請使用配置文件：product-context-my-product.md

【Step 1 痛點分析】
[粘貼你的痛點分析報告]
```

之後在所有項目中都能使用此配置。

---

### 方式 C：自動使用本地配置 - 項目級別 📁

**適合特定項目的配置**

#### Claude Code：

```bash
# 解壓縮 .skill 文件到項目
unzip OpportunitySolutionTree.skill -d /my-project/.claude/skills/

# 複製配置到項目目錄
cp product-context-my-product.md \
   /my-project/.claude/skills/OpportunitySolutionTree/examples/
```

#### Antigravity：

```bash
# 複製配置到項目目錄
cp product-context-my-product.md \
   /my-project/.agents/skills/OpportunitySolutionTree/examples/
```

#### 使用：

```
我要用 OST Skill 進行產品探索。
請使用配置文件：product-context-my-product.md

【Step 1 痛點分析】
[粘貼你的痛點分析報告]
```

只在此項目中自動應用配置。（項目級配置會覆蓋用戶級配置）

---

---

## 配置層級說明

### Claude Code

| 層級 | 位置 | 適用場景 | 優先度 |
|------|------|---------|--------|
| **用戶級** | `~/.claude/skills/OpportunitySolutionTree/examples/` | 課程標準配置、團隊共用 | ⭐⭐ |
| **項目級** | `/project/.claude/skills/OpportunitySolutionTree/examples/` | 特定項目的配置 | ⭐⭐⭐（最高） |
| **一次性** | 直接上傳到對話 | 快速測試、臨時使用 | ⭐ |

### Antigravity

| 層級 | 位置 | 適用場景 | 優先度 |
|------|------|---------|--------|
| **用戶級** | `~/.agents/skills/OpportunitySolutionTree/examples/` | 課程標準配置、團隊共用 | ⭐⭐ |
| **項目級** | `/project/.agents/skills/OpportunitySolutionTree/examples/` | 特定項目的配置 | ⭐⭐⭐（最高） |
| **一次性** | 直接上傳到對話 | 快速測試、臨時使用 | ⭐ |

**規則**：項目級會覆蓋用戶級，用戶級會覆蓋一次性。（各平台獨立運作）

---

## Gem 選擇

使用時，Skill 會讓你選擇工作模式：

### 快速模式 🚀（5 分鐘）

- 直接生成 OST 報告
- 適合：快速原型、時間有限、已有明確方向
- 輸出：完整的 OST 文件

### 探索模式 🔍（15-30 分鐘）

- 與 Skill 互動式對話，逐步發現機會
- 適合：團隊學習、創新挖掘、深入思考
- 輸出：經過協作精煉的 OST 文件

---

## 工作流程

```
Step 1: 痛點分析 ✓（來自 PainAnalysis Skill）
    ↓
Step 2: OST 探索 ← 【你在這】
    ├─ 模式選擇（快速 vs 探索）
    ├─ 定義 Outcome
    ├─ 發現 Opportunities
    ├─ 探索 Solutions
    └─ 建議 Experiments
    ↓
Step 3: 用戶故事 & PRD（待建設）
```

---

## 實際範例

### 輸入（Step 1 痛點分析）

```
敏捷團隊的各角色因為 Sprint 執行過程中缺乏即時、統一的進度與風險可視化資訊，
無法在正確的時間點識別風險並做出調整，導致問題在 Sprint 後半段集中爆發。
```

### 輸出（OST 報告）

```
# 🧩 機會解決方案樹（OST）報告 — Step 2

## 1. Outcome
- Sprint 過程中，團隊能及時識別和調整風險

## 2. Opportunity Clusters
- Cluster A：資訊透明度問題
  - Opportunity A1：Burndown Chart 不易取得或理解
  - Opportunity A2：Ticket 的 Roadmap 連結不清晰

- Cluster B：風險可視化問題
  - Opportunity B1：插單的優先度與容量影響沒有可視化
  - Opportunity B2：Blocker 沒有預警機制

## 3. Solutions
- Opportunity A1 → Solutions
  - 技術解法：建立統一的 Dashboard
  - 流程解法：簡化 Burndown 解讀儀式
  - 可視化解法：大螢幕實時展示

[詳細解法...]

## 4. Experiments
[驗證方式...]

## 5. 後續建議
[優先方向...]
```

---

## 產品背景上下文使用指南

### 什麼是產品背景上下文？

`product-context-[your-product].md` 定義了你的產品邊界：
- ✅ **應該探索的解法方向** — Skill 會在這個範圍內發散
- ❌ **絕對禁止的範圍** — Skill 不會建議這些方向
- **核心問題框架** — 聚焦的方向

### 快速開始

1. **複製模板**：`references/product-context-template.md`
2. **填入你的產品信息**
3. **在 Skill 中使用**

### 使用方式

#### 方式 A：靈活指定（一次性上傳）🚀

在 Claude Code 對話中：

```
我要用 OST Skill 進行產品探索。

【我的產品背景上下文】
[直接貼入你的 product-context 內容]

【Step 1 痛點分析】
[貼入痛點分析報告]
```

---

#### 方式 B：用戶級配置（推薦 - 課程/團隊標準）⚙️

**Claude Code**：
```bash
# macOS / Linux
cp product-context-my-product.md ~/.claude/skills/OpportunitySolutionTree/examples/

# Windows
copy product-context-my-product.md %USERPROFILE%\.claude\skills\OpportunitySolutionTree\examples\
```

**Antigravity**：
```bash
# macOS / Linux
cp product-context-my-product.md ~/.agents/skills/OpportunitySolutionTree/examples/

# Windows
copy product-context-my-product.md %USERPROFILE%\.agents\skills\OpportunitySolutionTree\examples\
```

之後只需告訴 Skill：
```
我要用 OST Skill 進行產品探索。
請使用配置文件：product-context-my-product.md

【Step 1 痛點分析】
[貼入痛點分析報告]
```

---

#### 方式 C：項目級配置（特定項目）📁

**Claude Code**：
```bash
cp product-context-my-product.md /my-project/.claude/skills/OpportunitySolutionTree/examples/
```

**Antigravity**：
```bash
cp product-context-my-product.md /my-project/.agents/skills/OpportunitySolutionTree/examples/
```

### 配置優先級

```
項目級配置（最高優先）
    ↓
用戶級配置（中優先）
    ↓
一次性上傳（最低優先）
```

**最佳實踐**：
- 課程標準配置 → 放在用戶級別（所有項目共用）
- 特定項目配置 → 放在項目級別（該項目專用）
- 快速測試 → 直接上傳到對話

---

## 何時使用此 Skill

✅ **適合使用**：
- 已完成 Step 1 痛點分析，想探索解法空間
- 團隊陷入「怎麼辦」的困境，需要系統性地發散
- 想確保不會過早跳到具體功能，先把機會和解法空間理清楚
- 學習如何進行產品發現和機會定義

❌ **不適合使用**：
- 還沒做痛點分析（先用 PainAnalysis Skill）
- 已經決定要做什麼了，只想寫技術規格（這時應該用 Step 3 User Story Skill）

---

## 何時更新此 Skill

- 實際使用 OST 過程中發現新的「機會發現」模式
- Google Gemini Gem 機制有官方更新
- 需要支持更多的工作模式或互動流程
- 學員反饋的新使用場景

---

## 相關資源

- **PainAnalysis Skill**：Step 1 痛點分析（必須先完成）
- **Gemini-Gem Skill**：Gem System Prompt 架構師（想深入理解本 Skill 的設計邏輯時用）
- **Agent Skill 知識體系**：深入學習 Skill 設計原理

---

---

## 🧩 使用 Gemini Gem（Google Gemini）

### 第一次設定

1. **建立 Gemini Gem**：在 Google Gemini 中建立新的自定義 Gem

2. **複製系統提示詞**：
   - 打開 `references/gemini-gem-PM-2-ost-generic-template.md`
   - **只複製**「# Role（角色設定）」到「# Output Format（輸出格式）」的部分
   - ❌ **不需要複製**：「## 重要提醒」和「### 常見問題」
   - 貼入 Gemini Gem 的系統提示詞設定

3. **上傳產品背景上下文**：
   - 在對話中上傳你的 `product-context-*.md` 文件
   - 或告訴 Gem 上下文文件的位置

4. **開始對話**

### 每次使用

```
我想用 OST Gem 進行產品探索。
【產品背景上下文已上傳】

【Step 1 痛點分析】
[貼入你的痛點分析報告]

選擇工作模式：快速 or 探索？
```

---

## ✅ 品質檢查清單

使用 OST Skill / Gem 時，確保通過以下檢查：

- [ ] **產品背景上下文清楚**
  - 已定義「✅ 應該探索的解法」
  - 已定義「❌ 禁止的範圍」
  - 已明確核心問題框架

- [ ] **所有建議符合邊界**
  - 沒有超出「❌ 禁止範圍」的建議
  - Solutions 都在產品能力範圍內
  - 沒有跳過 Opportunities 層級

- [ ] **避免過度具體化**
  - 沒有提前寫 User Story / PRD
  - 沒有 Acceptance Criteria
  - Solutions 是多樣化的探索，不是單一功能推薦

- [ ] **Experiments 具體可行**
  - 每個 Solution 都有驗證方式
  - Experiments 用最小成本

---

## ❓ 常見問題

### 關於產品背景上下文文件

**Q：產品背景上下文文件很重要嗎？**
A：⭐ 非常重要。它決定了 Skill/Gem 的建議邊界。如果沒有清楚的配置，會容易建議超出範圍的解法。建議花 5 分鐘定義清楚，省後面 50 分鐘的討論。

**Q：每次都需要上傳配置嗎？**
A：
- 如果用 **Claude Code/Antigravity Skill**：設定好後，Skill 會自動讀取（取決於配置層級）
- 如果用 **Gemini Gem**：第一次上傳後，同一個對話中無需再上傳。開新對話時建議重新上傳

**Q：如果我想改配置呢？**
A：上傳新的配置文件，Skill/Gem 會自動讀取最新版本。

### 關於工作模式

**Q：快速模式和探索模式有什麼區別？**
A：
- **快速模式**（5 分鐘）：Skill 直接生成 OST 報告，適合時間緊張
- **探索模式**（15-30 分鐘）：互動式與 Skill 一起發現機會，適合團隊學習和創新
- 可以結合使用：先快速生成，再深入探索某些機會

**Q：我應該選哪一個？**
A：
- 第一次使用 → 探索模式（理解完整流程）
- 快速迭代 → 快速模式（快速決策）
- 最終用法 → 混合使用

### 平台相關

**Q：Claude Code 和 Antigravity 有什麼區別？**
A：
- **Claude Code**：Skill 放在 `~/.claude/skills/` 或 `/project/.claude/skills/`
- **Antigravity**：Skill 放在 `~/.agents/skills/` 或 `/project/.agents/skills/`
- 使用方式相同，只是目錄不同

**Q：我可以同時在 Claude Code 和 Gemini 中使用嗎？**
A：可以。它們是獨立的平台，各有各的配置和對話上下文。

---

## 最後提醒

⚠️ **重要**：
- 產品背景配置很重要，它決定了 Skill/Gem 的建議邊界
- 清楚的邊界約束能確保建議始終在你的產品範圍內
- 花 5 分鐘定義清楚你的產品邊界，省後面很多時間

💡 **最佳實踐**：
- 課程標準配置 → 放在用戶級別（所有項目共用）
- 項目特定配置 → 放在項目級別（該項目專用）
- 快速測試 → 直接上傳到對話
- 保留配置版本 → 便於日後參考和更新
