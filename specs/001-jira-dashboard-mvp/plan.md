# Implementation Plan: Jira Dashboard MVP v1.0

**Branch**: `001-jira-dashboard-mvp` | **Date**: 2025-10-29 | **Spec**: `/specs/001-jira-dashboard-mvp/spec.md`
**Input**: Feature specification from `/specs/001-jira-dashboard-mvp/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

構建一個功能完整的 Jira Dashboard MVP v1.0 應用，整合 Google Sheets 作為真實資料來源，透過 5 分鐘快取機制實現效能優化。系統核心功能包括：4 個統計卡片（Total Issue Count、Total Story Points、Total Done Item Count、Done Story Points）、1 個 Issue 狀態分布長條圖（支援 9 個固定狀態）、以及 1 個 Sprint 篩選器。採用現代化技術堆疊（Next.js 15、React 19、Python/FastAPI、TypeScript）實現前後端分離架構，支援 Docker 容器化部署，嚴格遵守 Google Sheets 的 23 欄位 rawData 資料表結構限制。

## Technical Context

**前端技術棧**:
- **Language/Version**: TypeScript 5.x + Next.js 15.2.4 (App Router)
- **Primary Dependencies**: React 19.0.0、shadcn/ui (Radix UI)、Tailwind CSS 3.4.x、Recharts 2.x、React Hook Form 7.x、Zod 3.x
- **Testing**:
  - Unit/Component: Jest 29.x + React Testing Library 14.x + @testing-library/jest-dom 6.x
  - E2E: Playwright 1.40+ (覆蓋 TC-DASHBOARD-*, TC-CHART-*, TC-FILTER-* 系列)
  - API Mocking: Mock Service Worker (MSW) 2.0+ (模擬 Google Sheets API 失敗情境)
- **Target Platform**: Web Browser (Chrome、Firefox、Safari、Edge 最新版本)
- **Project Type**: Web Application (Monorepo - frontend + backend)

**後端技術棧**:
- **Language/Version**: Python 3.11
- **Primary Dependencies**: FastAPI 0.104.1、Uvicorn 0.24.0、Pandas 2.1.3
- **Testing**:
  - Unit/Integration: pytest 7.4.3 + pytest-asyncio 0.21.1 + httpx 0.25.2
  - Load Testing: k6 0.48+ 或 Locust 2.15+ (驗證 TC-EDGE-005: 100 concurrent users)
  - Contract Testing: Pydantic model validation + pytest
- **Storage**: Google Sheets (CSV API) + In-memory Cache (5 min TTL)
- **Target Platform**: Linux Server (Docker)

**Infrastructure**:
- **Deployment**: Docker + Docker Compose
- **Monorepo**: npm workspaces
- **Automation**: Makefile

**Data Architecture**:
- **Data Source**: Google Sheets (Public CSV Export - No API key required)
- **Primary Table**: rawData (23 columns A:W) - Fixed schema, strict field order
- **Secondary Table**: GetJiraSprintValues (9 columns A:I) - Sprint management data
- **Cache Strategy**: 5-minute TTL in-memory cache
- **Schema Stability**: Assume fixed schema; MVP v1.0 does not handle schema changes

**Performance Goals**:
- 4 metric cards load within 3 seconds
- Sprint filter update within 2 seconds
- Tooltip display within 0.5 seconds
- Support at least 50 concurrent users (goal: 100)
- API response time < 5 seconds p95

**Constraints**:
- Google Sheets public link must remain valid and accessible
- Raw data limited to 23 fixed columns (cannot add/remove/reorder)
- No user authentication in MVP
- Read-only access to Google Sheets (no write capability)
- Slow network handling: display loading spinner without timeout

**Scale/Scope**:
- Estimated data: Up to 10,000 Issues per Jira instance
- 4 Key Metric Cards + 1 Status Distribution Bar Chart + 1 Sprint Filter
- 9 Fixed Status values in workflow order
- ~50 concurrent users expected in MVP phase

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on `.specify/memory/constitution.md` v1.0.0 principles:

### ✅ Gate 1: Specification Completeness
- [x] User Stories follow format: `作為 [角色]，我希望 [功能]，以便 [價值]`
- [x] Each User Story has clear value proposition (3 stories: P1 metrics monitoring, P1 status visualization, P2 sprint filtering)
- [x] Acceptance Criteria use Gherkin format for all 23 scenarios (Given-When-Then)
- [x] Edge cases documented (invalid status values, non-numeric story points, duplicate sprint names, slow network, large concurrent users)

### ✅ Gate 2: Template Compliance
- [x] All placeholders replaced with concrete content or marked where uncertain
- [x] Documentation structure matches spec-driven principles
- [x] Traditional Chinese used for documentation, English for technical identifiers
- [x] All references to tech-overview.md and table-schema.md provided

### ⚠️ Gate 3: Testing Coverage (to be completed in Phase 2)
- [ ] Each AC scenario will map to at least one test case (23 AC scenarios → 23+ test cases)
- [ ] Test cases will include all mandatory fields (Test ID, Objective, Pre-conditions, Steps, Expected Results)
- [ ] Test-first approach will be documented (tests before implementation in Phase 2)
- [ ] Automation feasibility will be assessed per test

### ✅ Gate 4: Consistency Check
- [x] Terminology consistent: "Issue", "Sprint", "Status", "Metric Card" align with spec
- [x] Data schema constraints documented per constitution (rawData 23-column strict structure)
- [x] Communication style is direct and objective
- [x] Vibe Coding design constraints explicitly referenced

### ✅ Gate 5: Pedagogical Value
- [x] Common mistakes documented: invalid status handling, non-numeric story points, slow networks
- [x] AI interaction prompts will be included in Phase 1 design
- [x] Examples use realistic Jira Dashboard context
- [x] Rationale provided for technical choices (caching strategy, fixed schema, slow network handling)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

已存在的 Monorepo 結構（根據專案現狀）：

```text
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── (dashboard)/
│   │       ├── layout.tsx
│   │       └── page.tsx
│   ├── components/
│   │   ├── MetricCard.tsx
│   │   ├── StatusDistributionChart.tsx
│   │   ├── SprintFilter.tsx
│   │   └── LoadingSpinner.tsx
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── dashboard.ts
│   └── hooks/
│       └── useDashboardData.ts
├── tests/
│   ├── unit/
│   │   ├── MetricCard.test.tsx
│   │   ├── StatusDistributionChart.test.tsx
│   │   └── SprintFilter.test.tsx
│   ├── integration/
│   │   └── DashboardPage.test.tsx
│   ├── e2e/
│   │   ├── dashboard.spec.ts         # TC-DASHBOARD-001~004
│   │   ├── status-chart.spec.ts      # TC-CHART-001~005
│   │   ├── sprint-filter.spec.ts     # TC-FILTER-001~008
│   │   └── edge-cases.spec.ts        # TC-EDGE-001~004
│   ├── contract/
│   │   └── api-contracts.test.ts
│   └── mocks/
│       └── google-sheets-api.ts      # MSW handlers for API mocking
├── playwright.config.ts
├── jest.config.js
├── tsconfig.json
└── package.json

backend/
├── src/
│   ├── main.py
│   ├── models/
│   │   ├── issue.py
│   │   ├── sprint.py
│   │   └── metric.py
│   ├── services/
│   │   ├── google_sheets_service.py
│   │   ├── cache_service.py
│   │   └── data_processor.py
│   ├── api/
│   │   ├── routes.py
│   │   ├── dependencies.py
│   │   └── schemas.py
│   └── config.py
├── tests/
│   ├── unit/
│   │   ├── test_data_processor.py
│   │   ├── test_google_sheets_service.py
│   │   └── test_cache_service.py
│   ├── integration/
│   │   └── test_api_endpoints.py
│   ├── contract/
│   │   └── test_api_contracts.py
│   ├── load/
│   │   ├── k6-script.js              # k6 負載測試腳本 (TC-EDGE-005)
│   │   └── locustfile.py             # Locust 負載測試 (100 concurrent users)
│   └── fixtures/
│       ├── test_data_tc_dashboard_002.csv  # TC-DASHBOARD-002 測試資料
│       ├── test_data_edge_002.csv          # TC-EDGE-002 無效 Status
│       └── test_data_edge_003.csv          # TC-EDGE-003 非數值 Story Points
├── requirements.txt
├── requirements-dev.txt              # 包含測試工具: pytest, k6, locust
├── pytest.ini
└── Dockerfile

docker-compose.yml
Makefile
```

**Structure Decision**: Web application Monorepo structure with separate frontend (Next.js) and backend (Python/FastAPI) projects. Frontend handles UI components, state management, and HTTP client; Backend provides REST API endpoints for data aggregation from Google Sheets with caching strategy.

## Complexity Tracking

> **No Constitution violations detected. All gates passed.**

| Item | Status | Notes |
|------|--------|-------|
| Spec-Driven Development | ✅ PASS | 3 user stories, 23 AC scenarios, clear acceptance criteria |
| Template Compliance | ✅ PASS | All placeholders filled, Traditional Chinese used consistently |
| Testing Coverage | ⏳ PHASE 2 | Will be completed during implementation phase |
| Consistency Check | ✅ PASS | Terminology, data schema constraints, communication style verified |
| Pedagogical Value | ✅ PASS | Edge cases, rationale, and Jira Dashboard context documented |

---

## Phase 0: Research Tasks

**Identified Research Needs**: None - All technical context fully specified in Feature Specification and Reference Documentation

- ✅ Tech stack choices documented in tech-overview.md
- ✅ Data architecture specified in table-schema.md
- ✅ Performance requirements defined in spec.md (SC-001 through SC-011)
- ✅ Constraints documented (Edge Cases section)

**Research Consolidation**: research.md will document implementation approach for:
1. Google Sheets CSV API integration strategy
2. In-memory cache implementation (5-minute TTL)
3. Data transformation from raw 23-column format to metric calculations
4. Loading spinner implementation for slow network scenarios
5. Sprint filter deduplication logic (Sprint Name + Sprint ID)

---

## Phase 1: Design & Contracts Deliverables

### Artifacts to Generate:

1. **data-model.md**
   - Entity definitions: Issue, Sprint, StatusDistribution, MetricCard
   - Field mapping from rawData (23 columns) to domain models
   - Validation rules for each entity
   - State transitions (Sprint state: future → active → closed)

2. **contracts/api-endpoints.md**
   - GET /api/dashboard/metrics - Returns 4 metric cards
   - GET /api/dashboard/status-distribution - Returns status distribution data
   - GET /api/sprints - Returns available sprint options
   - Request/Response schemas using TypeScript types

3. **contracts/data-contracts.md**
   - Google Sheets CSV format specification
   - rawData table schema (23 columns A:W with field indices)
   - GetJiraSprintValues schema (9 columns A:I)
   - Data type mapping and null handling

4. **quickstart.md**
   - Development environment setup
   - Running frontend: `cd frontend && npm install && npm run dev`
   - Running backend: `cd backend && pip install -r requirements.txt && python src/main.py`
   - Running with Docker: `docker-compose up`
   - Key environment variables (NEXT_PUBLIC_API_URL, GoogleSheets__SheetId, etc.)

---

## Implementation Approach

### Frontend (Next.js 15 + React 19)

**Architecture Pattern**:
- React Server Components for layout/pages
- Client components for interactive features (SprintFilter, chart interactions)
- Custom hooks for data fetching and state management (useDashboardData)
- TypeScript for type safety

**Key Components**:
- **MetricCard**: Displays single metric with icon, title, value
- **StatusDistributionChart**: Recharts bar chart with 9 fixed statuses
- **SprintFilter**: Dropdown selector with deduplication logic
- **LoadingSpinner**: Persistent spinner during data load (no timeout)

**Data Flow**:
1. useDashboardData hook fetches from `/api/dashboard/*` endpoints
2. State: selectedSprint → filters all data client-side
3. UI components consume data via context/props

**Error Handling**:
- Display error boundary for API failures
- Show empty state when no data available
- Handle non-numeric Story Points (treat as 0)

### Backend (Python 3.11 + FastAPI)

**Architecture Pattern**:
- Dependency Injection for service layer
- Async/await for I/O operations
- Pandas for CSV parsing and data transformation

**Key Services**:
- **GoogleSheetsService**: Fetch CSV from public URL, parse to DataFrame
- **CacheService**: In-memory TTL-based cache (5 minutes)
- **DataProcessor**: Transform raw 23-column data to metrics, handle invalid statuses

**API Endpoints**:
- **GET /api/dashboard/metrics**: Calculate and return 4 metrics
- **GET /api/dashboard/status-distribution**: Count issues per status (9 fixed values)
- **GET /api/sprints**: Return sprint options from GetJiraSprintValues

**Data Processing Logic**:
- Parse rawData: 23 columns → Issue entities
- Metrics calculation:
  - Total Issue Count: row count (include invalid statuses)
  - Total Story Points: sum(row[15]) or 0 for non-numeric
  - Total Done Item Count: count(row[5] == "Done")
  - Done Story Points: sum(row[15] where row[5] == "Done")
- Status Distribution:
  - Fixed 9-status order (not from data)
  - Count issues per status, ignore unknown statuses
- Sprint Filtering:
  - Extract Sprint Names from GetJiraSprintValues (Column C)
  - Handle duplicates: append (Sprint ID) format
  - Filter rawData by Sprint Name

**Error Handling**:
- Catch Google Sheets API errors → return cached data or empty response
- Log data parsing errors but don't fail
- Validate CSV format, handle truncated/incomplete data

---

## Next Steps

1. **Phase 0**: Generate research.md documenting implementation approach
2. **Phase 1**: Generate data-model.md, API contracts, and quickstart.md
3. **Phase 2**: `/speckit.tasks` command will generate detailed implementation tasks from spec.md
4. **Phase 3**: Begin implementation following test-first (TDD) approach from tasks.md
