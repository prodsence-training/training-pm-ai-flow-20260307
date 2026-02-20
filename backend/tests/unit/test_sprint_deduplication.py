"""
Unit tests for DataProcessor.generate_sprint_options
對應 tasks.md T050

測試目標：
- 驗證重複 Sprint Name 的檢測和 ID 附加邏輯
- 驗證 "All" 和 "No Sprints" 始終存在
- 驗證排序順序（alphabetically between "All" and "No Sprints"）
- 驗證空 Sprint 資料處理
"""
import pytest
from src.services.data_processor import DataProcessor
from src.models.sprint import Sprint, SprintState


class TestSprintDeduplication:
    """測試 DataProcessor.generate_sprint_options 方法"""

    @pytest.fixture
    def processor(self):
        """創建 DataProcessor 實例"""
        return DataProcessor()

    def test_generate_sprint_options_basic(self, processor):
        """
        測試基本 Sprint 選項生成
        對應 TC-FILTER-002
        """
        sprints = [
            Sprint(board_id=10, board_name="Dev Board", sprint_name="Sprint A",
                   sprint_id=101, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
            Sprint(board_id=10, board_name="Dev Board", sprint_name="Sprint B",
                   sprint_id=102, state=SprintState.ACTIVE, start_date="2025-01-15",
                   end_date="2025-01-28"),
            Sprint(board_id=10, board_name="Dev Board", sprint_name="Sprint C",
                   sprint_id=103, state=SprintState.CLOSED, start_date="2024-12-15",
                   end_date="2024-12-28"),
        ]

        options = processor.generate_sprint_options(sprints)

        # 驗證選項結構
        assert options[0] == "All", "第一個選項應為 'All'"
        assert options[-1] == "No Sprints", "最後一個選項應為 'No Sprints'"

        # 驗證 Sprint 選項（應包含所有 3 個 Sprint）
        assert "Sprint A" in options
        assert "Sprint B" in options
        assert "Sprint C" in options

        # 總選項數：All + 3 個 Sprint + No Sprints = 5
        assert len(options) == 5

    def test_generate_sprint_options_with_duplicates(self, processor):
        """
        測試重複 Sprint Name 的處理
        對應 TC-FILTER-004
        """
        sprints = [
            Sprint(board_id=10, board_name="Dev Board", sprint_name="Sprint 1",
                   sprint_id=11, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
            Sprint(board_id=10, board_name="Dev Board", sprint_name="Sprint 1",
                   sprint_id=15, state=SprintState.CLOSED, start_date="2024-12-01",
                   end_date="2024-12-14"),
            Sprint(board_id=10, board_name="Dev Board", sprint_name="Sprint 2",
                   sprint_id=20, state=SprintState.FUTURE, start_date="2025-01-15",
                   end_date="2025-01-28"),
        ]

        options = processor.generate_sprint_options(sprints)

        # 驗證 "All" 和 "No Sprints" 存在
        assert options[0] == "All"
        assert options[-1] == "No Sprints"

        # 驗證重複的 "Sprint 1" 附加了 Sprint ID
        assert "Sprint 1 (11)" in options
        assert "Sprint 1 (15)" in options

        # 驗證唯一的 "Sprint 2" 不附加 ID
        assert "Sprint 2" in options
        assert "Sprint 2 (20)" not in options

        # 驗證重複名稱的原始名稱不存在（應該被替換為帶 ID 的版本）
        sprint_names_without_all = [opt for opt in options if opt not in ["All", "No Sprints"]]
        assert "Sprint 1" not in sprint_names_without_all, "重複的 Sprint Name 不應單獨存在"

    def test_generate_sprint_options_sorting(self, processor):
        """
        測試 Sprint 選項的排序
        應按字母順序排列（在 "All" 和 "No Sprints" 之間）
        """
        sprints = [
            Sprint(board_id=10, board_name="Board", sprint_name="Zebra Sprint",
                   sprint_id=203, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
            Sprint(board_id=10, board_name="Board", sprint_name="Alpha Sprint",
                   sprint_id=201, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
            Sprint(board_id=10, board_name="Board", sprint_name="Beta Sprint",
                   sprint_id=202, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
        ]

        options = processor.generate_sprint_options(sprints)

        # 提取中間的 Sprint 選項（排除 "All" 和 "No Sprints"）
        sprint_options = options[1:-1]

        # 驗證排序（應為 Alpha -> Beta -> Zebra）
        assert sprint_options == ["Alpha Sprint", "Beta Sprint", "Zebra Sprint"], \
            "Sprint 選項應按字母順序排列"

    def test_generate_sprint_options_empty_dataset(self, processor):
        """
        測試空 Sprint 資料集
        對應 TC-EDGE-004
        """
        sprints = []

        options = processor.generate_sprint_options(sprints)

        # 應只返回 "All" 和 "No Sprints"
        assert options == ["All", "No Sprints"], \
            "空資料集應只返回 'All' 和 'No Sprints'"

    def test_generate_sprint_options_all_duplicates(self, processor):
        """測試所有 Sprint 名稱都重複的情況"""
        sprints = [
            Sprint(board_id=10, board_name="Board", sprint_name="Sprint",
                   sprint_id=1, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
            Sprint(board_id=10, board_name="Board", sprint_name="Sprint",
                   sprint_id=2, state=SprintState.ACTIVE, start_date="2025-01-15",
                   end_date="2025-01-28"),
            Sprint(board_id=10, board_name="Board", sprint_name="Sprint",
                   sprint_id=3, state=SprintState.CLOSED, start_date="2024-12-01",
                   end_date="2024-12-14"),
        ]

        options = processor.generate_sprint_options(sprints)

        # 所有 Sprint 選項都應附加 ID
        assert "Sprint (1)" in options
        assert "Sprint (2)" in options
        assert "Sprint (3)" in options

        # 原始名稱不應單獨存在
        sprint_names_without_all = [opt for opt in options if opt not in ["All", "No Sprints"]]
        assert "Sprint" not in sprint_names_without_all

    def test_generate_sprint_options_mixed_duplicates(self, processor):
        """測試混合場景：部分重複，部分唯一"""
        sprints = [
            Sprint(board_id=10, board_name="Board", sprint_name="Dev Sprint",
                   sprint_id=10, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
            Sprint(board_id=10, board_name="Board", sprint_name="Dev Sprint",
                   sprint_id=20, state=SprintState.CLOSED, start_date="2024-12-01",
                   end_date="2024-12-14"),
            Sprint(board_id=10, board_name="Board", sprint_name="QA Sprint",
                   sprint_id=30, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
            Sprint(board_id=10, board_name="Board", sprint_name="Release Sprint",
                   sprint_id=40, state=SprintState.FUTURE, start_date="2025-02-01",
                   end_date="2025-02-14"),
            Sprint(board_id=10, board_name="Board", sprint_name="Release Sprint",
                   sprint_id=50, state=SprintState.FUTURE, start_date="2025-03-01",
                   end_date="2025-03-14"),
        ]

        options = processor.generate_sprint_options(sprints)

        # 驗證重複的附加 ID
        assert "Dev Sprint (10)" in options
        assert "Dev Sprint (20)" in options
        assert "Release Sprint (40)" in options
        assert "Release Sprint (50)" in options

        # 驗證唯一的不附加 ID
        assert "QA Sprint" in options
        assert "QA Sprint (30)" not in options

        # 總選項數：All + 5 個 Sprint + No Sprints = 7
        assert len(options) == 7

    def test_generate_sprint_options_duplicate_ids_sorted(self, processor):
        """測試重複名稱的 Sprint ID 按數字排序"""
        sprints = [
            Sprint(board_id=10, board_name="Board", sprint_name="Sprint",
                   sprint_id=100, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
            Sprint(board_id=10, board_name="Board", sprint_name="Sprint",
                   sprint_id=50, state=SprintState.ACTIVE, start_date="2025-01-15",
                   end_date="2025-01-28"),
            Sprint(board_id=10, board_name="Board", sprint_name="Sprint",
                   sprint_id=75, state=SprintState.CLOSED, start_date="2024-12-01",
                   end_date="2024-12-14"),
        ]

        options = processor.generate_sprint_options(sprints)

        # 找到所有 "Sprint" 相關選項的索引
        sprint_options = [opt for opt in options if opt.startswith("Sprint (")]

        # 驗證 Sprint ID 排序（應為 50 -> 75 -> 100）
        assert sprint_options == ["Sprint (50)", "Sprint (75)", "Sprint (100)"], \
            "重複名稱的 Sprint ID 應按數字排序"

    def test_generate_sprint_options_empty_sprint_names(self, processor):
        """測試空 Sprint 名稱的處理"""
        sprints = [
            Sprint(board_id=10, board_name="Board", sprint_name="Valid Sprint",
                   sprint_id=10, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
            Sprint(board_id=10, board_name="Board", sprint_name="",
                   sprint_id=20, state=SprintState.ACTIVE, start_date="2025-01-15",
                   end_date="2025-01-28"),
            Sprint(board_id=10, board_name="Board", sprint_name=None,
                   sprint_id=30, state=SprintState.CLOSED, start_date="2024-12-01",
                   end_date="2024-12-14"),
        ]

        options = processor.generate_sprint_options(sprints)

        # 空名稱的 Sprint 應被忽略
        assert "Valid Sprint" in options
        assert "" not in options
        assert None not in options

        # 總選項數：All + Valid Sprint + No Sprints = 3
        assert len(options) == 3

    def test_generate_sprint_options_case_sensitive(self, processor):
        """測試 Sprint 名稱是否大小寫敏感"""
        sprints = [
            Sprint(board_id=10, board_name="Board", sprint_name="sprint",
                   sprint_id=10, state=SprintState.ACTIVE, start_date="2025-01-01",
                   end_date="2025-01-14"),
            Sprint(board_id=10, board_name="Board", sprint_name="Sprint",
                   sprint_id=20, state=SprintState.ACTIVE, start_date="2025-01-15",
                   end_date="2025-01-28"),
            Sprint(board_id=10, board_name="Board", sprint_name="SPRINT",
                   sprint_id=30, state=SprintState.CLOSED, start_date="2024-12-01",
                   end_date="2024-12-14"),
        ]

        options = processor.generate_sprint_options(sprints)

        # 不同大小寫應視為不同的 Sprint Name
        assert "SPRINT" in options
        assert "Sprint" in options
        assert "sprint" in options

        # 沒有重複，所以不應附加 ID
        assert "SPRINT (30)" not in options
        assert "Sprint (20)" not in options
        assert "sprint (10)" not in options
