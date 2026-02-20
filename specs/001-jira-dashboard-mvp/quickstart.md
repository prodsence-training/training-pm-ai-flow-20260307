# 快速開始: Jira Dashboard MVP v1.0

**Date**: 2025-10-29 | **適用版本**: 1.0.0+

---

## 前置需求

### 系統要求

- **Node.js**: 18.17+ (前端開發)
- **Python**: 3.11+ (後端開發)
- **Docker**: 20.10+ (容器化部署)
- **Docker Compose**: 2.0+ (本地測試)
- **Git**: 2.30+ (版本管理)

### 開發工具

- **VS Code** 或其他編輯器 (推薦 VS Code 搭配 Python + ESLint 擴展)
- **Postman** 或 **Thunder Client** (API 測試)
- **Chrome DevTools** (前端除錯)

### Google Sheets 存取

- Google Sheets 公開分享連結（已預設）
- Sheet ID: `1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM`
- 包含 rawData 和 GetJiraSprintValues 工作表

---

## 本地開發設置

### 1. 克隆或初始化專案

```bash
# 如果尚未初始化
git clone [repository-url]
cd training-youtube-spec-kit

# 驗證專案結構
ls -la frontend backend Makefile docker-compose.yml
```

### 2. 環境變數配置

#### 後端環境變數

創建 `backend/.env` 文件：

```bash
# Google Sheets 配置
GoogleSheets__SheetId=1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM
GoogleSheets__RawDataSheet=rawData
GoogleSheets__SprintSheet=GetJiraSprintValues

# 快取配置
CacheDuration=300  # 5 minutes (秒)

# 伺服器配置
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

#### 前端環境變數

創建 `frontend/.env.local` 文件：

```bash
# API 後端位址（開發時）
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# 應用配置
NEXT_PUBLIC_APP_TITLE=Jira Dashboard
```

### 3. 後端開發伺服器

#### 選項 A: 使用 Python virtualenv（推薦）

```bash
# 進入後端目錄
cd backend

# 建立虛擬環境
python3.11 -m venv venv

# 啟動虛擬環境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt

# 運行伺服器
python src/main.py
```

伺服器應在 `http://localhost:8000` 啟動

#### 選項 B: 使用 Docker

```bash
# 建構後端映像
docker build -t jira-dashboard-backend ./backend

# 運行後端容器
docker run -p 8000:8000 \
  -e GoogleSheets__SheetId=1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM \
  -e GoogleSheets__RawDataSheet=rawData \
  -e GoogleSheets__SprintSheet=GetJiraSprintValues \
  -e CacheDuration=300 \
  jira-dashboard-backend
```

### 4. 前端開發伺服器

```bash
# 進入前端目錄
cd frontend

# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev
```

前端應在 `http://localhost:3000` 啟動

### 5. 驗證本地設置

#### 後端 API 檢查

```bash
# 檢查伺服器是否運行
curl http://localhost:8000

# 取得指標資料
curl http://localhost:8000/api/dashboard/metrics

# 取得狀態分布
curl http://localhost:8000/api/dashboard/status-distribution

# 取得 Sprint 選項
curl http://localhost:8000/api/sprints
```

預期回應 (200 OK 包含 JSON 資料)

#### 前端檢查

- 在瀏覽器開啟 `http://localhost:3000`
- 應看到 Loading Spinner (如果後端正在連接 Google Sheets)
- 3-5 秒後應顯示四個統計卡片 + 長條圖 + Sprint 篩選器

---

## 使用 Docker Compose 運行完整應用

### 快速啟動

```bash
# 從專案根目錄
cd /path/to/training-youtube-spec-kit

# 啟動所有服務
docker-compose up

# 背景運行
docker-compose up -d
```

### 驗證容器狀態

```bash
# 檢查運行中的容器
docker-compose ps

# 檢查後端日誌
docker-compose logs backend

# 檢查前端日誌
docker-compose logs frontend

# 跟隨即時日誌
docker-compose logs -f
```

### 服務存取

- **前端**: `http://localhost:3000`
- **後端 API**: `http://localhost:8000/api`
- **API 文檔**: `http://localhost:8000/docs` (FastAPI Swagger UI)

### 停止服務

```bash
# 停止並移除容器
docker-compose down

# 停止但保留容器（用於重啟）
docker-compose stop

# 重啟容器
docker-compose restart
```

### 清理與重建

```bash
# 移除所有容器、網路和匿名卷
docker-compose down -v

# 重建映像
docker-compose build --no-cache

# 啟動新映像
docker-compose up
```

---

## Makefile 便利指令

如果專案包含 `Makefile`，可使用以下指令：

```bash
# 查看所有可用指令
make help

# 安裝依賴
make install

# 運行開發伺服器
make dev

# 運行測試
make test

# 執行 linting
make lint

# 構建生產版本
make build

# Docker Compose 操作
make docker-up
make docker-down
make docker-logs
```

---

## API 測試

### 使用 cURL

```bash
# 基本測試 - 所有 Sprint 的指標
curl -X GET "http://localhost:8000/api/dashboard/metrics?sprint=All" \
  -H "Content-Type: application/json"

# 特定 Sprint 的指標
curl -X GET "http://localhost:8000/api/dashboard/metrics?sprint=DEMO1-Sprint%201" \
  -H "Content-Type: application/json"

# 狀態分布
curl -X GET "http://localhost:8000/api/dashboard/status-distribution?sprint=All" \
  -H "Content-Type: application/json"

# Sprint 篩選選項
curl -X GET "http://localhost:8000/api/sprints" \
  -H "Content-Type: application/json"
```

### 使用 Postman

1. 開啟 Postman
2. 建立新的 Collection: "Jira Dashboard MVP"
3. 新增以下請求：

**請求 1: Get Metrics**
- Method: GET
- URL: `http://localhost:8000/api/dashboard/metrics`
- Query Params: `sprint=All`
- 預期: 200 OK with metrics JSON

**請求 2: Get Status Distribution**
- Method: GET
- URL: `http://localhost:8000/api/dashboard/status-distribution`
- Query Params: `sprint=All`
- 預期: 200 OK with distribution array

**請求 3: Get Sprints**
- Method: GET
- URL: `http://localhost:8000/api/sprints`
- 預期: 200 OK with sprint options list

### 使用 FastAPI Swagger UI

1. 導航到 `http://localhost:8000/docs`
2. 展開各個端點
3. 點擊 "Try it out"
4. 修改參數並執行請求
5. 查看回應

---

## 測試執行

### 後端單元測試

```bash
cd backend

# 運行所有測試
pytest

# 運行特定測試文件
pytest tests/unit/test_data_processor.py

# 運行帶覆蓋率報告
pytest --cov=src --cov-report=html

# 詳細輸出
pytest -v
```

### 後端整合測試

```bash
cd backend

# 運行整合測試（需要後端服務運行）
pytest tests/integration/

# 測試 API 端點
pytest tests/integration/test_api_endpoints.py::test_metrics_endpoint
```

### 前端單元測試

```bash
cd frontend

# 運行所有測試
npm test

# 互動式監視模式
npm test -- --watch

# 生成覆蓋率報告
npm test -- --coverage
```

### 前端端到端測試

```bash
cd frontend

# 使用 Playwright 執行 E2E 測試
npx playwright test

# 打開 Playwright UI 模式
npx playwright test --ui

# 執行特定測試案例
npx playwright test tests/e2e/dashboard.spec.ts
```

### 負載測試（驗證 100 並發使用者）

```bash
# 使用 k6 執行負載測試
k6 run tests/load/concurrent-users.js

# 或使用 Locust
cd backend/tests/load
locust -f locustfile.py --host=http://localhost:8000
```

---

## 測試資料準備

### 為測試案例準備 Google Sheets 資料

根據 `testcases.md` 的需求，建議準備以下測試資料集：

#### **TC-DASHBOARD-002 測試資料集**

在 Google Sheets rawData 工作表中準備：

| Key | Status | Story Points | (其他欄位) |
|-----|--------|--------------|-----------|
| TEST-1 | Done | 3.5 | ... |
| TEST-2 | In Progress | 5 | ... |
| TEST-3 | Done | 2 | ... |
| TEST-4 | To Do | 8 | ... |
| TEST-5 | Done | 5 | ... |
| TEST-6 | Waiting | 0 | ... |
| TEST-7 | Done | 2 | ... |
| TEST-8 | Backlog | 0 | ... |
| TEST-9 | Ready to Verify | 0 | ... |
| TEST-10 | Evaluated | 0 | ... |

**預期統計**:
- Total Issue Count: 10
- Total Story Points: 25.5
- Total Done Item Count: 4
- Done Story Points: 12.5

#### **TC-EDGE-002 測試資料集（無效 Status）**

準備包含無效 Status 的資料：

| Key | Status | Story Points |
|-----|--------|--------------|
| VALID-1 | Done | 5 |
| VALID-2 | In Progress | 3 |
| INVALID-1 | **Unknown** | 2 |
| INVALID-2 | **Testing** | 1 |
| INVALID-3 | **Archive** | 0 |

**預期結果**:
- Total Issue Count: 5 (包含無效 Status)
- 長條圖總計: 2 (僅有效 Status)

#### **TC-EDGE-003 測試資料集（非數值 Story Points）**

| Key | Status | Story Points |
|-----|--------|--------------|
| NUM-1 | Done | 5 |
| NUM-2 | To Do | 10 |
| INVALID-1 | In Progress | **TBD** |
| INVALID-2 | Backlog | **N/A** |
| EMPTY-1 | Waiting | *(空值)* |

**預期結果**:
- Total Issue Count: 5
- Total Story Points: 15 (非數值視為 0)

#### **TC-FILTER-004 測試資料集（重複 Sprint Name）**

在 GetJiraSprintValues 工作表中準備：

| Board ID | Board Name | Sprint Name | Sprint ID | state |
|----------|-----------|-------------|-----------|-------|
| 1 | Board A | Sprint 1 | 11 | active |
| 1 | Board A | Sprint 1 | 15 | closed |
| 1 | Board A | Sprint 2 | 20 | active |

**預期下拉選項**:
- All
- Sprint 1 (11)
- Sprint 1 (15)
- Sprint 2
- No Sprints

### 使用測試資料的最佳實踐

1. **建立專用測試 Sheet**: 複製主 Google Sheet 作為測試環境
2. **使用環境變數切換**:
   ```bash
   # 開發環境
   GoogleSheets__SheetId=1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM

   # 測試環境
   GoogleSheets__SheetId=TEST_SHEET_ID_HERE
   ```
3. **測試前後清理**: 確保測試資料不影響生產環境

---

## 常見問題與排除故障

### 問題 1: 後端無法連接 Google Sheets

**症狀**: 後端返回 500 錯誤，日誌顯示 "Failed to connect to Google Sheets"

**解決方案**:
```bash
# 1. 驗證 Sheet ID 是否正確
echo $GoogleSheets__SheetId

# 2. 在瀏覽器驗證公開連結是否可存取
# 訪問: https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv

# 3. 檢查網路連接
ping docs.google.com

# 4. 查看後端日誌
docker-compose logs backend
```

### 問題 2: CORS 錯誤 (前端無法存取後端)

**症狀**: 前端 console 顯示 "Access-Control-Allow-Origin 錯誤"

**解決方案**:
```bash
# 後端應自動處理 CORS，但如果仍有問題：
# 1. 確認後端正在運行: http://localhost:8000
# 2. 確認 NEXT_PUBLIC_API_URL 正確設置
# 3. 重啟前端開發伺服器
cd frontend && npm run dev

# 4. 檢查後端 CORS 配置（應在 main.py）
```

### 問題 3: Port 已在使用

**症狀**: `Address already in use` 錯誤

**解決方案**:
```bash
# 查找佔用端口的進程
lsof -i :8000   # 後端
lsof -i :3000   # 前端

# 終止進程
kill -9 <PID>

# 或使用不同的端口
PORT=8001 python src/main.py  # 後端
PORT=3001 npm run dev         # 前端
```

### 問題 4: Node modules 或依賴衝突

**症狀**: `npm install` 失敗或奇怪的 JavaScript 錯誤

**解決方案**:
```bash
# 清除快取並重新安裝
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# 對於 Python
cd backend
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 問題 5: 載入時間過長

**症狀**: 前端載入 spinner 超過 5 秒

**可能原因**:
- Google Sheets 無法存取（檢查網路）
- 資料過大（>10,000 Issue）
- 後端伺服器資源不足

**診斷**:
```bash
# 測試 Google Sheets 連接速度
time curl "https://docs.google.com/spreadsheets/d/1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM/export?format=csv"

# 檢查後端效能
curl -i http://localhost:8000/api/dashboard/metrics

# 檢查系統資源
docker stats  # 或 top/Activity Monitor
```

---

## 開發工作流程

### 修改後端程式碼

```bash
# 1. 編輯 backend/src/services/data_processor.py
# 2. 測試修改
cd backend && pytest tests/unit/test_data_processor.py
# 3. 後端開發伺服器會自動重載（watchdog）
# 4. 測試 API
curl http://localhost:8000/api/dashboard/metrics
```

### 修改前端程式碼

```bash
# 1. 編輯 frontend/src/components/MetricCard.tsx
# 2. 保存時自動編譯（Next.js hot reload）
# 3. 瀏覽器自動刷新（如果設置了 hot reload）
# 4. 執行前端測試
cd frontend && npm test
```

### 新增功能

1. 在 `spec.md` 中編寫 Acceptance Criteria
2. 在 `data-model.md` 中更新實體定義
3. 在 `contracts/api-endpoints.md` 中定義 API 契約
4. 編寫測試（TDD 方式）
5. 實作功能
6. 運行所有測試
7. 建立 PR

---

## 效能調試

### 後端效能分析

```bash
# 安裝效能分析工具
pip install py-spy

# 執行效能分析
py-spy record -o profile.svg python src/main.py

# 訪問端點
curl http://localhost:8000/api/dashboard/metrics

# 查看生成的 flame graph
open profile.svg
```

### 前端效能分析

```bash
# 使用 Chrome DevTools 的 Performance 標籤
# 或使用 Next.js 分析工具

ANALYZE=true npm run build

# 查看包大小
npm run build -- --analyze
```

---

## 生產部署 (Docker)

### 構建生產映像

```bash
# 構建後端映像
docker build -t jira-dashboard-backend:1.0.0 ./backend

# 構建前端映像
docker build -t jira-dashboard-frontend:1.0.0 ./frontend

# 標記版本
docker tag jira-dashboard-backend:1.0.0 myregistry/jira-dashboard-backend:1.0.0
docker tag jira-dashboard-frontend:1.0.0 myregistry/jira-dashboard-frontend:1.0.0
```

### 使用生產 docker-compose

創建 `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  frontend:
    image: myregistry/jira-dashboard-frontend:1.0.0
    ports:
      - "80:3000"
    environment:
      - NEXT_PUBLIC_API_URL=https://api.example.com

  backend:
    image: myregistry/jira-dashboard-backend:1.0.0
    ports:
      - "8000:8000"
    environment:
      - GoogleSheets__SheetId=1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM
      - GoogleSheets__RawDataSheet=rawData
      - GoogleSheets__SprintSheet=GetJiraSprintValues
      - CacheDuration=300
```

---

## 相關文件

- [spec.md](./spec.md) - 完整功能規格
- [data-model.md](./data-model.md) - 資料模型定義
- [contracts/api-endpoints.md](./contracts/api-endpoints.md) - API 契約
- [../../docs/tech-overview.md](../../docs/tech-overview.md) - 技術架構
- [../../docs/table-schema.md](../../docs/table-schema.md) - Google Sheets 資料結構

---

## 取得幫助

- **技術問題**: 查看相關文檔或檢查 GitHub Issues
- **API 文檔**: 訪問 `http://localhost:8000/docs` (Swagger UI)
- **代碼貢獻**: 參見 CONTRIBUTING.md

