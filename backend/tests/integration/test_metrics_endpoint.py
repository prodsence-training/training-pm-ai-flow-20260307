"""
Integration tests for GET /api/dashboard/metrics endpoint
對應 tasks.md T025

測試目標：
- 測試 endpoint 回應結構和計算正確性
- 測試 Sprint 篩選（"All", 特定 Sprint, "No Sprints"）
- 測試快取行為（首次請求 vs 快取命中）
- 測試錯誤處理
"""
import pytest
from tests.fixtures.sample_raw_data import (
    SAMPLE_RAW_DATA_BASIC,
    SAMPLE_RAW_DATA_ALL_STATUSES,
    SAMPLE_RAW_DATA_EMPTY,
)


class TestMetricsEndpoint:
    """測試 GET /api/dashboard/metrics endpoint"""

    def test_get_metrics_basic(self, test_client, mock_sheets_service):
        """
        測試基本指標計算
        對應 TC-DASHBOARD-002
        """
        # 使用基本測試資料
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        response = test_client.get("/api/dashboard/metrics?sprint=All")

        assert response.status_code == 200
        data = response.json()

        # 驗證回應結構
        assert "totalIssueCount" in data
        assert "totalStoryPoints" in data
        assert "totalDoneItemCount" in data
        assert "doneStoryPoints" in data
        assert "timestamp" in data
        assert "cacheHit" in data

        # 驗證計算結果（SAMPLE_RAW_DATA_BASIC 有 6 筆，3 筆 Done）
        assert data["totalIssueCount"] == 6
        assert data["totalDoneItemCount"] == 3
        assert data["cacheHit"] is False  # 首次請求不是快取

    def test_get_metrics_all_statuses_dataset(self, test_client, mock_sheets_service):
        """
        測試涵蓋所有 9 種狀態的資料集
        對應 TC-DASHBOARD-002 和 TC-CHART-002 整合場景
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_ALL_STATUSES)

        response = test_client.get("/api/dashboard/metrics?sprint=All")

        assert response.status_code == 200
        data = response.json()

        # SAMPLE_RAW_DATA_ALL_STATUSES 包含 27 筆 Issue
        # 其中 8 筆 Done
        assert data["totalIssueCount"] == 27
        assert data["totalDoneItemCount"] == 8

    def test_get_metrics_empty_dataset(self, test_client, mock_sheets_service):
        """
        測試空資料集
        對應 TC-DASHBOARD-003
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_EMPTY)

        response = test_client.get("/api/dashboard/metrics?sprint=All")

        assert response.status_code == 200
        data = response.json()

        # 所有指標應為 0
        assert data["totalIssueCount"] == 0
        assert data["totalStoryPoints"] == 0.0
        assert data["totalDoneItemCount"] == 0
        assert data["doneStoryPoints"] == 0.0

    def test_get_metrics_sprint_filter_all(self, test_client, mock_sheets_service):
        """
        測試 Sprint 篩選：All
        對應 TC-FILTER-005
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        response = test_client.get("/api/dashboard/metrics?sprint=All")

        assert response.status_code == 200
        data = response.json()

        # 應包含所有 Issue（6 筆）
        assert data["totalIssueCount"] == 6

    def test_get_metrics_sprint_filter_specific(self, test_client, mock_sheets_service):
        """
        測試 Sprint 篩選：特定 Sprint
        對應 TC-FILTER-006
        """
        # SAMPLE_RAW_DATA_BASIC 有 "Sprint 1" 和 "Sprint 2"
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        response = test_client.get("/api/dashboard/metrics?sprint=Sprint 1")

        assert response.status_code == 200
        data = response.json()

        # Sprint 1 有 3 筆 Issue（前 3 筆）
        # 其中 2 筆 Done
        assert data["totalIssueCount"] == 3
        assert data["totalDoneItemCount"] == 2

    def test_get_metrics_sprint_filter_no_sprints(self, test_client, mock_sheets_service):
        """
        測試 Sprint 篩選：No Sprints
        對應 TC-FILTER-007
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        response = test_client.get("/api/dashboard/metrics?sprint=No Sprints")

        assert response.status_code == 200
        data = response.json()

        # SAMPLE_RAW_DATA_BASIC 有 1 筆無 Sprint 的 Issue（PROJ-005）
        assert data["totalIssueCount"] == 1
        assert data["totalDoneItemCount"] == 1

    def test_get_metrics_caching_behavior(self, test_client, mock_sheets_service, mock_cache_service):
        """
        測試快取行為
        對應 TC-DASHBOARD-004（快取機制）
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        # 首次請求
        response1 = test_client.get("/api/dashboard/metrics?sprint=All")
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["cacheHit"] is False

        # 第二次請求（應從快取返回）
        response2 = test_client.get("/api/dashboard/metrics?sprint=All")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["cacheHit"] is True

        # 驗證資料一致
        assert data1["totalIssueCount"] == data2["totalIssueCount"]
        assert data1["totalStoryPoints"] == data2["totalStoryPoints"]

    def test_get_metrics_different_sprints_different_cache(
        self, test_client, mock_sheets_service
    ):
        """測試不同 Sprint 使用不同快取"""
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        # 請求 Sprint 1
        response1 = test_client.get("/api/dashboard/metrics?sprint=Sprint 1")
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["cacheHit"] is False

        # 請求 Sprint 2（應該是不同快取）
        response2 = test_client.get("/api/dashboard/metrics?sprint=Sprint 2")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["cacheHit"] is False  # 不同快取 key

        # 再次請求 Sprint 1（應該快取命中）
        response3 = test_client.get("/api/dashboard/metrics?sprint=Sprint 1")
        assert response3.status_code == 200
        data3 = response3.json()
        assert data3["cacheHit"] is True

    def test_get_metrics_default_sprint_parameter(self, test_client, mock_sheets_service):
        """測試沒有提供 sprint 參數時預設為 'All'"""
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        # 不提供 sprint 參數
        response = test_client.get("/api/dashboard/metrics")

        assert response.status_code == 200
        data = response.json()

        # 應返回所有 Issue
        assert data["totalIssueCount"] == 6

    def test_get_metrics_response_structure(self, test_client, mock_sheets_service):
        """測試回應結構完整性"""
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        response = test_client.get("/api/dashboard/metrics?sprint=All")

        assert response.status_code == 200
        data = response.json()

        # 驗證所有必要欄位存在且型別正確
        assert isinstance(data["totalIssueCount"], int)
        assert isinstance(data["totalStoryPoints"], (int, float))
        assert isinstance(data["totalDoneItemCount"], int)
        assert isinstance(data["doneStoryPoints"], (int, float))
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["cacheHit"], bool)

    def test_get_metrics_story_points_precision(self, test_client, mock_sheets_service):
        """測試 Story Points 的小數點精確度（應四捨五入到 2 位）"""
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        response = test_client.get("/api/dashboard/metrics?sprint=All")

        assert response.status_code == 200
        data = response.json()

        # 驗證小數點精確度
        assert isinstance(data["totalStoryPoints"], (int, float))
        assert isinstance(data["doneStoryPoints"], (int, float))

        # 檢查小數位數（轉字串後檢查）
        total_points_str = str(data["totalStoryPoints"])
        done_points_str = str(data["doneStoryPoints"])

        if "." in total_points_str:
            decimal_places = len(total_points_str.split(".")[1])
            assert decimal_places <= 2, "Total Story Points 應最多 2 位小數"

        if "." in done_points_str:
            decimal_places = len(done_points_str.split(".")[1])
            assert decimal_places <= 2, "Done Story Points 應最多 2 位小數"
