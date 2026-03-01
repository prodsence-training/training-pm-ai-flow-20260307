# Jira Dashboard MVP v1.0

這是一個完整的全端應用程式，用於顯示 Jira 專案的關鍵統計指標、狀態分布和 Sprint 篩選功能。

## 功能特色

✅ **4 個統計指標卡片**
- Total Issue Count（總 Issue 數）
- Total Story Points（總故事點數）
- Total Done Item Count（已完成 Issue 數）
- Done Story Points（已完成故事點數）

✅ **狀態分布長條圖**
- 9 個固定狀態的 Issue 分布
- 互動式 tooltip 顯示詳細資訊
- 百分比顯示

✅ **Sprint 篩選器**
- 支援所有 Sprint、特定 Sprint 和「No Sprints」篩選
- 自動處理重複 Sprint 名稱
- 即時更新所有指標和圖表

✅ **效能優化**
- 5 分鐘 in-memory 快取
- 並行 API 請求
- 持續載入狀態（無超時）

## 技術堆疊

### 前端
- **Next.js 15.2.4** (App Router)
- **React 19.0.0**
- **TypeScript 5.x**
- **Tailwind CSS 3.4.x**
- **Recharts 2.x** (圖表庫)

### 後端
- **Python 3.11**
- **FastAPI 0.104.1**
- **Pandas 2.1.3** (資料處理)
- **Uvicorn 0.24.0** (ASGI 伺服器)

### 基礎設施
- **Docker & Docker Compose**
- **Google Sheets** (CSV API 作為資料來源)

## 🚀 環境設置

### 步驟 1：取得專案 - 選擇其中一種方式

#### 方式 A：使用 Terminal 執行 Git Clone

**前置要求**：
- 已安裝 Git（檢查：在 Terminal 執行 `git --version`）
- 如果未安裝，請先安裝：
  ```bash
  # macOS（使用 Homebrew）
  brew install git

  # Windows（使用 Chocolatey）
  choco install git

  # Linux（Ubuntu/Debian）
  sudo apt-get install git
  ```

**詳細步驟**：

1️⃣ **打開 Terminal（終端機）**
   - **macOS**: 按 `⌘ Command + Space`，搜尋 "Terminal"，按 Enter
   - **Windows**: 按 `Win + R`，輸入 `cmd` 或 `powershell`，按 Enter
   - **Linux**: 按 `Ctrl + Alt + T`

2️⃣ **執行以下指令**（複製整行，貼到 Terminal 後按 Enter）：
   ```bash
   git clone https://github.com/prodsence-training/training-pm-ai-flow-20260307.git
   ```

3️⃣ **進入專案目錄**：
   ```bash
   cd training-pm-ai-flow-20260307
   ```

4️⃣ **驗證成功**：
   ```bash
   # 應該會看到類似的輸出
   # On branch main
   # nothing to commit, working tree clean
   git status
   ```

---

#### 方式 B：使用 Antigravity IDE

**步驟**：
1. 在 Antigravity 中連接到 GitHub repo
2. 選擇專案並開啟

> 📸 **詳細截圖步驟**（待補充）
>
> [這裡將插入 Antigravity 的使用步驟和截圖]

---

### ✅ 驗證環境

在 Terminal 執行以下指令驗證 Docker 已正確安裝：

```bash
docker --version
docker-compose --version
```

**預期輸出**：
```
Docker version 20.10+
Docker Compose version 2.0+
```

如果看到版本號，表示環境已準備就緒！ ✅

## 快速開始

### 前置需求

✅ **只需要 Docker**：
- Docker 20.10+
- Docker Compose 2.0+

**下載 Docker Desktop**：https://www.docker.com/products/docker-desktop/

> ℹ️ **授權說明**：
> - 可以使用 **Docker Personal Free** 方案（個人或小團隊使用免費）
> - 或直接使用，**不需要登入帳號也能使用**

> 💡 **您無需安裝 Node.js 或 Python**
> 所有依賴都已包含在 Docker 容器中

### 🚀 推薦方式：課堂快速啟動（使用預構建版本）

**適用對象**：PM 學員、課堂演示

最簡單的方式，使用預構建的 images 一鍵啟動完整應用：

```bash
# 啟動所有服務（自動從 Docker Hub 拉取 pre-built images）
docker-compose -f docker-compose.prod.yml up

# 或背景執行
docker-compose -f docker-compose.prod.yml up -d

# 查看日誌
docker-compose -f docker-compose.prod.yml logs -f

# 停止服務
docker-compose -f docker-compose.prod.yml down
```

訪問：http://localhost:3000

> ✅ **優點**：
> - 啟動速度快（1-2 分鐘）
> - 無需本地構建
> - 從 Docker Hub 自動拉取預構建 images
> - 完全無需修改代碼

> 📦 **Images 來源**：
> - Backend: `docker.io/juggernautliu/training-pm-ai-flow:backend-v1.0`
> - Frontend: `docker.io/juggernautliu/training-pm-ai-flow:frontend-v1.0`
> - 公開倉庫，無需登入

---

### 📝 開發人員選項

#### 模式 2: 本地開發（Rapid Development）

首次啟動會自動構建 images，支援代碼熱重載：

```bash
# 啟動開發容器（首次會構建，之後可重複使用）
docker-compose up

# 背景執行
docker-compose up -d

# 查看日誌
docker-compose logs -f frontend

# 停止容器
docker-compose down
```

特點：
- ✅ 修改代碼後立即看到效果（無需重啟）
- ⚠️ 首次啟動較慢（需要構建 images）

---

#### 模式 3: 開發模式（Development Mode with Playwright）

包含 Playwright 瀏覽器測試環境：

```bash
# 啟動開發容器（支援 Playwright）
docker-compose -f docker-compose.dev.yml up

# 背景執行
docker-compose -f docker-compose.dev.yml up -d

# 查看日誌
docker-compose -f docker-compose.dev.yml logs -f frontend

# 停止開發容器
docker-compose -f docker-compose.dev.yml down
```

特點：
- ✅ 支援代碼熱重載
- ✅ 包含 Playwright 測試環境
- ⚠️ 首次啟動最慢（需要安裝 Playwright 瀏覽器）

---

## 構建 Pre-built Images

### 標準工作流程

**1️⃣ 開發階段**（頻繁改代碼）

```bash
# 使用開發版本，支援 hot reload
docker-compose up

# 修改代碼後自動更新，無需重啟
```

**2️⃣ 代碼完成後**（準備課堂演示）

```bash
# 構建最新版本
./scripts/build-docker.sh v1.0
```

**3️⃣ 課堂上使用**（快速啟動）

```bash
# 使用預構建版本，1-2 分鐘快速啟動
docker-compose -f docker-compose.prod.yml up
```

---

### 詳細說明

#### 何時執行構建？

| 場景 | 命令 | 說明 |
|------|------|------|
| 開發中修改代碼 | `docker-compose up` | 自動 hot reload，無需 rebuild |
| 代碼改完要定型 | `./scripts/build-docker.sh v1.0` | 構建新的 pre-built images |
| 課堂上快速演示 | `docker-compose -f docker-compose.prod.yml up` | 1-2 分鐘啟動 |

#### 版本管理

每次改完代碼後更新版本號：

```bash
# v1.0 → v1.1
./scripts/build-docker.sh v1.1

# 之後課堂用最新版本
docker-compose -f docker-compose.prod.yml up
```

#### 推送到 Docker Hub（可選）

如果要讓學員從遠端拉取：

```bash
# 需要先登入
docker login

# 構建並標記版本
./scripts/build-docker.sh v1.0 docker.io/yourusername

# 推送到 registry
docker push docker.io/yourusername/training-pm-ai-flow:backend-v1.0
docker push docker.io/yourusername/training-pm-ai-flow:frontend-v1.0
```

學員就可以直接拉取：

```bash
docker pull docker.io/yourusername/training-pm-ai-flow:backend-v1.0
docker pull docker.io/yourusername/training-pm-ai-flow:frontend-v1.0
docker-compose -f docker-compose.prod.yml up
```

---

## 訪問應用程式

啟動容器後，訪問以下位置：

- **前端**：http://localhost:3000
- **後端 API**：http://localhost:8000
- **API 文檔**：http://localhost:8000/docs

---

## 🔄 更新 Google Sheet 配置

如果你需要更換 Google Sheet 的資料來源，按以下步驟操作：

### 步驟 1：更新後端環境變數

編輯 `backend/.env`：

```bash
# Google Sheets 配置
GoogleSheets__SheetId=YOUR_NEW_SHEET_ID          # 改成新的 Sheet ID
GoogleSheets__RawDataSheet=rawData                # 原始資料工作表名稱
GoogleSheets__SprintSheet=GetJiraSprintValues     # Sprint 工作表名稱
```

**如何獲取 Sheet ID**：
- 打開你的 Google Sheet
- URL 中的這段就是 Sheet ID：`https://docs.google.com/spreadsheets/d/**SHEET_ID**/edit`

### 步驟 2：驗證工作表名稱

確保你的 Google Sheet 中有兩個工作表：
- **rawData** - 包含 23 個欄位的 Issue 資料（A:W）
- **GetJiraSprintValues** - 包含 9 個欄位的 Sprint 資料（A:I）

> 📌 如果你的工作表名稱不同，修改上面 `.env` 中的名稱。

### 步驟 3：重新構建 Images

```bash
# 更新版本號（例如從 v1.0 → v1.1）
./scripts/build-docker.sh v1.1
```

### 步驟 4：推送到 Docker Hub

```bash
# 推送新版本到 Docker Hub
docker push docker.io/juggernautliu/training-pm-ai-flow:backend-v1.1
docker push docker.io/juggernautliu/training-pm-ai-flow:frontend-v1.1
```

### 步驟 5：更新 docker-compose.prod.yml

編輯 `docker-compose.prod.yml`，更新 backend image 版本：

```yaml
backend:
  image: docker.io/juggernautliu/training-pm-ai-flow:backend-v1.1  # 改成 v1.1
```

### 步驟 6：驗證新配置

```bash
# 啟動應用
docker-compose -f docker-compose.prod.yml up

# 訪問前端
http://localhost:3000

# 查看後端日誌確認連接成功
docker-compose -f docker-compose.prod.yml logs backend
```

---

### 方法 2: 本地開發（適合開發人員，學員無需此步驟）

> ⚠️ **學員注意**：Docker Compose 已包含所有開發環境，無需本地安裝

如果需要本地開發環境，參考以下步驟：

#### 後端

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

#### 前端

```bash
cd frontend
npm install
npm run dev
```

## 專案結構

```
training-pm-ai-flow-20260307/
│
├── 📦 frontend/              # Next.js 前端應用
│   ├── src/
│   │   ├── app/            # 儀表板頁面
│   │   ├── components/     # UI 元件（卡片、圖表、篩選器）
│   │   ├── hooks/          # 資料抓取邏輯
│   │   └── services/       # API 客戶端
│   ├── Dockerfile
│   ├── .env                # 前端環境變數
│   └── .env.example        # 環境變數範本
│
├── 📦 backend/              # FastAPI 後端應用
│   ├── src/
│   │   ├── models/         # 資料結構定義
│   │   ├── services/       # 業務邏輯（資料處理、快取）
│   │   └── api/            # API 端點
│   ├── Dockerfile
│   ├── .env                # 後端環境變數
│   ├── .env.example        # 環境變數範本
│   └── requirements.txt    # Python 依賴
│
├── 📚 docs/                # 教學文件
│   ├── template/           # PM 工作流程 Skill 模板
│   │   ├── PainAnalysis-SKILL.md              # Step 1: 痛點分析助手
│   │   ├── OpportunitySolutionTree-SKILL.md   # Step 2: OST 探索助手
│   │   ├── UserStory-SKILL.md                 # Step 3: User Story 拆解助手
│   │   ├── feature-spec-template-v2.md        # 功能規格編寫範本
│   │   ├── acceptance-criteria-guide.md       # AC 驗收條件指南
│   │   └── prototype-guide.md                 # Prototype 編寫指南
│   │
│   ├── reference/          # 參考文檔
│   │   ├── PRD.md                    # 完整產品規格書
│   │   ├── step0-painpoint-ref.md    # 痛點案例參考
│   │   ├── 002-ScopeChangeWaterfallWidget.md  # 範例功能規格
│   │   ├── tech-overview.md          # 技術架構說明
│   │   └── table-schema.md           # 資料結構定義
│   │
│   └── prototype/          # 原型示例
│
├── docker-compose.yml         # 示範模式（給學員用）
├── docker-compose.dev.yml     # 開發模式（開發人員用）
├── docker-compose.prod.yml    # 課堂快速啟動（預構建版本）
└── README.md                  # 本檔案
```

**給 PM 學員的重點**：
- 🎯 **frontend/** - 看得到的儀表板界面
- 🎯 **backend/** - 資料處理和計算邏輯
- 🎯 **docs/template/** - PM 工作流程 Skill 助手（Step 1-3）
- 🎯 **docs/reference/** - 完整功能規格、技術架構、資料結構

## 環境變數

專案使用 `.env` 檔案管理環境變數。預設值已提供在 `.env` 檔案中。

### 修改環境變數

如需修改環境變數，編輯對應的 `.env` 檔案：

- **後端**: `backend/.env` - Google Sheets 配置、快取設定、伺服器設定
- **前端**: `frontend/.env` - API 端點、應用程式名稱

**範例**（參考 `.env.example`）：

**backend/.env**
```bash
GoogleSheets__SheetId=YOUR_SHEET_ID
GoogleSheets__RawDataSheet=rawData
GoogleSheets__SprintSheet=GetJiraSprintValues
CacheDuration=300
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

**frontend/.env**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_TITLE=Jira Dashboard
```

> ℹ️ **.env 檔案已被 .gitignore 忽略**，不會提交到 git。修改後重啟容器即可生效。

## 資料來源

本應用程式使用 Google Sheets 作為資料來源：

- **Sheet ID**: `1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM`
- **rawData 工作表**: 包含 23 個欄位的 Issue 資料（A:W）
- **GetJiraSprintValues 工作表**: 包含 9 個欄位的 Sprint 資料（A:I）

資料通過 Google Sheets 的公開 CSV 匯出 URL 取得，無需 API 金鑰。

## 故障排除

### 問題 1: 無法連接 Google Sheets

**解決方案:**
- 驗證 Sheet ID 是否正確
- 檢查 Google Sheets 是否為公開分享
- 確認網路連接

### 問題 2: CORS 錯誤

**解決方案:**
- 確認後端正在執行 (http://localhost:8000)
- 檢查 NEXT_PUBLIC_API_URL 是否正確設置
- 重啟前端開發伺服器

### 問題 3: Port 已被使用

**解決方案:**
```bash
# 查找佔用端口的進程
lsof -i :8000   # 後端
lsof -i :3000   # 前端

# 終止進程
kill -9 <PID>
```

## 📖 PM 工作流程指南

本課程提供一套完整的 **AI 協作式產品探索流程**，從痛點分析到規格撰寫：

### Step 1: 痛點分析
- **工具**: [docs/template/PainAnalysis-SKILL.md](./docs/template/PainAnalysis-SKILL.md)
- **目的**: 深入理解使用者問題，而非跳到解法
- **輸出**: 結構化的問題假設報告

### Step 2: 機會探索（OST）
- **工具**: [docs/template/OpportunitySolutionTree-SKILL.md](./docs/template/OpportunitySolutionTree-SKILL.md)
- **目的**: 探索完整的機會與解法空間
- **輸出**: Outcome → Opportunities → Solutions → Experiments

### Step 3: User Story 拆解
- **工具**: [docs/template/UserStory-SKILL.md](./docs/template/UserStory-SKILL.md)
- **目的**: 將解法拆解成真實反映使用者意圖的故事
- **輸出**: 結構化的 User Stories

### Step 4：驗收條件（AC）
- **工具**: [docs/template/acceptance-criteria-SKILL.md](./docs/template/acceptance-criteria-SKILL.md)
- **目的**: 透過「釐清對談」定義明確的驗收條件（Gherkin 格式）
- **輸出**: Acceptance Criteria scenarios 與 Story → AC 對應表

### Step 5：規格撰寫（PRD）
- **工具**: [docs/skills/PRD.skill](./docs/skills/PRD.skill)
- **目的**: 整合前四步成果，透過逐題澄清確認所有關鍵決策
- **輸出**: 完整的 PRD 規格文檔

### 參考資料
- [PRD.md](./docs/reference/PRD.md) - 完整產品規格書範例
- [tech-overview.md](./docs/reference/tech-overview.md) - 技術架構與資料模型
- [table-schema.md](./docs/reference/table-schema.md) - Google Sheets 資料結構定義
- [prototype-guide.md](./docs/template/prototype-guide.md) - Prototype 編寫指南

## 授權

本專案為教學用途，遵循 MIT 授權。

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 作者
JUGG
