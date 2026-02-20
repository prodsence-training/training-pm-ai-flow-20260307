"""
Integration tests for GET /api/sprints endpoint
對應 tasks.md T051

測試目標：
- 測試 endpoint 回應結構
- 測試 Sprint 選項生成邏輯
- 測試快取行為
- 測試空資料集處理
"""
import pytest
from tests.fixtures.sample_sprint_data import (
    SAMPLE_SPRINT_DATA_BASIC,
    SAMPLE_SPRINT_DATA_DUPLICATES,
    SAMPLE_SPRINT_DATA_EMPTY,
)


class TestSprintsEndpoint:
    """測試 GET /api/sprints endpoint"""

    def test_get_sprints_basic(self, test_client, mock_sheets_service):
        """
        測試基本 Sprint 選項取得
        對應 TC-FILTER-002
        """
        mock_sheets_service.set_sprint_data_fixture(SAMPLE_SPRINT_DATA_BASIC)

        response = test_client.get("/api/sprints")

        assert response.status_code == 200
        data = response.json()

        # 驗證回應結構
        assert "options" in data
        assert "totalSprints" in data
        assert "timestamp" in data
        assert "cacheHit" in data

        # 驗證選項內容
        options = data["options"]
        assert options[0] == "All", "第一個選項應為 'All'"
        assert options[-1] == "No Sprints", "最後一個選項應為 'No Sprints'"

        # SAMPLE_SPRINT_DATA_BASIC 有 3 個 Sprint
        assert data["totalSprints"] == 3
        assert len(options) == 5  # All + 3 Sprints + No Sprints

    def test_get_sprints_includes_all_sprint_names(self, test_client, mock_sheets_service):
        """測試所有 Sprint 名稱都包含在選項中"""
        mock_sheets_service.set_sprint_data_fixture(SAMPLE_SPRINT_DATA_BASIC)

        response = test_client.get("/api/sprints")

        assert response.status_code == 200
        data = response.json()
        options = data["options"]

        # SAMPLE_SPRINT_DATA_BASIC 包含：Sprint 1, Sprint 2, Sprint 3
        assert "Sprint 1" in options
        assert "Sprint 2" in options
        assert "Sprint 3" in options

    def test_get_sprints_with_duplicates(self, test_client, mock_sheets_service):
        """
        測試重複 Sprint Name 的處理
        對應 TC-FILTER-004
        """
        mock_sheets_service.set_sprint_data_fixture(SAMPLE_SPRINT_DATA_DUPLICATES)

        response = test_client.get("/api/sprints")

        assert response.status_code == 200
        data = response.json()
        options = data["options"]

        # SAMPLE_SPRINT_DATA_DUPLICATES 有重複的 "Sprint 1"（ID 11 和 15）
        assert "Sprint 1 (11)" in options
        assert "Sprint 1 (15)" in options
        assert "Sprint 1 (25)" in options  # 第三個 Sprint 1

        # "Sprint 2" 只有一個，不應附加 ID
        assert "Sprint 2" in options
        assert "Sprint 2 (20)" not in options

        # 驗證重複名稱的原始名稱不單獨存在
        sprint_names_without_all = [opt for opt in options if opt not in ["All", "No Sprints"]]
        assert "Sprint 1" not in sprint_names_without_all

    def test_get_sprints_empty_dataset(self, test_client, mock_sheets_service):
        """
        測試空 Sprint 資料集
        對應 TC-EDGE-004
        """
        mock_sheets_service.set_sprint_data_fixture(SAMPLE_SPRINT_DATA_EMPTY)

        response = test_client.get("/api/sprints")

        assert response.status_code == 200
        data = response.json()

        # 應只返回 "All" 和 "No Sprints"
        assert data["options"] == ["All", "No Sprints"]
        assert data["totalSprints"] == 0

    def test_get_sprints_caching_behavior(self, test_client, mock_sheets_service):
        """測試快取行為"""
        mock_sheets_service.set_sprint_data_fixture(SAMPLE_SPRINT_DATA_BASIC)

        # 首次請求
        response1 = test_client.get("/api/sprints")
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["cacheHit"] is False

        # 第二次請求（應從快取返回）
        response2 = test_client.get("/api/sprints")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["cacheHit"] is True

        # 驗證資料一致
        assert data1["options"] == data2["options"]
        assert data1["totalSprints"] == data2["totalSprints"]

    def test_get_sprints_response_structure(self, test_client, mock_sheets_service):
        """測試回應結構完整性"""
        mock_sheets_service.set_sprint_data_fixture(SAMPLE_SPRINT_DATA_BASIC)

        response = test_client.get("/api/sprints")

        assert response.status_code == 200
        data = response.json()

        # 驗證所有必要欄位存在且型別正確
        assert isinstance(data["options"], list)
        assert isinstance(data["totalSprints"], int)
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["cacheHit"], bool)

        # 驗證 options 為字串列表
        for option in data["options"]:
            assert isinstance(option, str)

    def test_get_sprints_options_order(self, test_client, mock_sheets_service):
        """測試 Sprint 選項排序（應按字母順序，在 "All" 和 "No Sprints" 之間）"""
        mock_sheets_service.set_sprint_data_fixture(SAMPLE_SPRINT_DATA_BASIC)

        response = test_client.get("/api/sprints")

        assert response.status_code == 200
        data = response.json()
        options = data["options"]

        # 提取中間的 Sprint 選項
        sprint_options = options[1:-1]

        # 驗證排序（SAMPLE_SPRINT_DATA_BASIC: Sprint 1, Sprint 2, Sprint 3）
        assert sprint_options == sorted(sprint_options), "Sprint 選項應按字母順序排列"

    def test_get_sprints_all_and_no_sprints_always_present(
        self, test_client, mock_sheets_service, mock_cache_service
    ):
        """測試 "All" 和 "No Sprints" 始終存在"""
        # 測試有資料的情況
        mock_sheets_service.set_sprint_data_fixture(SAMPLE_SPRINT_DATA_BASIC)
        response1 = test_client.get("/api/sprints")
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["options"][0] == "All"
        assert data1["options"][-1] == "No Sprints"

        # 測試空資料的情況
        mock_sheets_service.set_sprint_data_fixture(SAMPLE_SPRINT_DATA_EMPTY)

        # 清空快取以測試空資料情況
        mock_cache_service.cache.clear()

        response2 = test_client.get("/api/sprints")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["options"] == ["All", "No Sprints"]

    def test_get_sprints_total_count_accuracy(self, test_client, mock_sheets_service):
        """測試 totalSprints 計數準確性"""
        mock_sheets_service.set_sprint_data_fixture(SAMPLE_SPRINT_DATA_DUPLICATES)

        response = test_client.get("/api/sprints")

        assert response.status_code == 200
        data = response.json()

        # SAMPLE_SPRINT_DATA_DUPLICATES 有 4 個 Sprint 記錄
        assert data["totalSprints"] == 4

        # 選項數應為：All + Sprint 處理後的選項 + No Sprints
        # Sprint 1 (11), Sprint 1 (15), Sprint 1 (25), Sprint 2 = 4 個選項
        assert len(data["options"]) == 6  # All + 4 + No Sprints
