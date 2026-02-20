# Test Cases: Jira Dashboard MVP v1.0

**Feature Branch**: `001-jira-dashboard-mvp`
**Created**: 2025-10-29
**Status**: Draft

本文件包含 Jira Dashboard MVP v1.0 的完整測試案例，基於 spec.md 中的 User Stories 和 Acceptance Criteria 生成。

---

## User Story 1: 即時專案健康度監控

### TC-DASHBOARD-001

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-DASHBOARD-001 |
| **測試目標** | 驗證儀表板首頁顯示四個統計卡片 |
| **相關 User Story** | US1: 作為專案經理，我希望能在儀表板上即時查看專案的關鍵統計指標，以便快速了解專案整體健康度和進度狀況 |
| **相關 AC 場景** | AC1: Given 使用者開啟 Jira Dashboard 首頁，When 頁面載入完成，Then 應顯示四個統計卡片 |
| **測試前置條件** | 1. 應用程式已部署並可存取<br>2. Google Sheets rawData 工作表包含測試資料<br>3. 瀏覽器為現代版本（Chrome/Firefox/Safari/Edge） |
| **測試步驟** | 1. 開啟瀏覽器<br>2. 導航至 Jira Dashboard 首頁 URL<br>3. 等待頁面完全載入（出現所有內容） |
| **預期結果** | 1. 頁面標題顯示「Jira Dashboard」<br>2. 頁面顯示四個統計卡片：<br>   - Total Issue Count（含文件圖標）<br>   - Total Story Points（含目標圖標）<br>   - Total Done Item Count（含勾選圖標）<br>   - Done Story Points（含時鐘圖標）<br>3. 所有卡片排列整齊且視覺設計使用藍色主題（#3b82f6） |
| **測試資料** | N/A（視覺化測試） |
| **測試類型** | 功能測試（正常流程） |
| **自動化程度** | 全自動（E2E 測試 - Playwright/Cypress） |

---

### TC-DASHBOARD-002

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-DASHBOARD-002 |
| **測試目標** | 驗證統計卡片顯示正確的計算數值 |
| **相關 User Story** | US1: 作為專案經理，我希望能在儀表板上即時查看專案的關鍵統計指標 |
| **相關 AC 場景** | AC2: Given Google Sheets rawData 工作表包含 Issue 資料，When 使用者查看統計卡片，Then 每個卡片應顯示正確的統計數值 |
| **測試前置條件** | 1. Google Sheets rawData 工作表包含已知數量的測試資料<br>2. 測試資料包含不同 Status 的 Issue<br>3. 測試資料包含整數和小數的 Story Points |
| **測試步驟** | 1. 準備測試資料集：<br>   - 總計 10 筆 Issue<br>   - 其中 4 筆 Status 為「Done」<br>   - Total Story Points: 25.5（包含小數點）<br>   - Done Story Points: 12.5<br>2. 開啟 Jira Dashboard 首頁<br>3. 記錄四個卡片顯示的數值<br>4. 與預期值比對 |
| **預期結果** | 1. Total Issue Count 顯示：10<br>2. Total Story Points 顯示：25.5<br>3. Total Done Item Count 顯示：4<br>4. Done Story Points 顯示：12.5<br>5. 所有數值計算準確率達 100% |
| **測試資料** | **rawData 測試資料集**：<br>- Issue 1: Status=Done, Story Points=3.5<br>- Issue 2: Status=In Progress, Story Points=5<br>- Issue 3: Status=Done, Story Points=2<br>- Issue 4: Status=To Do, Story Points=8<br>- Issue 5: Status=Done, Story Points=5<br>- Issue 6: Status=Waiting, Story Points=0<br>- Issue 7: Status=Done, Story Points=2<br>- Issue 8: Status=Backlog, Story Points=0<br>- Issue 9: Status=Ready to Verify, Story Points=0<br>- Issue 10: Status=Evaluated, Story Points=0 |
| **測試類型** | 功能測試（數值驗證） |
| **自動化程度** | 全自動（E2E 測試 + API 驗證） |

---

### TC-DASHBOARD-003

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-DASHBOARD-003 |
| **測試目標** | 驗證無資料或無法連接時的空狀態處理 |
| **相關 User Story** | US1: 作為專案經理，我希望能在儀表板上即時查看專案的關鍵統計指標 |
| **相關 AC 場景** | AC3: Given Google Sheets rawData 工作表無資料或無法連接，When 使用者查看統計卡片，Then 應顯示 0 或適當的空狀態提示 |
| **測試前置條件** | 1. 能夠控制 Google Sheets 連接狀態（測試環境）<br>2. 或使用空的 rawData 工作表 |
| **測試步驟** | **情境 A：空資料表**<br>1. 清空 Google Sheets rawData 工作表所有資料（僅保留標題列）<br>2. 開啟 Jira Dashboard 首頁<br>3. 檢查統計卡片顯示<br><br>**情境 B：無法連接**<br>1. 模擬網路錯誤或 API 失效<br>2. 開啟 Jira Dashboard 首頁<br>3. 檢查錯誤提示 |
| **預期結果** | **情境 A**：<br>1. Total Issue Count 顯示：0<br>2. Total Story Points 顯示：0<br>3. Total Done Item Count 顯示：0<br>4. Done Story Points 顯示：0<br><br>**情境 B**：<br>1. 頁面顯示友善的錯誤訊息（而非崩潰）<br>2. 錯誤訊息在 3 秒內顯示<br>3. 錯誤訊息清楚說明無法連接 Google Sheets |
| **測試資料** | 空資料表或模擬連接失敗 |
| **測試類型** | 異常測試（錯誤處理） |
| **自動化程度** | 半自動（需手動模擬網路錯誤） |

---

### TC-DASHBOARD-004

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-DASHBOARD-004 |
| **測試目標** | 驗證資料更新後快取過期機制 |
| **相關 User Story** | US1: 作為專案經理，我希望能在儀表板上即時查看專案的關鍵統計指標 |
| **相關 AC 場景** | AC4: Given 統計資料已顯示，When Google Sheets 資料更新且快取過期（5分鐘），Then 重新整理頁面後應顯示更新後的數值 |
| **測試前置條件** | 1. Jira Dashboard 已開啟並載入初始資料<br>2. 能夠編輯 Google Sheets rawData 工作表<br>3. 能夠等待至少 5 分鐘或手動清除快取 |
| **測試步驟** | 1. 開啟 Jira Dashboard，記錄初始統計數值（例如 Total Issue Count = 10）<br>2. 在 Google Sheets rawData 工作表新增 3 筆 Issue<br>3. 立即重新整理頁面，記錄數值（應維持 10，因快取未過期）<br>4. 等待 5 分鐘後重新整理頁面<br>5. 檢查統計數值是否更新 |
| **預期結果** | 1. 步驟 3：Total Issue Count 仍顯示 10（快取生效）<br>2. 步驟 5：Total Issue Count 顯示 13（快取過期，資料更新）<br>3. 其他統計卡片數值也相應更新 |
| **測試資料** | 初始：10 筆 Issue<br>更新後：13 筆 Issue |
| **測試類型** | 功能測試（快取機制） |
| **自動化程度** | 半自動（需等待時間） |

---

## User Story 2: Issue 狀態分布視覺化

### TC-CHART-001

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-CHART-001 |
| **測試目標** | 驗證 Issue 狀態分布長條圖顯示 |
| **相關 User Story** | US2: 作為團隊領導，我希望能透過長條圖查看 Issue 在各個狀態的分布情況 |
| **相關 AC 場景** | AC1: Given 使用者開啟 Jira Dashboard，When 頁面載入完成，Then 應顯示 Issue 狀態分布長條圖 |
| **測試前置條件** | 1. Google Sheets rawData 工作表包含測試資料<br>2. 測試資料涵蓋多種不同狀態的 Issue |
| **測試步驟** | 1. 開啟 Jira Dashboard 首頁<br>2. 等待頁面完全載入<br>3. 檢查頁面是否顯示長條圖元件 |
| **預期結果** | 1. 頁面在統計卡片下方顯示長條圖<br>2. 長條圖標題清楚標示為「Issue 狀態分布」或類似名稱<br>3. 長條圖使用藍色主題（#3b82f6）<br>4. 長條圖底部顯示總 Issue 數量統計 |
| **測試資料** | N/A（視覺化測試） |
| **測試類型** | 功能測試（正常流程） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-CHART-002

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-CHART-002 |
| **測試目標** | 驗證長條圖按固定順序顯示 9 個狀態 |
| **相關 User Story** | US2: 作為團隊領導，我希望能透過長條圖查看 Issue 在各個狀態的分布情況 |
| **相關 AC 場景** | AC2: Given 長條圖已顯示，When 使用者查看圖表，Then 應按照固定順序顯示 9 個狀態 |
| **測試前置條件** | 1. Google Sheets rawData 工作表包含所有 9 種狀態的 Issue<br>2. 長條圖已成功載入 |
| **測試步驟** | 1. 開啟 Jira Dashboard 首頁<br>2. 檢查長條圖的 X 軸標籤順序<br>3. 驗證每個狀態是否存在且順序正確 |
| **預期結果** | 1. 長條圖顯示以下 9 個狀態（由左至右順序）：<br>   - Backlog<br>   - Evaluated<br>   - To Do<br>   - In Progress<br>   - Waiting<br>   - Ready to Verify<br>   - Done<br>   - Invalid<br>   - Routine<br>2. 狀態順序固定不變，不受資料影響<br>3. 所有狀態都顯示，即使某狀態的 Issue 數量為 0 |
| **測試資料** | **rawData 測試資料集（涵蓋所有狀態）**：<br>- 2 筆 Backlog<br>- 1 筆 Evaluated<br>- 3 筆 To Do<br>- 5 筆 In Progress<br>- 2 筆 Waiting<br>- 4 筆 Ready to Verify<br>- 8 筆 Done<br>- 1 筆 Invalid<br>- 1 筆 Routine |
| **測試類型** | 功能測試（順序驗證） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-CHART-003

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-CHART-003 |
| **測試目標** | 驗證滑鼠懸停顯示詳細數值和百分比 |
| **相關 User Story** | US2: 作為團隊領導，我希望能透過長條圖查看 Issue 在各個狀態的分布情況 |
| **相關 AC 場景** | AC3: Given 使用者查看長條圖，When 滑鼠懸停在任一長條上，Then 應顯示該狀態的詳細數值和百分比 |
| **測試前置條件** | 1. 長條圖已成功載入<br>2. 測試資料包含可計算百分比的 Issue 數量 |
| **測試步驟** | 1. 開啟 Jira Dashboard 首頁<br>2. 將滑鼠移至「In Progress」狀態的長條上<br>3. 觀察是否出現 Tooltip（提示框）<br>4. 檢查 Tooltip 內容 |
| **預期結果** | 1. 滑鼠懸停後在 0.5 秒內顯示 Tooltip<br>2. Tooltip 包含以下資訊：<br>   - 狀態名稱（例如「In Progress」）<br>   - Issue 數量（例如「5」）<br>   - 百分比（例如「18.5%」，基於總 Issue 數 27）<br>3. Tooltip 格式清晰易讀 |
| **測試資料** | 總計 27 筆 Issue，其中 5 筆為 In Progress<br>預期百分比：5/27 ≈ 18.5% |
| **測試類型** | 功能測試（互動測試） |
| **自動化程度** | 全自動（E2E 測試 - 支援滑鼠事件） |

---

### TC-CHART-004

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-CHART-004 |
| **測試目標** | 驗證長條圖底部顯示總 Issue 數量統計 |
| **相關 User Story** | US2: 作為團隊領導，我希望能透過長條圖查看 Issue 在各個狀態的分布情況 |
| **相關 AC 場景** | AC4: Given 長條圖已顯示，When 使用者查看圖表底部，Then 應顯示總 Issue 數量統計 |
| **測試前置條件** | 1. Google Sheets rawData 工作表包含已知數量的 Issue<br>2. 長條圖已成功載入 |
| **測試步驟** | 1. 準備測試資料：共 30 筆 Issue<br>2. 開啟 Jira Dashboard 首頁<br>3. 檢查長條圖底部或標題區域是否顯示總數 |
| **預期結果** | 1. 長條圖底部或標題區域顯示「Total Issues: 30」或類似文字<br>2. 數值與實際 rawData 筆數一致<br>3. 數值與 Total Issue Count 卡片一致 |
| **測試資料** | 30 筆 Issue（涵蓋各種狀態） |
| **測試類型** | 功能測試（數值驗證） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-CHART-005

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-CHART-005 |
| **測試目標** | 驗證無資料時的空狀態提示 |
| **相關 User Story** | US2: 作為團隊領導，我希望能透過長條圖查看 Issue 在各個狀態的分布情況 |
| **相關 AC 場景** | AC5: Given Google Sheets rawData 工作表無資料，When 使用者查看長條圖區域，Then 應顯示友善的空狀態提示訊息 |
| **測試前置條件** | 1. Google Sheets rawData 工作表為空（僅保留標題列） |
| **測試步驟** | 1. 清空 rawData 工作表所有資料列<br>2. 開啟 Jira Dashboard 首頁<br>3. 檢查長條圖區域的顯示內容 |
| **預期結果** | 1. 長條圖區域顯示空狀態提示訊息<br>2. 提示訊息內容友善且清楚（例如「目前沒有資料可顯示」或「No data available」）<br>3. 不顯示空的長條圖或錯誤訊息 |
| **測試資料** | 空資料表 |
| **測試類型** | 異常測試（空狀態處理） |
| **自動化程度** | 全自動（E2E 測試） |

---

## User Story 3: Sprint 篩選功能

### TC-FILTER-001

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-FILTER-001 |
| **測試目標** | 驗證 Sprint 篩選器下拉選單顯示 |
| **相關 User Story** | US3: 作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint |
| **相關 AC 場景** | AC1: Given 使用者開啟 Jira Dashboard，When 頁面載入完成，Then 頂部應顯示 Sprint 篩選器下拉選單 |
| **測試前置條件** | 1. 應用程式已部署並可存取<br>2. Google Sheets GetJiraSprintValues 工作表包含 Sprint 資料 |
| **測試步驟** | 1. 開啟 Jira Dashboard 首頁<br>2. 等待頁面完全載入<br>3. 檢查頁面頂部區域 |
| **預期結果** | 1. 頁面頂部（統計卡片上方）顯示 Sprint 篩選器下拉選單<br>2. 下拉選單有清楚的標籤（例如「Select Sprint」）<br>3. 下拉選單預設值為「All」 |
| **測試資料** | N/A（視覺化測試） |
| **測試類型** | 功能測試（正常流程） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-FILTER-002

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-FILTER-002 |
| **測試目標** | 驗證 Sprint 篩選器選項完整性 |
| **相關 User Story** | US3: 作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint |
| **相關 AC 場景** | AC2: Given Sprint 篩選器已顯示，When 使用者點擊下拉選單，Then 應顯示「All」、所有有效的 Sprint 名稱、以及「No Sprints」選項 |
| **測試前置條件** | 1. Google Sheets GetJiraSprintValues 工作表包含已知的 Sprint 資料<br>2. Sprint 資料包含至少 3 個不同的 Sprint |
| **測試步驟** | 1. 準備測試資料：GetJiraSprintValues 包含 Sprint A、Sprint B、Sprint C<br>2. 開啟 Jira Dashboard 首頁<br>3. 點擊 Sprint 篩選器下拉選單<br>4. 檢查所有可選選項 |
| **預期結果** | 1. 下拉選單包含以下選項（由上至下）：<br>   - All<br>   - Sprint A<br>   - Sprint B<br>   - Sprint C<br>   - No Sprints<br>2. 所有選項都可點擊選擇<br>3. 選項數量與 GetJiraSprintValues 工作表的 Sprint 數量 + 2（All 和 No Sprints）一致 |
| **測試資料** | **GetJiraSprintValues 測試資料**：<br>- Sprint A (ID: 101)<br>- Sprint B (ID: 102)<br>- Sprint C (ID: 103) |
| **測試類型** | 功能測試（選項驗證） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-FILTER-003

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-FILTER-003 |
| **測試目標** | 驗證 Sprint 選項從正確的工作表欄位讀取 |
| **相關 User Story** | US3: 作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint |
| **相關 AC 場景** | AC3: Given Sprint 篩選器選項來自 Google Sheets GetJiraSprintValues 工作表，When 系統載入 Sprint 選項，Then 應從 Column C（Sprint Name）和 Column D（Sprint ID）讀取資料 |
| **測試前置條件** | 1. Google Sheets GetJiraSprintValues 工作表結構正確（A:I 欄位）<br>2. Column C 包含 Sprint Name，Column D 包含 Sprint ID |
| **測試步驟** | 1. 準備測試資料：在 GetJiraSprintValues 設定<br>   - Column C: "Development Sprint"<br>   - Column D: "201"<br>2. 開啟 Jira Dashboard 首頁<br>3. 點擊 Sprint 篩選器下拉選單<br>4. 檢查是否顯示「Development Sprint」選項 |
| **預期結果** | 1. 下拉選單顯示「Development Sprint」選項<br>2. 系統正確讀取 Column C 和 Column D 的資料<br>3. Sprint ID (201) 用於後續篩選邏輯（但不一定顯示在選單中，除非有重複名稱） |
| **測試資料** | GetJiraSprintValues Column C: "Development Sprint", Column D: "201" |
| **測試類型** | 功能測試（資料讀取） |
| **自動化程度** | 全自動（API 驗證 + E2E 測試） |

---

### TC-FILTER-004

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-FILTER-004 |
| **測試目標** | 驗證重複 Sprint Name 的處理（顯示 Sprint ID） |
| **相關 User Story** | US3: 作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint |
| **相關 AC 場景** | AC4: Given GetJiraSprintValues 工作表包含重複的 Sprint Name，When 系統生成篩選器選項，Then 應在重複的 Sprint Name 後加上 Sprint ID 以區分 |
| **測試前置條件** | 1. Google Sheets GetJiraSprintValues 工作表包含重複的 Sprint Name |
| **測試步驟** | 1. 準備測試資料：在 GetJiraSprintValues 設定<br>   - Row 1: Sprint Name="Sprint 1", Sprint ID="11"<br>   - Row 2: Sprint Name="Sprint 1", Sprint ID="15"<br>   - Row 3: Sprint Name="Sprint 2", Sprint ID="20"<br>2. 開啟 Jira Dashboard 首頁<br>3. 點擊 Sprint 篩選器下拉選單<br>4. 檢查重複 Sprint Name 的顯示格式 |
| **預期結果** | 1. 下拉選單顯示：<br>   - All<br>   - Sprint 1 (11)<br>   - Sprint 1 (15)<br>   - Sprint 2<br>   - No Sprints<br>2. 重複的「Sprint 1」名稱後加上 Sprint ID 區分<br>3. 唯一的「Sprint 2」不加 Sprint ID |
| **測試資料** | **GetJiraSprintValues 測試資料**：<br>- Sprint 1 (ID: 11)<br>- Sprint 1 (ID: 15)<br>- Sprint 2 (ID: 20) |
| **測試類型** | 邊界測試（重複資料處理） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-FILTER-005

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-FILTER-005 |
| **測試目標** | 驗證選擇「All」顯示所有 Issue |
| **相關 User Story** | US3: 作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint |
| **相關 AC 場景** | AC5: Given 使用者選擇「All」選項，When 系統更新資料，Then 應顯示所有 Issue 的統計和分布 |
| **測試前置條件** | 1. Google Sheets rawData 工作表包含不同 Sprint 的 Issue<br>2. 測試資料已知總 Issue 數量 |
| **測試步驟** | 1. 準備測試資料：rawData 包含<br>   - 10 筆屬於 Sprint A<br>   - 8 筆屬於 Sprint B<br>   - 5 筆沒有 Sprint（空值）<br>   - 總計 23 筆 Issue<br>2. 開啟 Jira Dashboard 首頁<br>3. 確認 Sprint 篩選器預設為「All」<br>4. 檢查統計卡片和長條圖 |
| **預期結果** | 1. Total Issue Count 顯示：23<br>2. 長條圖顯示所有 23 筆 Issue 的狀態分布<br>3. 不受 Sprint 欄位值影響，包含所有記錄 |
| **測試資料** | 總計 23 筆 Issue（10 筆 Sprint A + 8 筆 Sprint B + 5 筆無 Sprint） |
| **測試類型** | 功能測試（篩選邏輯） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-FILTER-006

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-FILTER-006 |
| **測試目標** | 驗證選擇特定 Sprint 的篩選功能 |
| **相關 User Story** | US3: 作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint |
| **相關 AC 場景** | AC6: Given 使用者選擇特定 Sprint 名稱，When 系統更新資料，Then 應只顯示該 Sprint 的 Issue 統計和分布 |
| **測試前置條件** | 1. Google Sheets rawData 工作表包含不同 Sprint 的 Issue<br>2. Sprint 欄位值與 GetJiraSprintValues 工作表的 Sprint Name 一致 |
| **測試步驟** | 1. 準備測試資料：rawData 包含<br>   - 12 筆屬於「Development Sprint」<br>   - 其中 5 筆 Status 為 Done，Story Points 總和 15<br>   - 8 筆屬於其他 Sprint<br>2. 開啟 Jira Dashboard 首頁<br>3. 點擊 Sprint 篩選器，選擇「Development Sprint」<br>4. 等待資料更新<br>5. 檢查統計卡片和長條圖 |
| **預期結果** | 1. Total Issue Count 顯示：12（僅 Development Sprint 的 Issue）<br>2. Total Done Item Count 顯示：5<br>3. Done Story Points 顯示：15<br>4. 長條圖只顯示「Development Sprint」的 Issue 狀態分布<br>5. 其他 Sprint 的 Issue 不計入統計 |
| **測試資料** | **rawData 測試資料**：<br>- 12 筆 Sprint="Development Sprint"（5 筆 Done, Story Points=15）<br>- 8 筆 Sprint="Testing Sprint" |
| **測試類型** | 功能測試（篩選邏輯） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-FILTER-007

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-FILTER-007 |
| **測試目標** | 驗證選擇「No Sprints」的篩選功能 |
| **相關 User Story** | US3: 作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint |
| **相關 AC 場景** | AC7: Given 使用者選擇「No Sprints」選項，When 系統更新資料，Then 應只顯示沒有指定 Sprint 的 Issue |
| **測試前置條件** | 1. Google Sheets rawData 工作表包含 Sprint 欄位為空值的 Issue |
| **測試步驟** | 1. 準備測試資料：rawData 包含<br>   - 6 筆 Sprint 欄位為空（無 Sprint）<br>   - 其中 2 筆 Status 為 Done<br>   - 15 筆有 Sprint 值的 Issue<br>2. 開啟 Jira Dashboard 首頁<br>3. 點擊 Sprint 篩選器，選擇「No Sprints」<br>4. 等待資料更新<br>5. 檢查統計卡片和長條圖 |
| **預期結果** | 1. Total Issue Count 顯示：6（僅無 Sprint 的 Issue）<br>2. Total Done Item Count 顯示：2<br>3. 長條圖只顯示無 Sprint Issue 的狀態分布<br>4. 有 Sprint 值的 Issue 不計入統計 |
| **測試資料** | **rawData 測試資料**：<br>- 6 筆 Sprint=空值（2 筆 Done）<br>- 15 筆有 Sprint 值 |
| **測試類型** | 功能測試（篩選邏輯） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-FILTER-008

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-FILTER-008 |
| **測試目標** | 驗證切換 Sprint 時統計和圖表即時更新 |
| **相關 User Story** | US3: 作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint |
| **相關 AC 場景** | AC8: Given 使用者切換不同 Sprint，When 篩選器值改變，Then 統計卡片和狀態分布圖應即時同步更新 |
| **測試前置條件** | 1. Google Sheets rawData 工作表包含至少兩個不同 Sprint 的 Issue<br>2. 每個 Sprint 的統計數值不同 |
| **測試步驟** | 1. 準備測試資料：<br>   - Sprint A: 10 筆 Issue, 3 筆 Done<br>   - Sprint B: 15 筆 Issue, 8 筆 Done<br>2. 開啟 Jira Dashboard 首頁（預設 All）<br>3. 點擊 Sprint 篩選器，選擇「Sprint A」<br>4. 記錄統計卡片數值（Total Issue Count, Total Done Item Count）<br>5. 點擊 Sprint 篩選器，切換至「Sprint B」<br>6. 檢查統計卡片和長條圖是否更新 |
| **預期結果** | 1. 選擇 Sprint A 後：<br>   - Total Issue Count 顯示：10<br>   - Total Done Item Count 顯示：3<br>   - 長條圖更新為 Sprint A 的分布<br>2. 切換至 Sprint B 後（2 秒內）：<br>   - Total Issue Count 顯示：15<br>   - Total Done Item Count 顯示：8<br>   - 長條圖即時更新為 Sprint B 的分布<br>3. 無需重新整理頁面，資料即時同步 |
| **測試資料** | **rawData 測試資料**：<br>- Sprint A: 10 筆（3 筆 Done）<br>- Sprint B: 15 筆（8 筆 Done） |
| **測試類型** | 功能測試（即時更新） |
| **自動化程度** | 全自動（E2E 測試） |

---

## Edge Cases（邊界與異常情況）

### TC-EDGE-001

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-EDGE-001 |
| **測試目標** | 驗證 Google Sheets 連結失效時的錯誤處理 |
| **相關 User Story** | N/A（系統穩定性需求） |
| **相關 AC 場景** | Edge Case: 當 Google Sheets 公開連結失效或無法存取時，系統應顯示錯誤提示而非崩潰 |
| **測試前置條件** | 1. 能夠模擬 API 失效或網路錯誤<br>2. 或使用無效的 Google Sheets URL |
| **測試步驟** | 1. 修改應用程式設定，使用無效的 Google Sheets URL<br>2. 或使用網路攔截工具（如 Mock Service Worker）模擬 API 失敗<br>3. 開啟 Jira Dashboard 首頁<br>4. 檢查頁面反應 |
| **預期結果** | 1. 頁面不崩潰或顯示白屏<br>2. 在 3 秒內顯示友善的錯誤訊息<br>3. 錯誤訊息清楚說明「無法連接資料來源」或類似內容<br>4. 提供使用者後續操作建議（例如「請稍後再試」或「請聯絡管理員」） |
| **測試資料** | 無效 Google Sheets URL 或模擬 API 失敗 |
| **測試類型** | 異常測試（錯誤處理） |
| **自動化程度** | 半自動（需手動設定或 Mock API） |

---

### TC-EDGE-002

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-EDGE-002 |
| **測試目標** | 驗證 Status 欄位包含無效值時的處理 |
| **相關 User Story** | N/A（資料品質處理） |
| **相關 AC 場景** | Edge Case: 當 rawData 工作表的 Status 欄位包含 9 個預定義狀態以外的值時，系統必須在長條圖中忽略這些記錄，但在「Total Issue Count」計算中仍包含這些記錄 |
| **測試前置條件** | 1. Google Sheets rawData 工作表包含無效 Status 值的記錄 |
| **測試步驟** | 1. 準備測試資料：rawData 包含<br>   - 20 筆有效 Status（如 Done, In Progress 等）<br>   - 3 筆無效 Status（如 "Unknown", "Testing", "Archive"）<br>2. 開啟 Jira Dashboard 首頁<br>3. 檢查統計卡片的 Total Issue Count<br>4. 檢查長條圖的顯示內容 |
| **預期結果** | 1. Total Issue Count 顯示：23（包含 3 筆無效 Status 的記錄）<br>2. 長條圖只顯示 9 個預定義狀態的分布<br>3. 長條圖的總 Issue 數為 20（忽略 3 筆無效 Status）<br>4. 無效 Status 的記錄不出現在長條圖中<br>5. 系統不顯示錯誤訊息，靜默處理無效資料 |
| **測試資料** | **rawData 測試資料**：<br>- 20 筆有效 Status<br>- 3 筆無效 Status（"Unknown", "Testing", "Archive"） |
| **測試類型** | 邊界測試（無效資料處理） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-EDGE-003

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-EDGE-003 |
| **測試目標** | 驗證 Story Points 欄位包含非數值資料時的處理 |
| **相關 User Story** | N/A（資料品質處理） |
| **相關 AC 場景** | Edge Case: 當 Story Points 欄位包含非數值資料時，系統必須將其視為 0，Issue 記錄仍納入所有統計計算中 |
| **測試前置條件** | 1. Google Sheets rawData 工作表包含非數值 Story Points 的記錄 |
| **測試步驟** | 1. 準備測試資料：rawData 包含<br>   - 10 筆正常數值 Story Points（總和 30）<br>   - 3 筆非數值 Story Points（如 "TBD", "N/A", "#REF!"）<br>   - 2 筆空值 Story Points<br>2. 開啟 Jira Dashboard 首頁<br>3. 檢查統計卡片的數值 |
| **預期結果** | 1. Total Issue Count 顯示：15（包含所有記錄）<br>2. Total Story Points 顯示：30（非數值和空值視為 0）<br>3. 系統不顯示錯誤訊息，靜默處理非數值資料<br>4. 非數值 Story Points 的 Issue 仍計入 Total Issue Count |
| **測試資料** | **rawData 測試資料**：<br>- 10 筆正常 Story Points（總和 30）<br>- 3 筆非數值（"TBD", "N/A", "#REF!"）<br>- 2 筆空值 |
| **測試類型** | 邊界測試（非數值資料處理） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-EDGE-004

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-EDGE-004 |
| **測試目標** | 驗證 GetJiraSprintValues 工作表無資料時的處理 |
| **相關 User Story** | US3: 作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint |
| **相關 AC 場景** | FR-027: 當 GetJiraSprintValues 工作表無資料時，Sprint 篩選器必須只顯示「All」和「No Sprints」選項 |
| **測試前置條件** | 1. Google Sheets GetJiraSprintValues 工作表為空（僅保留標題列） |
| **測試步驟** | 1. 清空 GetJiraSprintValues 工作表所有資料列<br>2. 開啟 Jira Dashboard 首頁<br>3. 點擊 Sprint 篩選器下拉選單<br>4. 檢查可選選項 |
| **預期結果** | 1. Sprint 篩選器正常顯示（不崩潰）<br>2. 下拉選單只包含兩個選項：<br>   - All<br>   - No Sprints<br>3. 無其他 Sprint 選項<br>4. 系統不顯示錯誤訊息 |
| **測試資料** | 空的 GetJiraSprintValues 工作表 |
| **測試類型** | 異常測試（空狀態處理） |
| **自動化程度** | 全自動（E2E 測試） |

---

### TC-EDGE-005

| 欄位 | 內容 |
|------|------|
| **測試案例編號** | TC-EDGE-005 |
| **測試目標** | 驗證大量使用者同時存取時的效能（快取機制） |
| **相關 User Story** | N/A（效能需求） |
| **相關 AC 場景** | Edge Case: 當同時有大量使用者存取儀表板時，5 分鐘快取機制是否足以應對（MVP v1.0 假設同時使用者數不超過 100 人） |
| **測試前置條件** | 1. 能夠模擬多個使用者同時存取（負載測試工具如 JMeter, k6）<br>2. 應用程式已部署至測試環境 |
| **測試步驟** | 1. 使用負載測試工具模擬 100 個使用者同時開啟 Jira Dashboard 首頁<br>2. 記錄所有使用者的頁面載入時間<br>3. 檢查伺服器回應狀態碼<br>4. 驗證快取是否生效（檢查實際 API 呼叫次數） |
| **預期結果** | 1. 所有 100 個使用者的頁面都成功載入（HTTP 200）<br>2. 90% 使用者的載入時間不超過 5 秒<br>3. 快取機制生效，減少對 Google Sheets API 的重複呼叫<br>4. 伺服器不崩潰或回應 5xx 錯誤 |
| **測試資料** | 負載測試：100 個並發使用者 |
| **測試類型** | 效能測試（負載測試） |
| **自動化程度** | 全自動（負載測試工具） |

---

## 測試案例統計

- **總測試案例數量**: 20
- **User Story 1（即時專案健康度監控）**: 4 個測試案例
- **User Story 2（Issue 狀態分布視覺化）**: 5 個測試案例
- **User Story 3（Sprint 篩選功能）**: 8 個測試案例
- **Edge Cases（邊界與異常情況）**: 5 個測試案例

### 按測試類型分類

- **功能測試**: 13
- **異常測試**: 4
- **邊界測試**: 3
- **效能測試**: 1

### 按自動化程度分類

- **全自動（E2E/API 測試）**: 16
- **半自動（需手動設定或等待）**: 4

---

## 測試執行建議

### 測試優先級

**P0（必須通過，阻礙發布）**:
- TC-DASHBOARD-001, TC-DASHBOARD-002（核心統計功能）
- TC-CHART-001, TC-CHART-002（長條圖核心功能）
- TC-FILTER-001, TC-FILTER-005, TC-FILTER-006（Sprint 篩選核心功能）
- TC-EDGE-001（錯誤處理）

**P1（重要，影響使用者體驗）**:
- TC-DASHBOARD-003（空狀態處理）
- TC-CHART-003, TC-CHART-005（互動與空狀態）
- TC-FILTER-002, TC-FILTER-008（篩選器完整性與即時更新）
- TC-EDGE-002, TC-EDGE-003（資料品質處理）

**P2（次要，可接受風險）**:
- TC-DASHBOARD-004（快取機制）
- TC-CHART-004（總數顯示）
- TC-FILTER-003, TC-FILTER-004, TC-FILTER-007（進階篩選邏輯）
- TC-EDGE-004, TC-EDGE-005（邊界情況與效能）

### 自動化測試工具建議

- **E2E 測試**: Playwright 或 Cypress（適合 TC-DASHBOARD-*, TC-CHART-*, TC-FILTER-* 系列）
- **API 測試**: Postman 或 REST Assured（適合驗證 Google Sheets 資料讀取邏輯）
- **負載測試**: k6 或 Apache JMeter（適合 TC-EDGE-005）
- **Mock API**: Mock Service Worker (MSW)（適合模擬 Google Sheets API 失敗情境）

### CI/CD 整合建議

- **每次 Commit**: 執行所有 P0 測試案例（快速驗證核心功能）
- **每次 Pull Request**: 執行所有 P0 + P1 測試案例
- **發布前驗證**: 執行所有測試案例（P0 + P1 + P2）
- **定期回歸測試**: 每週執行完整測試套件，包含效能測試
