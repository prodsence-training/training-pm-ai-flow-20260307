# Implementation Tasks: Jira Dashboard MVP v1.0

**Generated**: 2025-10-29 | **Phase**: Phase 2 - Implementation
**Approach**: Test-Driven Development (TDD) - Tests first, implementation follows
**Status**: Ready for execution

---

## Overview

This document defines all implementation tasks for the Jira Dashboard MVP v1.0, organized by user story with complete test coverage. The implementation follows a TDD-first approach where test cases guide the development of each feature.

**Total Tasks**: 42 implementation tasks + 23 test tasks = 65 total tasks
**Organized by**: User Story (priority order from spec.md)
**Dependencies**: All foundational infrastructure must complete before user story tasks

---

## Phase Structure

1. **Phase 1: Setup** (3 tasks) - Project initialization
2. **Phase 2: Foundational** (5 tasks) - Blocking prerequisites for all user stories
3. **Phase 3: User Story 1** (15 tasks) - Metric Cards Implementation
4. **Phase 4: User Story 2** (14 tasks) - Status Distribution Chart Implementation
5. **Phase 5: User Story 3** (18 tasks) - Sprint Filter Implementation
6. **Phase 6: Polish** (3 tasks) - Error handling, optimization, documentation

---

## Phase 1: Setup (Project Initialization)

Initialize the monorepo structure, dependencies, and environment configuration.

**Goal**: Establish baseline development environment
**Tests**: No specific tests required for setup phase
**Estimated Duration**: 1-2 hours
**Blocking**: Yes - all subsequent phases depend on setup completion

### Tasks

- [X] T001 Initialize Node.js project and npm workspaces in `/frontend` and `/backend` directories

- [X] T002 Install frontend dependencies in `frontend/package.json`: Next.js 15.2.4, React 19.0.0, TypeScript 5.x, Tailwind CSS 3.4.x, Recharts 2.x, shadcn/ui, React Hook Form 7.x, Zod 3.x, Jest 29.x, React Testing Library 14.x

- [X] T003 Install backend dependencies in `backend/requirements.txt`: Python 3.11, FastAPI 0.104.1, Uvicorn 0.24.0, Pandas 2.1.3, pytest 7.4.3, pytest-asyncio 0.21.1, httpx 0.25.2

---

## Phase 2: Foundational Infrastructure (Blocking Prerequisites)

Establish shared infrastructure, type definitions, and service layer that supports all user stories.

**Goal**: Create reusable foundation for all data processing and API integration
**Tests**: Unit tests for each service (7 tests)
**Estimated Duration**: 3-4 hours
**Blocking**: Yes - User stories depend on these services

### Tasks

#### Backend Data Models & Services

- [X] T004 [P] Create Issue data model in `backend/src/models/issue.py` with Python `@dataclass` containing all 23 field mappings from rawData table (indices 0-22), including `from_row()` static method for CSV conversion and type coercion for Story Points (non-numeric → 0)

- [X] T005 [P] Create Sprint data model in `backend/src/models/sprint.py` with Python `@dataclass` containing 9 field mappings from GetJiraSprintValues table (A-I), SprintState enum (future/active/closed), and `from_row()` static method

- [X] T006 [P] Create metric data models in `backend/src/models/metric.py`: DashboardMetrics dataclass (total_issue_count, total_story_points, total_done_item_count, done_story_points), StatusDistribution dataclass, and FIXED_STATUSES constant with 9 status values in fixed order

- [X] T007 Create Google Sheets CSV API service in `backend/src/services/google_sheets_service.py` with `GoogleSheetsService` class that:
  - Implements `async def fetch_raw_data()` → downloads CSV from public Google Sheets export URL (read sheet ID from environment variable)
  - Implements `async def fetch_sprint_data()` → downloads GetJiraSprintValues sheet
  - Parses CSV to list[list[str]] format
  - Handles HTTP connection errors with graceful fallback

- [X] T008 Create in-memory cache service in `backend/src/services/cache_service.py` with `CacheService` class that:
  - Stores key-value pairs with 5-minute TTL
  - Implements `get(key: str)` → returns cached value or None
  - Implements `set(key: str, value: any, ttl_seconds: int = 300)` → stores value with expiration
  - Auto-expiry: removes expired entries on access

- [X] T009 Create data processor service in `backend/src/services/data_processor.py` with `DataProcessor` class that:
  - Implements `parse_issues(raw_data: list[list[str]]) → List[Issue]` (uses Issue.from_row)
  - Implements `parse_sprints(sprint_data: list[list[str]]) → List[Sprint]` (uses Sprint.from_row)
  - Implements `calculate_metrics(issues: List[Issue], sprint_filter: str = "All") → DashboardMetrics` (filters by sprint, counts, sums)
  - Implements `calculate_status_distribution(issues: List[Issue]) → List[StatusDistribution]` (counts per status, calculates percentages, respects FIXED_STATUSES order, ignores invalid statuses)

- [X] T010 [P] Create TypeScript type definitions in `frontend/src/types/dashboard.ts` with Issue interface (23 fields indexed 0-22), Sprint interface, StatusDistribution interface, MetricCard interface, DashboardMetrics interface, parseIssueFromRow function, and FIXED_STATUSES constant matching backend

#### Frontend API & Services

- [X] T011 Create API client service in `frontend/src/services/api.ts` with `DashboardApiClient` class that:
  - Implements `async getMetrics(sprint: string = "All") → DashboardMetrics` (GET /api/dashboard/metrics?sprint=...)
  - Implements `async getStatusDistribution(sprint: string = "All") → StatusDistribution[]` (GET /api/dashboard/status-distribution?sprint=...)
  - Implements `async getSprints() → string[]` (GET /api/sprints)
  - Uses base URL from `process.env.NEXT_PUBLIC_API_URL` or localhost:8000
  - Includes error handling and request timeout (30 seconds)

---

## Phase 3: User Story 1 - Metric Cards (Priority P1)

**User Story**: 作為專案經理，我希望能在儀表板上即時查看專案的關鍵統計指標（總 Issue 數、總故事點數、已完成 Issue 數、已完成故事點數），以便快速了解專案整體健康度和進度狀況。

**Goal**: Display 4 metric cards with accurate calculations
**Tests**: 5 tests - test case execution (US1 scenarios 1-5)
**Estimated Duration**: 4-5 hours
**Independent Test**: Verify 4 metric cards display correct values
**Success Criteria**: SC-001 (< 3 seconds load time), SC-010 (100% calculation accuracy)

### Test Tasks (Execute Test Cases)

- [X] T012 [US1] Execute TC-DASHBOARD-001: Display four metric cards on dashboard page load - validate card titles, icons, and layout in `frontend/tests/e2e/dashboard.spec.ts`

- [X] T013 [US1] Execute TC-DASHBOARD-002: Calculate and display correct metric values - validate totalIssueCount, totalStoryPoints, totalDoneItemCount, doneStoryPoints match test fixture in `frontend/tests/e2e/dashboard.spec.ts`

- [X] T014 [US1] Execute TC-DASHBOARD-003: Handle empty data - verify cards display 0 when rawData has no rows in `frontend/tests/e2e/dashboard.spec.ts`

- [X] T015 [US1] Execute TC-DASHBOARD-004: Display updated values after cache expiry - verify new data displayed 5 minutes later in `frontend/tests/e2e/dashboard.spec.ts`

- [X] T016 [US1] Execute TC-DASHBOARD-LOADING: Display loading spinner - verify spinner shown during data fetch in `frontend/tests/e2e/dashboard.spec.ts`

### Backend Implementation

- [ ] T017 [P] [US1] Create FastAPI endpoint `GET /api/dashboard/metrics` in `backend/src/api/routes.py` that:
  - Accepts optional `sprint` query parameter (default "All")
  - Calls GoogleSheetsService.fetch_raw_data() with caching via CacheService
  - Parses data using DataProcessor.parse_issues()
  - Filters by sprint (calls filter_issues_by_sprint helper)
  - Calls DataProcessor.calculate_metrics()
  - Returns DashboardMetrics JSON with `timestamp` and `cacheHit` fields
  - Handles errors (Google Sheets connection, parsing) with 500 response

- [ ] T018 [P] [US1] Create sprint filtering helper function in `backend/src/services/data_processor.py`:
  - `def filter_issues_by_sprint(issues: List[Issue], sprint: str) → List[Issue]`
  - "All" → return all issues
  - "No Sprints" → return issues where sprint field is empty/None
  - Specific sprint → return issues matching sprint name (case-sensitive)

- [ ] T019 [US1] Create dependency injection container in `backend/src/api/dependencies.py` that provides:
  - GoogleSheetsService singleton
  - CacheService singleton
  - DataProcessor instance
  - Makes services available to route handlers

- [ ] T020 [P] [US1] Create React component `frontend/src/components/MetricCard.tsx` that:
  - Accepts MetricCard interface props (title, value, icon, unit)
  - Displays card with icon, title, numeric value, and optional unit
  - Uses Tailwind CSS with blue theme (#3b82f6)
  - Shows value right-aligned, large font (responsive)
  - Responsive layout (stacks on mobile, 2x2 grid on desktop)

- [ ] T021 [P] [US1] Create custom hook `frontend/src/hooks/useDashboardData.ts` that:
  - Implements `useDashboardData(sprint: string = "All")` hook
  - Calls DashboardApiClient.getMetrics(sprint)
  - Returns { metrics, loading, error }
  - Updates when sprint parameter changes
  - Handles loading state for SC-011 requirement

- [ ] T022 [US1] Create Metrics display component `frontend/src/components/MetricsGrid.tsx` that:
  - Accepts DashboardMetrics data
  - Uses MetricCard components to render 4 cards (totalIssueCount, totalStoryPoints, totalDoneItemCount, doneStoryPoints)
  - Implements responsive grid layout (2 columns on desktop, 1 on mobile)
  - Shows loading state while data fetching

- [ ] T023 [P] [US1] Create LoadingSpinner component in `frontend/src/components/LoadingSpinner.tsx` that:
  - Displays animated spinner with "Loading..." text
  - Uses Tailwind CSS and blue theme (#3b82f6)
  - No timeout mechanism (remains until data loaded or error occurs)
  - Responsive to screen size

- [ ] T024 [US1] Create backend test file `backend/tests/unit/test_data_processor_metrics.py` that:
  - Tests calculate_metrics with various issue datasets
  - Validates total issue count includes all records (even invalid status)
  - Validates story points sum (non-numeric → 0)
  - Validates done count only counts status == "Done"
  - Validates done story points calculation

- [ ] T025 [US1] Create backend test file `backend/tests/integration/test_metrics_endpoint.py` that:
  - Tests GET /api/dashboard/metrics endpoint with mock Google Sheets data
  - Validates response structure and calculations
  - Tests sprint filtering ("All", specific sprint, "No Sprints")
  - Tests caching behavior (cache hit after first request)

- [ ] T026 [US1] Create frontend test file `frontend/tests/unit/MetricCard.test.tsx` that:
  - Tests MetricCard component rendering (title, value, icon)
  - Tests responsive layout
  - Tests optional unit display

- [ ] T027 [P] [US1] Implement dashboard page layout in `frontend/src/app/(dashboard)/page.tsx` that:
  - Uses useDashboardData hook to fetch metrics
  - Conditionally renders:
    - LoadingSpinner if loading
    - Error message if error (with retry button)
    - MetricsGrid with data if success
  - Passes sprint parameter from context/state to hook

---

## Phase 4: User Story 2 - Status Distribution Chart (Priority P1)

**User Story**: 作為團隊領導，我希望能透過長條圖查看 Issue 在各個狀態的分布情況，以便識別工作流程瓶頸和團隊的工作重心。

**Goal**: Display status distribution bar chart with 9 fixed statuses
**Tests**: 5 tests - test case execution (US2 scenarios 1-5)
**Estimated Duration**: 4-5 hours
**Independent Test**: Verify chart displays 9 statuses in correct order with accurate counts
**Success Criteria**: SC-003 (correct 9 statuses in order), SC-004 (tooltip within 0.5s)

### Test Tasks (Execute Test Cases)

- [X] T028 [US2] Execute TC-CHART-001: Display status distribution chart with 9 statuses in `frontend/tests/e2e/status-chart.spec.ts` - verify chart renders with all 9 statuses in correct order (Backlog → Evaluated → To Do → In Progress → Waiting → Ready to Verify → Done → Invalid → Routine)

- [X] T029 [US2] Execute TC-CHART-002: Display tooltip with value and percentage - verify tooltip appears on hover with count and percentage data in `frontend/tests/e2e/status-chart.spec.ts`

- [X] T030 [US2] Execute TC-CHART-003: Show total issue count at chart bottom - verify total count displayed correctly in `frontend/tests/e2e/status-chart.spec.ts`

- [X] T031 [US2] Execute TC-CHART-004: Display empty state when no data - verify friendly message shown when rawData has no rows in `frontend/tests/e2e/status-chart.spec.ts`

- [X] T032 [US2] Execute TC-CHART-005: Ignore invalid statuses in chart - verify records with unknown status values are excluded from chart but included in total count in `frontend/tests/e2e/status-chart.spec.ts`

### Backend Implementation

- [ ] T033 [P] [US2] Create FastAPI endpoint `GET /api/dashboard/status-distribution` in `backend/src/api/routes.py` that:
  - Accepts optional `sprint` query parameter (default "All")
  - Calls GoogleSheetsService.fetch_raw_data() with caching
  - Parses data using DataProcessor.parse_issues()
  - Filters by sprint using filter_issues_by_sprint
  - Calls DataProcessor.calculate_status_distribution()
  - Returns list of StatusDistribution JSON ordered by FIXED_STATUSES
  - Includes `totalIssueCount`, `timestamp`, `cacheHit` fields
  - Handles errors with 500 response

- [ ] T034 [US2] Create backend test file `backend/tests/unit/test_data_processor_status_distribution.py` that:
  - Tests calculate_status_distribution with sample issues
  - Validates all 9 statuses present in output
  - Validates percentage calculation (count / total * 100)
  - Tests handling of invalid status values (excluded from distribution)
  - Tests empty dataset (all counts = 0)

### Frontend Implementation

- [ ] T035 [P] [US2] Create Recharts bar chart component `frontend/src/components/StatusDistributionChart.tsx` that:
  - Accepts StatusDistribution[] data
  - Displays horizontal bar chart with 9 status categories
  - Shows status names on Y-axis, counts on X-axis
  - Includes Recharts Tooltip with custom formatter showing count and percentage
  - Uses blue color scheme (#3b82f6) for bars
  - Displays total issue count at bottom (as text "Total Issues: X")
  - Responsive container using ResponsiveContainer

- [ ] T036 [US2] Create custom hook `frontend/src/hooks/useStatusDistribution.ts` that:
  - Implements `useStatusDistribution(sprint: string = "All")` hook
  - Calls DashboardApiClient.getStatusDistribution(sprint)
  - Returns { distribution, totalIssueCount, loading, error }
  - Updates when sprint parameter changes

- [ ] T037 [P] [US2] Update dashboard layout `frontend/src/app/(dashboard)/page.tsx` to:
  - Add useStatusDistribution hook below useDashboardData
  - Conditionally render StatusDistributionChart with status distribution data
  - Pass same sprint filter to both hooks
  - Handle loading/error states for chart

- [ ] T038 [US2] Create frontend test file `frontend/tests/unit/StatusDistributionChart.test.tsx` that:
  - Tests chart rendering with 9 statuses
  - Tests status order (Backlog → Routine)
  - Tests data value accuracy
  - Tests tooltip rendering on bar hover

- [ ] T039 [P] [US2] Create empty state component `frontend/src/components/EmptyState.tsx` that:
  - Displays friendly message when no data available
  - Shows icon and text ("No data available")
  - Uses consistent styling with rest of dashboard
  - Responsive layout

---

## Phase 5: User Story 3 - Sprint Filter (Priority P2)

**User Story**: 作為開發團隊成員，我希望能透過 Sprint 篩選器選擇特定的 Sprint，以便專注查看當前或特定 Sprint 的資料。

**Goal**: Implement Sprint dropdown filter with deduplication logic
**Tests**: 8 tests - test case execution (US3 scenarios 1-8)
**Estimated Duration**: 5-6 hours
**Independent Test**: Verify sprint filter options display correctly and filtering works
**Success Criteria**: SC-002 (< 2 seconds update time), SC-009 (correct deduplication)

### Test Tasks (Execute Test Cases)

- [X] T040 [US3] Execute TC-FILTER-001: Display sprint filter dropdown on dashboard - verify dropdown shown with correct styling in `frontend/tests/e2e/sprint-filter.spec.ts`

- [X] T041 [US3] Execute TC-FILTER-002: Display sprint options from GetJiraSprintValues - verify dropdown shows "All", sprint names, and "No Sprints" options in `frontend/tests/e2e/sprint-filter.spec.ts`

- [X] T042 [US3] Execute TC-FILTER-003: Handle duplicate sprint names with Sprint ID - verify duplicate sprints displayed as "Sprint Name (Sprint ID)" format in `frontend/tests/e2e/sprint-filter.spec.ts`

- [X] T043 [US3] Execute TC-FILTER-004: Filter metrics when "All" selected - verify all issues counted when "All" option selected in `frontend/tests/e2e/sprint-filter.spec.ts`

- [X] T044 [US3] Execute TC-FILTER-005: Filter metrics by specific Sprint name - verify only selected sprint's issues counted in `frontend/tests/e2e/sprint-filter.spec.ts`

- [X] T045 [US3] Execute TC-FILTER-006: Filter metrics by "No Sprints" option - verify only issues without sprint shown in `frontend/tests/e2e/sprint-filter.spec.ts`

- [X] T046 [US3] Execute TC-FILTER-007: Update charts on sprint change - verify both metric cards and status chart update when sprint filter changes in `frontend/tests/e2e/sprint-filter.spec.ts`

- [X] T047 [US3] Execute TC-FILTER-008: Display "No Sprints" option - verify "No Sprints" option always available even when no sprint data in `frontend/tests/e2e/sprint-filter.spec.ts`

### Backend Implementation

- [ ] T048 [P] [US3] Create FastAPI endpoint `GET /api/sprints` in `backend/src/api/routes.py` that:
  - Calls GoogleSheetsService.fetch_sprint_data() with caching
  - Parses data using DataProcessor.parse_sprints()
  - Extracts sprint names (Column C) and sprint IDs (Column D)
  - Detects duplicate sprint names
  - Builds options list: ["All", ...sprint_names (with ID appended if duplicate), "No Sprints"]
  - Returns JSON with `options`, `totalSprints`, `duplicateHandled`, `timestamp`, `cacheHit`
  - Handles errors with 500 response

- [ ] T049 [US3] Create sprint deduplication helper in `backend/src/services/data_processor.py`:
  - `def generate_sprint_options(sprints: List[Sprint]) → List[str]`
  - Adds "All" to beginning
  - Groups sprints by name, identifies duplicates
  - For duplicates: appends " (Sprint ID)" to name
  - For non-duplicates: uses plain name
  - Adds "No Sprints" to end
  - Sorts alphabetically (between "All" and "No Sprints")

- [ ] T050 [US3] Create backend test file `backend/tests/unit/test_sprint_deduplication.py` that:
  - Tests generate_sprint_options with various sprint datasets
  - Tests duplicate detection and ID appending
  - Tests "All" and "No Sprints" always present
  - Tests sorting order

- [ ] T051 [US3] Create backend test file `backend/tests/integration/test_sprints_endpoint.py` that:
  - Tests GET /api/sprints endpoint
  - Validates response structure
  - Tests caching behavior

### Frontend Implementation

- [ ] T052 [P] [US3] Create SprintFilter component `frontend/src/components/SprintFilter.tsx` that:
  - Displays as dropdown/select element
  - Accepts sprint options array as prop
  - Accepts selectedSprint and onSprintChange callbacks
  - Default option: "All"
  - Renders all options from props
  - Uses shadcn/ui Select component (or native HTML select with Tailwind styling)
  - Responsive width (full width on mobile, fixed on desktop)
  - Blue theme (#3b82f6) for styling

- [ ] T053 [US3] Create custom hook `frontend/src/hooks/useSprintFilter.ts` that:
  - Implements `useSprintFilter()` hook
  - Calls DashboardApiClient.getSprints()
  - Manages selected sprint state (default "All")
  - Returns { options, selectedSprint, setSelectedSprint, loading, error }
  - Updates metrics and chart when sprint changes

- [ ] T054 [P] [US3] Update dashboard layout `frontend/src/app/(dashboard)/page.tsx` to:
  - Add useSprintFilter hook at top
  - Render SprintFilter component above MetricsGrid
  - Pass selectedSprint to useDashboardData and useStatusDistribution
  - Pass options and setSelectedSprint to SprintFilter component
  - Coordinate data updates across all child components

- [ ] T055 [US3] Create frontend test file `frontend/tests/unit/SprintFilter.test.tsx` that:
  - Tests SprintFilter component rendering with options
  - Tests option selection and callback firing
  - Tests default selection
  - Tests responsive layout

- [ ] T056 [P] [US3] Create context provider for sprint state in `frontend/src/context/SprintContext.tsx`:
  - Provides selectedSprint state across dashboard
  - Allows nested components to access/update sprint filter
  - Reduces prop drilling for sprint filter across components

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Error handling, performance optimization, and production readiness
**Tests**: 4 tests - edge cases (TC-EDGE series)
**Estimated Duration**: 2-3 hours
**Blocking**: No - completes MVP feature set

### Test Tasks (Execute Test Cases)

- [X] T057 Execute TC-EDGE-001: Handle Google Sheets connection errors - verify error message displayed when API unreachable in `frontend/tests/e2e/edge-cases.spec.ts`

- [X] T058 Execute TC-EDGE-002: Handle invalid status values - verify invalid statuses excluded from chart but included in total count in `frontend/tests/e2e/edge-cases.spec.ts`

- [X] T059 Execute TC-EDGE-003: Handle non-numeric story points - verify non-numeric values treated as 0 in calculations in `frontend/tests/e2e/edge-cases.spec.ts`

- [X] T060 Execute TC-EDGE-004: Handle slow network (loading persistence) - verify loading spinner persists without timeout during slow connection in `frontend/tests/e2e/edge-cases.spec.ts`

### Implementation Tasks

- [ ] T061 Create error boundary component `frontend/src/components/ErrorBoundary.tsx` that:
  - Catches React component errors
  - Displays user-friendly error message
  - Includes retry button to reload page
  - Logs errors to console for debugging
  - Prevents complete app crash

- [ ] T062 [P] Create global error handler in `frontend/src/services/api.ts` that:
  - Catches all HTTP errors from DashboardApiClient
  - Returns standardized error response { error, message }
  - Maps HTTP status codes to user-friendly messages
  - Differentiates between Google Sheets errors and backend errors
  - Implements retry logic for transient failures (500, 503)

- [ ] T063 Create backend error logging in `backend/src/api/routes.py` that:
  - Logs all endpoint errors with timestamps and request details
  - Includes error type (ExternalServiceError, DataProcessingError, etc.)
  - Captures Google Sheets API errors for troubleshooting
  - Uses Python logging module

- [ ] T064 [P] Create Docker Compose configuration in `docker-compose.yml` that:
  - Defines frontend service (Next.js on port 3000)
  - Defines backend service (FastAPI on port 8000)
  - Sets environment variables:
    - Frontend: NEXT_PUBLIC_API_URL=http://localhost:8001
    - Backend: GoogleSheets__SheetId, GoogleSheets__RawDataSheet, GoogleSheets__SprintSheet, CacheDuration=300
  - Mounts source code volumes for development
  - Defines shared network between services

- [ ] T065 Create Makefile in repository root with commands:
  - `make dev` - start dev environment (docker-compose up)
  - `make test` - run all tests (frontend + backend)
  - `make test-backend` - run backend tests only
  - `make test-frontend` - run frontend tests only
  - `make build` - build production Docker images
  - `make clean` - stop containers and clean up

---

## Dependency Graph & Execution Order

### Critical Path (Blocking Dependencies)

```
Phase 1: Setup
    ↓
Phase 2: Foundational (T004-T011: Data models, services, API client)
    ↓
Phase 3: User Story 1 (T012-T027: Metric Cards)
    ↓
Phase 4: User Story 2 (T028-T039: Status Chart) [Parallel with T003]
    ↓
Phase 5: User Story 3 (T040-T056: Sprint Filter) [Parallel with T004]
    ↓
Phase 6: Polish (T057-T065: Error handling, Docker)
```

### Parallelizable Tasks

**Phase 3 & 4**: User Story 1 and 2 backend implementation can run in parallel (separate files)
**Phase 4 & 5**: User Story 2 and 3 frontend implementation can run in parallel (separate components)
**Tests**: All test files can be executed in parallel using Jest/pytest with multi-worker setup

---

## Per-User-Story Summary

### User Story 1 - Metric Cards (US1)

| Aspect | Count | Details |
|--------|-------|---------|
| Tests | 5 | TC-DASHBOARD-001 through TC-DASHBOARD-004 + Loading state |
| Backend Tasks | 4 | Metrics endpoint, sprint filter helper, dependency injection, data processor metric calculations |
| Frontend Tasks | 6 | MetricCard component, MetricsGrid, LoadingSpinner, useDashboardData hook, dashboard page layout, component tests |
| Total Tasks | 15 | 5 tests + 10 implementation |
| Est. Duration | 4-5 hours | Includes component creation, endpoint development, testing |
| Success Criteria | SC-001, SC-010 | Load time < 3s, 100% calculation accuracy |

### User Story 2 - Status Chart (US2)

| Aspect | Count | Details |
|--------|-------|---------|
| Tests | 5 | TC-CHART-001 through TC-CHART-005 |
| Backend Tasks | 2 | Status distribution endpoint, backend tests |
| Frontend Tasks | 5 | StatusDistributionChart component, useStatusDistribution hook, empty state, dashboard integration, component tests |
| Total Tasks | 12 | 5 tests + 7 implementation |
| Est. Duration | 4-5 hours | Recharts integration, status ordering logic, tooltip implementation |
| Success Criteria | SC-003, SC-004 | Correct 9 statuses in order, tooltip < 0.5s |

### User Story 3 - Sprint Filter (US3)

| Aspect | Count | Details |
|--------|-------|---------|
| Tests | 8 | TC-FILTER-001 through TC-FILTER-008 |
| Backend Tasks | 4 | Sprint endpoint, deduplication logic, backend tests, endpoint tests |
| Frontend Tasks | 5 | SprintFilter component, useSprintFilter hook, sprint context, dashboard integration, component tests |
| Total Tasks | 17 | 8 tests + 9 implementation |
| Est. Duration | 5-6 hours | Sprint option generation, deduplication, state management |
| Success Criteria | SC-002, SC-009 | Update time < 2s, correct duplicate handling |

### Polish & Cross-Cutting

| Aspect | Count | Details |
|--------|-------|---------|
| Tests | 4 | TC-EDGE-001 through TC-EDGE-004 |
| Implementation | 4 | Error handling, Docker setup, Makefile, logging |
| Total Tasks | 8 | 4 tests + 4 implementation |
| Est. Duration | 2-3 hours | Error boundaries, environment configuration |
| Not Blocking | Yes | Completes MVP, doesn't block earlier features |

---

## Test Infrastructure Setup

### Frontend E2E Tests (Playwright)

- **Location**: `frontend/tests/e2e/`
- **Files**: dashboard.spec.ts, status-chart.spec.ts, sprint-filter.spec.ts, edge-cases.spec.ts
- **Configuration**: `frontend/playwright.config.ts` (headless mode, retries on failure, 30s timeout)
- **Mock Data**: `frontend/tests/fixtures/` (sample rawData and GetJiraSprintValues)
- **API Mocking**: Mock Service Worker (MSW) 2.0+ for Google Sheets API simulation

### Backend Unit Tests (pytest)

- **Location**: `backend/tests/unit/`
- **Files**: test_data_processor_metrics.py, test_data_processor_status_distribution.py, test_sprint_deduplication.py
- **Configuration**: `backend/pytest.ini` (asyncio support, fixtures directory)
- **Test Data**: `backend/tests/fixtures/` (CSV samples matching table schema)

### Backend Integration Tests (pytest + httpx)

- **Location**: `backend/tests/integration/`
- **Files**: test_metrics_endpoint.py, test_sprints_endpoint.py, test_status_distribution_endpoint.py
- **Setup**: In-memory FastAPI TestClient with dependency injection overrides
- **Mock Google Sheets**: Returns fixture data via mocked GoogleSheetsService

---

## Implementation Order Recommendations

### MVP Scope (User Stories 1 & 2)

If time-constrained, implement User Story 1 + 2 for MVP core:
1. **Start**: Phase 1 (Setup) → Phase 2 (Foundational) = 4-5 hours
2. **Then**: Phase 3 (Metric Cards) = 4-5 hours
3. **Then**: Phase 4 (Status Chart) = 4-5 hours
4. **Total**: ~12-15 hours for core MVP

### Full Feature (All User Stories)

1. **Repeat above**: Phases 1-4 = 12-15 hours
2. **Add**: Phase 5 (Sprint Filter) = 5-6 hours
3. **Add**: Phase 6 (Polish) = 2-3 hours
4. **Total**: ~19-24 hours for complete feature

### Parallel Execution (Team of 2)

- **Developer 1**: Backend (Phases 2, 3, 4, 5)
- **Developer 2**: Frontend (Phases 2, 3, 4, 5) - can start after Foundational phase completes
- **Both**: Polish phase (Docker, error handling)

---

## Quality Checkpoints

### Before Submitting PR

- [ ] All tests passing (Jest + pytest)
- [ ] No TypeScript compilation errors
- [ ] No ESLint violations
- [ ] Backend code follows PEP 8
- [ ] API responses match contracts/api-endpoints.md
- [ ] Loading spinner appears immediately on data request
- [ ] Error messages user-friendly (no stack traces)
- [ ] Performance metrics met (SC-001 through SC-011)

### Before Merging to Main

- [ ] Code review approved (minimum 1 reviewer)
- [ ] All 23 acceptance criteria scenarios tested
- [ ] Manual testing on real Google Sheets link
- [ ] Docker Compose successfully starts both services
- [ ] Documentation updated (CLAUDE.md, README.md if applicable)

---

## Related Documents

- [spec.md](./spec.md) - Feature specification with 3 user stories, 23 acceptance criteria
- [data-model.md](./data-model.md) - Entity definitions and data transformation logic
- [contracts/api-endpoints.md](./contracts/api-endpoints.md) - REST API contracts
- [table-schema.md](../../docs/table-schema.md) - Google Sheets rawData (23 columns) and GetJiraSprintValues (9 columns) schema
- [tech-overview.md](../../docs/tech-overview.md) - Technology stack and architecture overview
- [testcases.md](./testcases.md) - Detailed test cases with pre-conditions and expected results

---

**Status**: Ready for Phase 1 execution
**Next Step**: Begin Phase 1 Setup tasks (T001-T003)
**Estimated Total Duration**: 19-24 hours (all 65 tasks)
**Last Updated**: 2025-10-29
