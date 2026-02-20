"""
Integration tests for GET /api/dashboard/status-distribution endpoint
對應 tasks.md 中 T033 相關測試

測試目標：
- 測試 endpoint 回應結構
- 測試 9 個固定狀態順序
- 測試 Sprint 篩選功能
- 測試快取行為
"""
import pytest
from tests.fixtures.sample_raw_data import (
    SAMPLE_RAW_DATA_BASIC,
    SAMPLE_RAW_DATA_ALL_STATUSES,
    SAMPLE_RAW_DATA_INVALID_STATUS,
    SAMPLE_RAW_DATA_EMPTY,
)
from src.models.metric import FIXED_STATUSES


class TestStatusDistributionEndpoint:
    """測試 GET /api/dashboard/status-distribution endpoint"""

    def test_get_status_distribution_basic(self, test_client, mock_sheets_service):
        """
        測試基本狀態分布取得
        對應 TC-CHART-001
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_ALL_STATUSES)

        response = test_client.get("/api/dashboard/status-distribution?sprint=All")

        assert response.status_code == 200
        data = response.json()

        # 驗證回應結構
        assert "distribution" in data
        assert "totalIssueCount" in data
        assert "timestamp" in data
        assert "cacheHit" in data

        # 驗證 distribution 為陣列
        assert isinstance(data["distribution"], list)
        assert len(data["distribution"]) == 9, "應返回 9 個狀態"

    def test_get_status_distribution_correct_order(self, test_client, mock_sheets_service):
        """
        測試狀態順序正確
        對應 TC-CHART-002
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_ALL_STATUSES)

        response = test_client.get("/api/dashboard/status-distribution?sprint=All")

        assert response.status_code == 200
        data = response.json()
        distribution = data["distribution"]

        # 驗證順序符合 FIXED_STATUSES
        expected_order = list(FIXED_STATUSES)
        actual_order = [item["status"] for item in distribution]

        assert actual_order == expected_order, "狀態順序應符合固定順序"

    def test_get_status_distribution_includes_all_fields(
        self, test_client, mock_sheets_service
    ):
        """測試每個狀態項目包含所有必要欄位"""
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_ALL_STATUSES)

        response = test_client.get("/api/dashboard/status-distribution?sprint=All")

        assert response.status_code == 200
        data = response.json()
        distribution = data["distribution"]

        for item in distribution:
            assert "status" in item
            assert "count" in item
            assert "percentage" in item

            # 驗證型別
            assert isinstance(item["status"], str)
            assert isinstance(item["count"], int)
            assert isinstance(item["percentage"], (int, float))

    def test_get_status_distribution_percentage_calculation(
        self, test_client, mock_sheets_service
    ):
        """
        測試百分比計算準確性
        對應 TC-CHART-003
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_ALL_STATUSES)

        response = test_client.get("/api/dashboard/status-distribution?sprint=All")

        assert response.status_code == 200
        data = response.json()
        distribution = data["distribution"]
        total_count = data["totalIssueCount"]

        # 驗證百分比總和約為 100%（考慮四捨五入誤差）
        total_percentage = sum(item["percentage"] for item in distribution)
        assert 99.5 <= total_percentage <= 100.5, "百分比總和應約為 100%"

        # 驗證每個狀態的百分比計算正確
        for item in distribution:
            expected_percentage = round(item["count"] / total_count * 100, 2) if total_count > 0 else 0
            assert item["percentage"] == expected_percentage, \
                f"狀態 {item['status']} 的百分比計算錯誤"

    def test_get_status_distribution_total_issue_count(
        self, test_client, mock_sheets_service
    ):
        """
        測試 totalIssueCount 欄位
        對應 TC-CHART-004
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_ALL_STATUSES)

        response = test_client.get("/api/dashboard/status-distribution?sprint=All")

        assert response.status_code == 200
        data = response.json()

        # SAMPLE_RAW_DATA_ALL_STATUSES 有 27 筆 Issue
        assert data["totalIssueCount"] == 27

        # 驗證分布的總計數與 totalIssueCount 一致
        distribution_total = sum(item["count"] for item in data["distribution"])
        assert distribution_total == data["totalIssueCount"]

    def test_get_status_distribution_empty_dataset(self, test_client, mock_sheets_service):
        """
        測試空資料集
        對應 TC-CHART-005
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_EMPTY)

        response = test_client.get("/api/dashboard/status-distribution?sprint=All")

        assert response.status_code == 200
        data = response.json()

        # 應返回 9 個狀態，但所有 count 和 percentage 都是 0
        assert len(data["distribution"]) == 9
        assert data["totalIssueCount"] == 0

        for item in data["distribution"]:
            assert item["count"] == 0
            assert item["percentage"] == 0.0

    def test_get_status_distribution_excludes_invalid_statuses(
        self, test_client, mock_sheets_service
    ):
        """
        測試無效 Status 被排除在分布外
        對應 TC-EDGE-002
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_INVALID_STATUS)

        response = test_client.get("/api/dashboard/status-distribution?sprint=All")

        assert response.status_code == 200
        data = response.json()
        distribution = data["distribution"]

        # SAMPLE_RAW_DATA_INVALID_STATUS 有 5 筆 Issue
        # 其中 2 筆有效狀態（Done, In Progress）
        # 3 筆無效狀態（Unknown, Testing, Archived）
        assert data["totalIssueCount"] == 5

        # 分布統計應只包含有效狀態的 Issue
        distribution_total = sum(item["count"] for item in distribution)
        assert distribution_total == 2, "分布統計應排除無效 Status"

    def test_get_status_distribution_sprint_filter_specific(
        self, test_client, mock_sheets_service
    ):
        """
        測試 Sprint 篩選功能
        對應 TC-FILTER-006
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        response = test_client.get("/api/dashboard/status-distribution?sprint=Sprint 1")

        assert response.status_code == 200
        data = response.json()

        # Sprint 1 有 3 筆 Issue
        assert data["totalIssueCount"] == 3

        # 分布統計應只包含 Sprint 1 的 Issue
        distribution_total = sum(item["count"] for item in data["distribution"])
        assert distribution_total == 3

    def test_get_status_distribution_sprint_filter_no_sprints(
        self, test_client, mock_sheets_service
    ):
        """
        測試 "No Sprints" 篩選
        對應 TC-FILTER-007
        """
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        response = test_client.get("/api/dashboard/status-distribution?sprint=No Sprints")

        assert response.status_code == 200
        data = response.json()

        # SAMPLE_RAW_DATA_BASIC 有 1 筆無 Sprint 的 Issue
        assert data["totalIssueCount"] == 1

        distribution_total = sum(item["count"] for item in data["distribution"])
        assert distribution_total == 1

    def test_get_status_distribution_caching_behavior(
        self, test_client, mock_sheets_service
    ):
        """測試快取行為"""
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_ALL_STATUSES)

        # 首次請求
        response1 = test_client.get("/api/dashboard/status-distribution?sprint=All")
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["cacheHit"] is False

        # 第二次請求（應從快取返回）
        response2 = test_client.get("/api/dashboard/status-distribution?sprint=All")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["cacheHit"] is True

        # 驗證資料一致
        assert data1["distribution"] == data2["distribution"]
        assert data1["totalIssueCount"] == data2["totalIssueCount"]

    def test_get_status_distribution_different_sprints_different_cache(
        self, test_client, mock_sheets_service
    ):
        """測試不同 Sprint 使用不同快取"""
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_BASIC)

        # 請求 Sprint 1
        response1 = test_client.get("/api/dashboard/status-distribution?sprint=Sprint 1")
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["cacheHit"] is False

        # 請求 All（不同快取 key）
        response2 = test_client.get("/api/dashboard/status-distribution?sprint=All")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["cacheHit"] is False

        # 再次請求 Sprint 1（應快取命中）
        response3 = test_client.get("/api/dashboard/status-distribution?sprint=Sprint 1")
        assert response3.status_code == 200
        data3 = response3.json()
        assert data3["cacheHit"] is True

    def test_get_status_distribution_default_sprint_parameter(
        self, test_client, mock_sheets_service
    ):
        """測試沒有提供 sprint 參數時預設為 'All'"""
        mock_sheets_service.set_raw_data_fixture(SAMPLE_RAW_DATA_ALL_STATUSES)

        response = test_client.get("/api/dashboard/status-distribution")

        assert response.status_code == 200
        data = response.json()

        # 應返回所有 Issue 的分布
        assert data["totalIssueCount"] == 27
