# 🎓 課程學員須知 - AI 時代的新 PM 之術(台北班 2026/03/07)

> 本課程**不需要你寫程式**。課程中會有一個 Jira Dashboard 作為示範案例，但所有操作都由 AI 工具協助完成，你只需要專注在**產品規格的撰寫與思考**。

## 🔧 環境準備（課前必讀）

本課程分為兩大階段，使用不同工具：

| 階段 | 課程步驟 | 主要工具 | 用途 |
|------|---------|---------|------|
| **產品探索** | Step 1 ~ Step 3 | Gen AI 對話工具 | 痛點分析、機會評估、用戶故事 |
| **規格實現** | Step 4 ~ Step 7 | AI IDE| 驗收標準、PRD、實現驗證 |

---

### 🤖 工具一：Gen AI 對話工具（Step 1 ~ Step 3）

Step 1 到 Step 3 是**高度對話驅動**的產品探索階段，你會透過和 AI 來回對話，逐步釐清痛點、評估機會、撰寫用戶故事。

#### 推薦：Google Gemini（Gemini Gem）

本課程以 **Gemini Gem** 作為主要示範工具。

👉 請在課前準備好 Google 帳號，確認可以正常使用 [Gemini](https://gemini.google.com/)

> **什麼是 Gemini Gem？**
> Gem 是 Gemini 中的「自訂 AI 助手」功能，你可以替它設定角色、指令和背景知識，讓 AI 在整段對話中維持一致的行為。課堂上會用它來模擬 PM 工作流程中的結構化分析。

> **重要提醒**：課程中使用的 System Instructions（系統指令）是**以 Gemini Gem 為基準設計的**。如果你使用其他工具，可能需要自行調整指令格式以適配你的工具。

#### 替代方案：其他 Gen AI 工具

如果你已有慣用的 Gen AI 工具，也可以使用：

| 工具 | 對應功能 | 備註 |
|------|---------|------|
| **ChatGPT** | Projects | 可建立專屬專案，維持上下文 |
| **Claude** | Projects | 可上傳參考資料，維持對話脈絡 |

> 關鍵需求是能**維持長對話上下文**和**設定系統指令（System Instructions）**，只要你的工具支援這兩點就可以。

---

### 💻 工具二：AI IDE — Google Antigravity（Step 4 ~ Step 7）

Step 4 到 Step 7，我們會使用 AI IDE 來協助撰寫驗收標準、PRD，以及試著請 AI 製作 Prototype。

> **再次提醒**：這堂課不是程式課！你負責的是**用 PM 的角度定義需求和驗收標準**。

#### 什麼是 Antigravity？

Antigravity 是 Google 推出的 AI 工具，外觀和操作方式類似一般的文字編輯器，但內建了 AI 助手。你可以用自然語言告訴它你想做什麼，它會幫你完成。

> 🎬 **課程提供 Antigravity 基本操作介紹影片**，會在課前提供，不用擔心不會操作。

👉 請在課前下載安裝：[https://antigravity.google/](https://antigravity.google/)

#### Antigravity 方案與費用

👉 定價詳情：[https://antigravity.google/pricing](https://antigravity.google/pricing)

| 方案 | 費用 | 使用額度 | 說明 |
|------|------|---------|------|
| **免費方案（Public Preview）** | $0/月 | 按模型各有額度限制 | 單一模型額度用完需**等待一週**才會補充 |
| **Google AI Pro** ⭐ 推薦 | 訂閱制 | 較高額度，約每 5 小時刷新 | 課程期間使用最順暢 |
| **Google AI Ultra** | 訂閱制 | 最高額度，約每 5 小時刷新 | 重度使用者適用 |

**如何取得較高額度？**

- **方法 1**：透過 [Google One](https://one.google.com/about/google-ai-plans/) 訂閱 **Google AI Pro** 方案（內含 Developer plan）
- **方法 2**：如果你**已經有購買** Google AI Pro 或 Google AI Ultra 訂閱，你直接就有較高的 Antigravity 使用額度，不需要額外購買

> 💡 **課程建議**：
> - **免費方案的學員**：建議優先使用 **Fast Mode（Gemini 3 Flash 模型）**，速度快且額度消耗較少，能讓你的免費額度撐更久
> - Antigravity 的額度是**按模型（per-model）分開計算**的。如果某個模型額度用完，可以點擊右下角的模型選擇器，切換到其他模型繼續使用
> - 免費方案**可以完成課程**，但單一模型額度用完後需要等待一週才會補充
> - 如果希望課程期間不中斷，建議訂閱 **Google AI Pro** 方案
> - 已有 Google AI Pro / Ultra 訂閱的學員不需要額外購買

#### 替代方案：其他 AI IDE

如果你已有慣用的 AI IDE，也可以使用（但本課程所有範例和操作步驟以 Antigravity 為示範）：

| 工具 | 備註 |
|------|------|
| **Cursor** | AI 驅動的編輯器 |
| **Claude Code** | Anthropic 的命令列開發工具 |

> ⚠️ 使用其他工具的學員，操作步驟可能與課堂示範不同，需自行對照調整。

---

### 🐳 工具三：Docker Desktop

Docker 是用來**一鍵啟動課程示範應用**的工具。你不需要了解 Docker 的技術細節，只需要安裝好、確認它有在執行就可以了。

#### 安裝 Docker Desktop

- **Mac**：[下載 Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- **Windows**：[下載 Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)

下載後按照安裝精靈完成安裝即可。

#### 確認 Docker 已準備好

安裝完成後，**打開 Docker Desktop 應用程式**：

- **Mac**：在「應用程式」資料夾中找到 Docker，點擊開啟
- **Windows**：在開始選單中搜尋 "Docker Desktop"，點擊開啟

✅ 看到 Docker Desktop 視窗左下角顯示 **綠色圖示**（Engine running），就表示準備好了！

> ⚠️ 如果顯示紅色或黃色，請稍等幾秒讓它完成啟動。如果持續無法啟動，課前請告知講師。

---

## 🚀 取得課程示範專案

以下三種方式擇一即可。取得後的資料夾，就是之後課堂上用 Antigravity 打開的專案位置。

### 方式一：使用 Terminal 指令（推薦）

這是最標準的方式，適合想練習基本指令操作的學員。

#### Mac

**1. 打開 Terminal**

按 `⌘ Command + Space`，輸入 "Terminal"，按 Enter。

**2. 選擇存放位置並下載專案**

以下指令會把專案下載到你的 "Demo" 資料夾：(Demo 只是範例，請下載到你想要的位置)

```bash
cd ~/Demo
git clone https://github.com/prodsence-training/training-pm-ai-flow-20260307.git
```

完成後，Demo 資料夾會出現一個 `training-pm-ai-flow-20260307` 資料夾。

> 💡 如果想放到其他位置（例如「文件」資料夾），把第一行改成 `cd ~/Documents`

**3. 驗證下載成功**

```bash
cd ~/Demo/training-pm-ai-flow-20260307
git status
```

看到 `On branch main` 就表示成功了。

#### Windows

**1. 打開 PowerShell**

按 `Win + R`，輸入 `powershell`，按 Enter。

**2. 選擇存放位置並下載專案**

以下指令會把專案下載到你的「Demo」資料夾：(Demo 只是範例，請下載到你想要的位置)

```powershell
cd $HOME\Demo
git clone https://github.com/prodsence-training/training-pm-ai-flow-20260307.git
```

完成後，你的 Demo 資料夾上會出現一個 `training-pm-ai-flow-20260307` 資料夾。

> 💡 如果想放到其他位置（例如「文件」資料夾），把第一行改成 `cd $HOME\Documents`

**3. 驗證下載成功**

```powershell
cd $HOME\Demo\training-pm-ai-flow-20260307
git status
```

看到 `On branch main` 就表示成功了。

> ⚠️ 如果出現 `git: command not found` 或類似錯誤，表示你的電腦尚未安裝 Git。
> - **Mac**：在 Terminal 執行 `xcode-select --install`，按照提示安裝
> - **Windows**：前往 [https://git-scm.com/downloads](https://git-scm.com/downloads) 下載安裝

---

### 方式二：使用 Antigravity IDE

如果你已經安裝好 Antigravity，可以直接在 IDE 裡面下載專案。

**步驟**：

1. 打開 Antigravity
2. 選擇「Clone Repository」（或類似的 Clone 選項）
3. 貼上專案網址：`https://github.com/prodsence-training/training-pm-ai-flow-20260307.git`
4. 選擇存放位置（建議放在桌面或文件資料夾）
5. 完成後 Antigravity 會自動打開專案

> 📸 **詳細截圖步驟**（待補充）

---

### 方式三：從 Google Drive 下載

如果上面兩種方式都不方便，也可以直接下載壓縮檔。

👉 **下載連結**：（待補充）

下載後解壓縮，將資料夾放到你方便找到的位置（例如 Demo 資料夾）。

---

### 📁 專案放在哪裡？之後怎麼用？

不管用哪種方式取得專案，請**記住你放置的位置**。

之後在課堂上使用 Antigravity 時，你需要用「Open Folder」功能打開這個資料夾：

```
📂 training-pm-ai-flow-20260307    ← 用 Antigravity 打開這個資料夾
├── docs/          ← 課程教材和範本
├── frontend/      ← 示範應用的前端（不用管）
├── backend/       ← 示範應用的後端（不用管）
└── specs/         ← 規格文件
```

> 你只需要關注 `docs/` 這個資料夾，其他都是示範用的技術檔案。

---

## 🐳 啟動課程示範應用（Docker）

課堂上會用一個 Jira Dashboard 示範應用來說明規格驅動開發的成果。以下步驟教你如何在自己的電腦上啟動它。

> 💡 啟動示範應用的操作會在課堂上帶著做，課前只需確認 Docker Desktop 已安裝並能正常開啟即可。

### 啟動步驟

請先確認 **Docker Desktop 已開啟**（左下角是綠色圖示）。

#### Mac

打開 Terminal（`⌘ Command + Space` → 輸入 "Terminal"），執行：

```bash
# 進入專案資料夾（請改成你實際的路徑）
cd ~/Demo/training-pm-ai-flow-20260307

# 推薦：使用預構建版本（最快）
docker-compose -f docker-compose.prod.yml up

# 或使用預設版本（首次會較慢，需要構建 images）
docker-compose up
```

#### Windows

打開 PowerShell（`Win + R` → 輸入 "powershell"），執行：

```powershell
# 進入專案資料夾（請改成你實際的路徑）
cd $HOME\Demo\training-pm-ai-flow-20260307

# 推薦：使用預構建版本（最快）
docker-compose -f docker-compose.prod.yml up

# 或使用預設版本（首次會較慢，需要構建 images）
docker-compose up
```

### 確認啟動成功

等待畫面上的訊息跑完後，打開瀏覽器訪問：

👉 **http://localhost:3000**

看到 Jira Dashboard 頁面就表示成功了！

**預期時間**：
- ✅ **預構建版本**：1-2 分鐘
- ⚠️ **首次構建版本**：5-10 分鐘（取決於網路速度）

### 停止應用

在 Terminal / PowerShell 按 `Ctrl + C`，然後執行：

```bash
# 使用預構建版本時
docker-compose -f docker-compose.prod.yml down

# 或使用預設版本時
docker-compose down
```

### ✅ 預構建 Images 已上傳至 Docker Hub

**好消息**：你 **無需等待構建**！

預構建的 images 已經上傳到 Docker Hub（講師已準備）：
- Backend: `docker.io/juggernautliu/training-pm-ai-flow:backend-v1.0`
- Frontend: `docker.io/juggernautliu/training-pm-ai-flow:frontend-v1.0`

執行 `docker-compose -f docker-compose.prod.yml up` 時，Docker 會自動從 Docker Hub **拉取 images**（**無需登入，無需構建**）。

> 💡 **首次啟動時間**：1-2 分鐘（自動拉取 images）
> 💡 **後續啟動時間**：幾秒鐘（images 已存在本機）

---

## ⚡ 課堂快速指令

把這三行指令存下來，課堂上就只需要這些：

### 1️⃣ 啟動應用
```bash
docker-compose -f docker-compose.prod.yml up
```

### 2️⃣ 訪問儀表板
打開瀏覽器，輸入：
```
http://localhost:3000
```

### 3️⃣ 關閉應用
在 Terminal / PowerShell 按：
```
Ctrl + C
```

---

## 📚 課程教材位置

專案下載到本機後，以下是你會用到的教材：

| 位置 | 說明 |
|------|------|
| `docs/chat-note/student-workbook.md` | **👉 學員工作手冊（必看）** |
| `docs/reference/` | 每個 Step 的參考範例和產出 |
| `docs/template/` | 課程使用的 Prompt 範本 |
| `docs/lab-jugg-example/` | 講師的完整實例演示 |
| `.agents/skills/` | **AI Agent Skills — Step 4~7 在 Antigravity 中使用** |

#### AI Agent Skills（`.agents/skills/`）

這個資料夾放的是課程 Step 4~7 中，讓 AI IDE 使用的「技能包」。每個 Skill 對應課程的一個步驟：

| Skill | 對應 Step | 用途 |
|-------|----------|------|
| `PainAnalysis/` | Step 1 | 痛點分析（參考用） |
| `OpportunitySolutionTree/` | Step 2 | 機會規模評估（參考用） |
| `UserStory/` | Step 3 | 用戶故事撰寫（參考用） |
| `AcceptanceCriteria/` | Step 5 | 驗收標準撰寫 |
| `PRD/` | Step 6 | 產品需求文件撰寫 |

> 你不需要手動打開這些檔案。在 Antigravity 中操作時，AI 會自動讀取這些 Skills 來輔助你完成工作。課堂上會說明如何使用。

---

## ❓ 常見問題

### Q1: 我不會寫程式，能上這堂課嗎？

**A**: 完全可以！這堂課是為 PM 設計的，重點在產品規格的撰寫與思考。課程中的 Jira Dashboard 只是示範案例，所有技術操作都由 AI 工具協助完成。

### Q2: Docker Desktop 無法啟動？

**A**:
- 確認你的電腦符合系統需求（Mac 需 macOS 12+，Windows 需 Windows 10 64-bit 以上）
- Windows 使用者請確認已啟用「WSL 2」（安裝 Docker Desktop 時通常會自動處理）
- 重新啟動電腦後再試一次
- 如果仍然無法啟動，課前請告知講師

### Q3: 示範應用啟動很慢？

**A**: 第一次啟動需要下載必要的檔案，視網路速度可能需要 5-10 分鐘，請耐心等待。第二次啟動會快很多。

### Q4: Antigravity 免費額度用完了怎麼辦？

**A**: Antigravity 的額度是按模型分開計算的，有幾種應對方式：
1. **省著用** — 優先使用 **Fast Mode（Gemini 3 Flash）**，額度消耗較少
2. **換模型** — 點擊右下角的模型選擇器，切換到其他還有額度的模型繼續使用
3. **等待補充** — 免費方案單一模型額度用完後需等待一週補充
4. **升級方案** — 訂閱 Google AI Pro（額度約每 5 小時刷新）
5. **替代工具** — 暫時使用其他 AI IDE（如 Cursor）

### Q5: 沒有 Google 帳號怎麼辦？

**A**: 課程 Step 1~3 需要使用 Gemini（需要 Google 帳號）。如果不方便申請，可以使用 ChatGPT 或 Claude 作為替代，但 System Instructions 可能需要自行調整。

---

## ✅ 課前檢查清單

**Gen AI 對話工具（Step 1~3 使用）**
- [ ] Google 帳號已準備好，能正常使用 [Gemini](https://gemini.google.com/)
- [ ] 或已準備好替代工具（ChatGPT Projects / Claude Projects）

**AI IDE（Step 4~7 使用）**
- [ ] 已下載安裝 [Google Antigravity](https://antigravity.google/)
- [ ] 已了解 Antigravity 額度方案（免費方案或 Google AI Pro）
- [ ] 或已準備好替代 AI IDE（Cursor 等）

**Docker Desktop**
- [ ] 已安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [ ] Docker Desktop 能正常開啟（左下角顯示綠色圖示）

**課程示範專案**
- [ ] 已下載專案到電腦上（三種方式擇一）
- [ ] 記得專案資料夾的存放位置

**課程討論區**
- [ ] 已加入 [Discord](https://discord.gg/UBmFFW54Rh)

> 如果有任何項目遇到問題，**請在課程開始前透過 Discord 告知講師，不要等到上課時才反映。**

---

## 💬 課程討論區（Discord）

課程使用 **Discord** 作為主要的溝通和討論管道。請在課前加入：

👉 **https://discord.gg/UBmFFW54Rh**

在這裡你可以：
- 課前環境安裝遇到問題，隨時發問
- 課程期間與講師和其他學員即時討論
- 課後持續交流學習心得

> 請在課前就加入 Discord，確認能正常使用。

---

## 📞 重要連結

**課程資源**
- **Discord 討論區** → https://discord.gg/UBmFFW54Rh
- **GitHub Repo** → https://github.com/prodsence-training/training-pm-ai-flow-20260307
- **學員工作手冊** → `docs/chat-note/student-workbook.md`（下載專案後在本機打開）

**工具下載與帳號**
- **Google Gemini** → https://gemini.google.com/
- **Google Antigravity** → https://antigravity.google/
- **Antigravity 定價方案** → https://antigravity.google/pricing
- **Google One AI 方案** → https://one.google.com/about/google-ai-plans/
- **Docker Desktop** → https://www.docker.com/products/docker-desktop

---

**祝你學習愉快！有任何問題，隨時在 Discord 發問。** 🚀

---

**版本** | v2.0
**最後更新** | 2026年2月27日
**作者** | JUGG
