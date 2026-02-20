# Feature Specification: Jira Dashboard MVP v1

**Feature Branch**: `001-jira-dashboard-mvp`
**Created**: 2025-10-29
**Status**: Draft
**Input**: User description: "需求請參考 docs/reference/PRD.md - Jira Dashboard MVP v1 產品規格"

## Clarifications

### Session 2025-10-29

- Q: 當 rawData 工作表的 Status 欄位包含 9 個預定義狀態以外的值時，應如何處理？ → A: 在長條圖中忽略無效狀態的記錄，但在「Total Issue Count」計算中仍包含這些記錄
- Q: 當 Story Points 欄位包含非數值資料時，系統應該如何處理這些記錄？ → A: 將非數值的 Story Points 視為 0，Issue 記錄仍納入所有統計計算中
- Q: 當 GetJiraSprintValues 工作表的 Sprint Name 欄位包含重複值時，篩選器應如何顯示？ → A: 在 Sprint Name 後加上 Sprint ID 來區分（例如「Sprint 1 (11)」、「Sprint 1 (15)」）
- Q: 當使用者網路連線緩慢導致資料載入時間過長時，系統應該提供什麼樣的使用者體驗？ → A: 顯示載入指示器（Loading Spinner），不設定超時限制，讓使用者等待直到載入完成
- Q: 當 rawData 工作表的欄位順序或名稱改變時，系統應該如何反應？ → A: MVP v1.0 版本假設 schema 保持穩定，不處理 schema 變更情況

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 即時專案健康度監控 (Priority: P1)

作為專案經理，我希望能在儀表板上即時查看專案的關鍵統計指標（總 Issue 數、總故事點數、已完成 Issue 數、已完成故事點數），以便快速了解專案整體健康度和進度狀況。

**Why this priority**: 這是 MVP 的核心價值主張，提供專案經理最需要的一目了然的專案概覽。沒有這個功能，儀表板就失去了存在意義。

**Independent Test**: 可以透過開啟儀表板並驗證四個統計卡片是否正確顯示數據來獨立測試。這個功能不依賴其他功能即可提供價值。

**Acceptance Scenarios**:

1. **Given** 使用者開啟 Jira Dashboard 首頁，**When** 頁面載入完成，**Then** 應顯示四個統計卡片：Total Issue Count、Total Story Points、Total Done Item Count、Done Story Points
2. **Given** Google Sheets rawData 工作表包含 Issue 資料，**When** 使用者查看統計卡片，**Then** 每個卡片應顯示正確的統計數值（支援小數點的故事點數）
3. **Given** Google Sheets rawData 工作表無資料或無法連接，**When** 使用者查看統計卡片，**Then** 應顯示 0 或適當的空狀態提示
4. **Given** 統計資料已顯示，**When** Google Sheets 資料更新且快取過期（5分鐘），**Then** 重新整理頁面後應顯示更新後的數值
5. **Given** 使用者開啟儀表板但網路連線緩慢，**When** 資料正在載入中，**Then** 應顯示載入指示器直到資料載入完成

---

### User Story 2 - Issue 狀態分布視覺化 (Priority: P1)

作為團隊領導，我希望能透過長條圖查看 Issue 在各個狀態的分布情況，以便識別工作流程瓶頸和團隊的工作重心。

**Why this priority**: 狀態分布圖提供了專案進度的視覺化呈現，是專案健康度監控的重要補充。與統計卡片同為 P1，因為兩者共同構成 MVP 的完整價值。

**Independent Test**: 可以透過開啟儀表板並驗證長條圖是否按照固定順序顯示 9 個狀態的分布，以及滑鼠懸停時是否顯示詳細資訊來獨立測試。

**Acceptance Scenarios**:

1. **Given** 使用者開啟 Jira Dashboard，**When** 頁面載入完成，**Then** 應顯示 Issue 狀態分布長條圖
2. **Given** 長條圖已顯示，**When** 使用者查看圖表，**Then** 應按照固定順序顯示 9 個狀態：Backlog → Evaluated → To Do → In Progress → Waiting → Ready to Verify → Done → Invalid → Routine
3. **Given** 使用者查看長條圖，**When** 滑鼠懸停在任一長條上，**Then** 應顯示該狀態的詳細數值和百分比
4. **Given** 長條圖已顯示，**When** 使用者查看圖表底部，**Then** 應顯示總 Issue 數量統計
5. **Given** Google Sheets rawData 工作表無資料，**When** 使用者查看長條圖區域，**Then** 應顯示友善的空狀態提示訊息

---

### User Story 3 - Sprint 篩選功能 (Priority: P2)

作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint，以便專注查看當前或特定 Sprint 的資料。

**Why this priority**: Sprint 篩選是提升儀表板實用性的重要功能，但不是 MVP 的絕對必要條件。使用者仍可以透過查看所有資料來獲取價值。

**Independent Test**: 可以透過選擇不同的 Sprint 選項並驗證統計卡片和長條圖是否相應更新來獨立測試。

**Acceptance Scenarios**:

1. **Given** 使用者開啟 Jira Dashboard，**When** 頁面載入完成，**Then** 頂部應顯示 Sprint 篩選器下拉選單
2. **Given** Sprint 篩選器已顯示，**When** 使用者點擊下拉選單，**Then** 應顯示「All」、所有有效的 Sprint 名稱、以及「No Sprints」選項
3. **Given** Sprint 篩選器選項來自 Google Sheets GetJiraSprintValues 工作表，**When** 系統載入 Sprint 選項，**Then** 應從 Column C（Sprint Name）和 Column D（Sprint ID）讀取資料
4. **Given** GetJiraSprintValues 工作表包含重複的 Sprint Name，**When** 系統生成篩選器選項，**Then** 應在重複的 Sprint Name 後加上 Sprint ID 以區分（格式：「Sprint Name (Sprint ID)」）
5. **Given** 使用者選擇「All」選項，**When** 系統更新資料，**Then** 應顯示所有 Issue 的統計和分布
6. **Given** 使用者選擇特定 Sprint 名稱，**When** 系統更新資料，**Then** 應只顯示該 Sprint 的 Issue 統計和分布（透過 rawData 工作表的 Sprint 欄位篩選）
7. **Given** 使用者選擇「No Sprints」選項，**When** 系統更新資料，**Then** 應只顯示沒有指定 Sprint 的 Issue
8. **Given** 使用者切換不同 Sprint，**When** 篩選器值改變，**Then** 統計卡片和狀態分布圖應即時同步更新

---

### Edge Cases

- 當 Google Sheets 公開連結失效或無法存取時，系統應顯示錯誤提示而非崩潰
- 當 rawData 工作表的 Status 欄位包含 9 個預定義狀態以外的值時，系統必須在長條圖中忽略這些記錄，但在「Total Issue Count」計算中仍包含這些記錄
- 當 Story Points 欄位包含非數值資料時，系統必須將其視為 0，Issue 記錄仍納入所有統計計算中
- 當 GetJiraSprintValues 工作表的 Sprint Name 欄位包含重複值時，系統必須在 Sprint Name 後加上 Sprint ID 來區分（例如「Sprint 1 (11)」、「Sprint 1 (15)」）
- 當使用者的網路連線緩慢時，系統必須顯示載入指示器（Loading Spinner），持續顯示直到資料載入完成
- 當同時有大量使用者存取儀表板時，5 分鐘快取機制是否足以應對？（MVP v1.0 假設同時使用者數不超過 100 人）

## Requirements *(mandatory)*

### Functional Requirements

#### 核心顯示功能

- **FR-001**: 系統必須在首頁顯示四個統計卡片：Total Issue Count、Total Story Points、Total Done Item Count、Done Story Points
- **FR-002**: 系統必須從 Google Sheets rawData 工作表讀取 Issue 資料（A:W 欄位範圍，共 23 欄）
- **FR-003**: 系統必須顯示 Issue 狀態分布長條圖，包含 9 個固定狀態：Backlog、Evaluated、To Do、In Progress、Waiting、Ready to Verify、Done、Invalid、Routine
- **FR-004**: 狀態分布圖必須按照固定順序顯示（Backlog → Evaluated → To Do → In Progress → Waiting → Ready to Verify → Done → Invalid → Routine）
- **FR-005**: 系統必須支援滑鼠懸停在長條圖上時顯示詳細數值和百分比

#### 資料處理與計算

- **FR-006**: 系統必須從 rawData 工作表的欄位 1（Key）、欄位 6（Status）、欄位 16（Story Points）讀取資料
- **FR-007**: 系統必須使用 `row[index]` 模式存取 rawData 欄位（索引 0-22），而非依賴欄位名稱
- **FR-008**: Total Issue Count 必須計算 rawData 工作表中的總列數（包含所有記錄，即使 Status 為無效值）
- **FR-009**: Total Story Points 必須計算所有 Issue 的 Story Points 總和（欄位 16），支援小數點
- **FR-010**: Total Done Item Count 必須計算 Status 欄位（欄位 6）為「Done」的 Issue 數量
- **FR-011**: Done Story Points 必須計算 Status 為「Done」的 Issue 的 Story Points 總和
- **FR-012**: 狀態分布統計必須計算每個狀態的 Issue 數量和佔比百分比
- **FR-031**: 狀態分布長條圖必須只顯示 9 個預定義狀態，忽略 Status 欄位值不在預定義清單內的記錄
- **FR-032**: 當 Story Points 欄位包含非數值資料（文字、特殊符號等）時，系統必須將其視為 0 進行計算

#### Sprint 篩選功能

- **FR-013**: 系統必須在頂部顯示 Sprint 篩選器下拉選單
- **FR-014**: 系統必須從 Google Sheets GetJiraSprintValues 工作表讀取 Sprint 選項（A:I 欄位範圍）
- **FR-015**: Sprint 選項必須從 GetJiraSprintValues 工作表的 Column C（Sprint Name）和 Column D（Sprint ID）讀取
- **FR-016**: Sprint 篩選器必須提供「All」、所有有效 Sprint 名稱、以及「No Sprints」選項
- **FR-017**: 當選擇特定 Sprint 時，系統必須透過 rawData 工作表的欄位 7（Sprint）進行篩選
- **FR-018**: 當選擇「No Sprints」時，系統必須只顯示 Sprint 欄位為空的 Issue
- **FR-019**: 當 Sprint 篩選器值改變時，統計卡片和狀態分布圖必須即時同步更新
- **FR-033**: 當 GetJiraSprintValues 工作表包含重複的 Sprint Name 時，系統必須在下拉選單中以「Sprint Name (Sprint ID)」格式顯示，使用 Sprint ID 區分重複項目

#### 資料整合與快取

- **FR-020**: 系統必須透過 Google Sheets 公開 CSV API 讀取資料，無需 API 金鑰
- **FR-021**: 系統必須實作 5 分鐘快取機制，平衡效能與即時性
- **FR-022**: 系統必須處理 Story Points 欄位的空值和非數值資料（視為 0）
- **FR-023**: 系統必須處理 Sprint 欄位的空值（可透過「No Sprints」篩選）

#### 錯誤處理與空狀態

- **FR-024**: 當 Google Sheets 無法連接時，系統必須顯示友善的錯誤訊息
- **FR-025**: 當 rawData 工作表無資料時，統計卡片必須顯示 0
- **FR-026**: 當 rawData 工作表無資料時，狀態分布圖必須顯示空狀態提示
- **FR-027**: 當 GetJiraSprintValues 工作表無資料時，Sprint 篩選器必須只顯示「All」和「No Sprints」選項
- **FR-034**: 當資料正在載入時（包含網路連線緩慢情況），系統必須顯示載入指示器（Loading Spinner），持續顯示直到資料載入完成或發生錯誤

#### 使用者介面

- **FR-028**: 系統必須使用藍色主題（#3b82f6）作為主要視覺風格
- **FR-029**: 統計卡片必須包含適當的圖示：文件圖標（Total Issue Count）、目標圖標（Total Story Points）、勾選圖標（Total Done Item Count）、時鐘圖標（Done Story Points）
- **FR-030**: 應用程式標題必須顯示「Jira Dashboard」

### Key Entities

- **Issue**: 代表 Jira 系統中的工作項目，包含屬性：Key（唯一識別碼）、Issue Type（類型）、Status（狀態）、Sprint（所屬 Sprint）、Story Points（故事點數）、以及其他 18 個欄位。每個 Issue 在 rawData 工作表中佔一列，共 23 個欄位（A:W）。

- **Sprint**: 代表敏捷開發的迭代週期，包含屬性：Board ID（看板 ID）、Board Name（看板名稱）、Sprint Name（Sprint 名稱）、Sprint ID（Sprint ID）、state（狀態：future/active/closed）、startDate（開始日期）、endDate（結束日期）、completeDate（完成日期）、goal（目標）。每個 Sprint 在 GetJiraSprintValues 工作表中佔一列，共 9 個欄位（A:I）。Sprint Name 可能重複，需使用 Sprint ID 作為唯一識別。

- **Status**: 代表 Issue 的工作流程狀態，包含 9 個固定值：Backlog（待辦清單）、Evaluated（已評估）、To Do（待處理）、In Progress（進行中）、Waiting（等待中）、Ready to Verify（待驗證）、Done（已完成）、Invalid（無效）、Routine（例行作業）。狀態順序固定，用於長條圖顯示。

- **統計卡片（Metric Card）**: 代表儀表板上的統計資訊顯示元件，包含屬性：標題（如 Total Issue Count）、數值（統計結果）、圖示（視覺化圖標）、說明文字。共四個卡片提供專案健康度的關鍵指標。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 使用者開啟儀表板後，四個統計卡片必須在 3 秒內完成載入並顯示正確數值
- **SC-002**: 使用者切換 Sprint 篩選器後，統計卡片和長條圖必須在 2 秒內更新完成
- **SC-003**: 狀態分布長條圖必須正確顯示 9 個固定狀態，且順序符合工作流程（Backlog → Done）
- **SC-004**: 滑鼠懸停在長條圖上時，必須在 0.5 秒內顯示該狀態的詳細數值和百分比
- **SC-005**: 當 Google Sheets 資料更新後，使用者重新整理頁面（快取過期後）必須看到最新資料
- **SC-006**: 系統必須支援至少 50 個使用者同時存取，且回應時間不超過 5 秒
- **SC-007**: 當 Google Sheets 無法連接時，使用者必須在 3 秒內看到明確的錯誤訊息，而非頁面崩潰或無限載入
- **SC-008**: 90% 的使用者能在首次使用時，無需說明文件即可理解統計卡片的含義和 Sprint 篩選器的用途
- **SC-009**: Sprint 篩選器必須正確載入所有來自 GetJiraSprintValues 工作表的 Sprint 選項，包含「All」和「No Sprints」，重複的 Sprint Name 必須以「Sprint Name (Sprint ID)」格式顯示
- **SC-010**: 統計數值的計算準確率必須達到 100%（與 Google Sheets 原始資料對比，非數值 Story Points 視為 0）
- **SC-011**: 當資料載入時，使用者必須看到載入指示器，明確知道系統正在處理請求

## Assumptions

1. **資料來源穩定性**: 假設 Google Sheets 的公開連結在產品使用期間保持有效且可存取
2. **資料格式一致性（Schema 穩定性）**: 假設 rawData 工作表維持 23 欄固定格式（A:W），欄位順序和名稱不會改變。MVP v1.0 版本不處理 schema 變更情況
3. **Status 值標準化**: 假設 rawData 工作表的 Status 欄位主要包含 9 個預定義狀態值（但系統必須能處理少數無效值）
4. **快取策略充足性**: 假設 5 分鐘快取週期能滿足大多數使用者對即時性的需求
5. **使用者規模**: 假設同時線上使用者數不超過 100 人（基於 MVP 定位）
6. **瀏覽器相容性**: 假設使用者使用現代瀏覽器（Chrome、Firefox、Safari、Edge 最新版本）
7. **Story Points 資料品質**: 假設 Story Points 欄位主要包含數值或空值，極少出現非數值資料（但系統必須能處理）
8. **Sprint Name 唯一性**: 假設 GetJiraSprintValues 工作表中的 Sprint Name 可能重複，但 Sprint ID 是唯一的
9. **網路環境**: 假設使用者具備穩定的網路連線（至少 1 Mbps 下載速度），但系統必須能處理網路緩慢的情況
10. **視覺設計簡化**: 假設 MVP 階段採用簡化的 UI 設計，無需複雜的動畫或互動效果
