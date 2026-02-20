# Docker 建置與啟動錯誤排查記錄

**日期**: 2025-10-29
**階段**: 初次 Docker Compose 啟動
**狀態**: ✅ 已解決

---

## 錯誤總覽

在執行 `docker-compose up` 過程中遇到 4 個主要問題:

1. **npm ci 失敗** - 缺少 package-lock.json
2. **依賴版本衝突** - React 19 與 @testing-library/react 不相容
3. **TypeScript 編譯錯誤** - API 回應類型定義不一致
4. **Dockerfile 建置失敗** - 缺少 public 目錄
5. **Runtime 錯誤** - HTTP client 未跟隨 Google Sheets redirect

---

## 錯誤 1: npm ci 需要 package-lock.json

### 錯誤訊息
```
=> ERROR [frontend deps 3/3] RUN npm ci                                                                              1.7s
npm error code EUSAGE
npm error The `npm ci` command can only install with an existing package-lock.json or
npm error npm-shrinkwrap.json with lockfileVersion >= 1.
```

### 根本原因
- Dockerfile 第 9 行使用 `npm ci`,但 `frontend/package-lock.json` 不存在
- `npm ci` 是為 CI/CD 環境設計,需要 lock 檔案來確保依賴版本一致性

### 解決方案
**嘗試方案**: 在本地執行 `npm install` 生成 package-lock.json
**結果**: 觸發了錯誤 2

### 相關檔案
- `frontend/Dockerfile:9`
- `frontend/package.json`

---

## 錯誤 2: React 19 與測試函式庫版本衝突

### 錯誤訊息
```
npm error ERESOLVE unable to resolve dependency tree
npm error Found: react@19.0.0
npm error Could not resolve dependency:
npm error peer react@"^18.0.0" from @testing-library/react@14.3.1
```

### 根本原因
- 專案使用 React 19.0.0 (Next.js 15.2.4 需要)
- `@testing-library/react@^14.1.0` 只支援 React 18.x
- Peer dependency 衝突導致 npm install 失敗

### 解決方案
升級 `@testing-library/react` 到支援 React 19 的版本:

```diff
# frontend/package.json
  "devDependencies": {
-   "@testing-library/react": "^14.1.0",
+   "@testing-library/react": "^16.2.0",
+   "@testing-library/dom": "^10.4.0",
    "@testing-library/jest-dom": "^6.1.5",
```

### 技術背景
- `@testing-library/react` 從 v16.1.0 開始支援 React 19 (2024-12-05 發布)
- v16+ 需要同時安裝 `@testing-library/dom` 作為 peer dependency

### 相關檔案
- `frontend/package.json:29-30`

---

## 錯誤 3: TypeScript 編譯 - API 回應類型不一致

### 錯誤訊息
```
Failed to compile.

./src/hooks/useDashboardData.ts:42:47
Type error: Property 'distribution' does not exist on type 'StatusDistribution[]'.

  42 |         setStatusDistribution(distributionRes.distribution || distributionRes)
     |                                               ^
```

### 根本原因
**前後端類型不一致**:

- **後端** (`backend/src/api/routes.py:126-131`) 回傳物件:
  ```python
  {
    "distribution": [...],
    "totalIssueCount": ...,
    "timestamp": ...,
    "cacheHit": ...
  }
  ```

- **前端** (`frontend/src/services/api.ts:47`) 定義回傳陣列:
  ```typescript
  async getStatusDistribution(): Promise<StatusDistribution[]>
  ```

- **Hook** (`frontend/src/hooks/useDashboardData.ts:42`) 嘗試存取不存在的屬性:
  ```typescript
  setStatusDistribution(distributionRes.distribution || distributionRes)
  ```

### 解決方案

**步驟 1**: 新增 API 回應介面

```typescript
// frontend/src/services/api.ts
export interface StatusDistributionResponse {
  distribution: StatusDistribution[]
  totalIssueCount: number
  timestamp: string
  cacheHit: boolean
}
```

**步驟 2**: 更新 API 方法回傳類型

```diff
- async getStatusDistribution(): Promise<StatusDistribution[]>
+ async getStatusDistribution(): Promise<StatusDistributionResponse>
```

**步驟 3**: 修正 Hook 中的資料存取

```diff
- setStatusDistribution(distributionRes.distribution || distributionRes)
- setTotalIssueCount(distributionRes.totalIssueCount || 0)
+ setStatusDistribution(distributionRes.distribution)
+ setTotalIssueCount(distributionRes.totalIssueCount)
```

### 相關檔案
- `backend/src/api/routes.py:79-142`
- `frontend/src/services/api.ts:8-13, 55`
- `frontend/src/hooks/useDashboardData.ts:42-43`

---

## 錯誤 4: Next.js 配置警告與 Dockerfile 建置失敗

### 錯誤訊息 A: Next.js 配置警告
```
⚠ Invalid next.config.js options detected:
⚠   Unrecognized key(s) in object: 'swcMinify'
```

### 解決方案 A
移除過時的 `swcMinify` 選項 (Next.js 13+ 預設啟用):

```diff
# frontend/next.config.js
const nextConfig = {
  reactStrictMode: true,
- swcMinify: true,
  output: 'standalone',
}
```

### 錯誤訊息 B: Docker COPY 失敗
```
=> ERROR [frontend runner 2/4] COPY --from=builder /app/public ./public                                              0.0s
failed to solve: "/app/public": not found
```

### 根本原因
- Dockerfile 第 28 行期望複製 `public` 目錄
- 專案初始沒有創建 `public` 目錄
- Next.js 的 `output: 'standalone'` 模式需要複製 public 資源

### 解決方案
在 builder 階段確保目錄存在:

```diff
# frontend/Dockerfile
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

+# 確保 public 目錄存在
+RUN mkdir -p ./public

ENV NEXT_PUBLIC_API_URL=http://localhost:8000/api

RUN npm run build
```

### 相關檔案
- `frontend/next.config.js:4` (已移除)
- `frontend/Dockerfile:19`
- `frontend/public/` (新建)

---

## 錯誤 5: Google Sheets API Redirect 未跟隨

### 錯誤訊息
```
Error fetching Google Sheets data: Redirect response '307 Temporary Redirect' for url
'https://docs.google.com/spreadsheets/d/.../export?format=csv&gid=0'
Redirect location: 'https://doc-0g-0c-sheets.googleusercontent.com/export/...'
```

### 根本原因
- `httpx.AsyncClient` 預設不跟隨 HTTP redirects
- Google Sheets CSV export API 會先回傳 307 redirect 到實際的資料 URL
- 程式碼在 `google_sheets_service.py:43, 68` 沒有設定 `follow_redirects`

### 解決方案
在兩個 fetch 方法中啟用 redirect 跟隨:

```diff
# backend/src/services/google_sheets_service.py
- async with httpx.AsyncClient(timeout=30.0) as client:
+ async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
    response = await client.get(url)
```

### 修改位置
- `fetch_raw_data()` 方法 (第 43 行)
- `fetch_sprint_data()` 方法 (第 68 行)

### 相關檔案
- `backend/src/services/google_sheets_service.py:43, 68`

---

## 驗證方式

### 1. Frontend 建置成功
```bash
$ docker-compose logs frontend | grep "Compiled successfully"
✓ Compiled successfully
```

### 2. Backend API 正常回應
```bash
$ curl http://localhost:8000/api/dashboard/metrics?sprint=All
{
  "totalIssueCount": ...,
  "totalStoryPoints": ...,
  ...
}
```

### 3. Frontend 頁面載入
```bash
$ curl http://localhost:3000
# 應回傳 HTML 內容
```

---

## 經驗總結

### 🔍 診斷技巧
1. **逐層檢查**: Docker 多階段建置錯誤需要從 deps → builder → runner 逐層排查
2. **類型一致性**: 前後端整合時務必對照實際 API 回應格式
3. **HTTP 語意**: 注意 HTTP client library 的預設行為 (redirect, timeout 等)

### 🛠️ 預防措施
1. **Lock 檔案**: 專案初始化時就應生成 package-lock.json
2. **版本相容性**: 升級主要依賴 (React) 時檢查生態系相容性
3. **Contract Testing**: 前後端使用共享的 API schema (如 OpenAPI)
4. **基礎結構**: Dockerfile 應 gracefully handle 可選目錄

### 📚 技術債務
- [ ] 考慮使用 OpenAPI 生成 TypeScript 類型定義
- [ ] 新增 Docker healthcheck 驗證服務啟動狀態
- [ ] 設定 pre-commit hook 執行 TypeScript 類型檢查

---

## 相關文件
- [Next.js 15 升級指南](https://nextjs.org/docs/app/building-your-application/upgrading/version-15)
- [httpx redirect 設定](https://www.python-httpx.org/advanced/#redirect-following)
- [React 19 升級指南](https://react.dev/blog/2024/04/25/react-19-upgrade-guide)
