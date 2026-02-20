"""
Unit tests for DataProcessor.calculate_metrics
對應 tasks.md T024

測試目標：
- 驗證 calculate_metrics 正確計算所有指標
- 驗證 total issue count 包含所有記錄（即使 Status 無效）
- 驗證 story points 總和（非數值 → 0）
- 驗證 done count 只計算 status == "Done"
- 驗證 done story points 計算正確
"""
import pytest
from src.services.data_processor import DataProcessor
from src.models.issue import Issue


class TestDataProcessorMetrics:
    """測試 DataProcessor.calculate_metrics 方法"""

    @pytest.fixture
    def processor(self):
        """創建 DataProcessor 實例"""
        return DataProcessor()

    def test_calculate_metrics_basic_dataset(self, processor):
        """
        測試基本資料集的指標計算
        對應 TC-DASHBOARD-002
        """
        # 準備測試資料：10 筆 Issue
        # 其中 4 筆 Status 為 "Done"
        # Total Story Points: 25.5
        # Done Story Points: 12.5
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Issue 1",
                  status="Done", story_points=3.5),
            Issue(key="PROJ-002", issue_type="Task", project="PROJ", summary="Issue 2",
                  status="In Progress", story_points=5.0),
            Issue(key="PROJ-003", issue_type="Bug", project="PROJ", summary="Issue 3",
                  status="Done", story_points=2.0),
            Issue(key="PROJ-004", issue_type="Story", project="PROJ", summary="Issue 4",
                  status="To Do", story_points=8.0),
            Issue(key="PROJ-005", issue_type="Task", project="PROJ", summary="Issue 5",
                  status="Done", story_points=5.0),
            Issue(key="PROJ-006", issue_type="Bug", project="PROJ", summary="Issue 6",
                  status="Waiting", story_points=0.0),
            Issue(key="PROJ-007", issue_type="Story", project="PROJ", summary="Issue 7",
                  status="Done", story_points=2.0),
            Issue(key="PROJ-008", issue_type="Task", project="PROJ", summary="Issue 8",
                  status="Backlog", story_points=0.0),
            Issue(key="PROJ-009", issue_type="Bug", project="PROJ", summary="Issue 9",
                  status="Ready to Verify", story_points=0.0),
            Issue(key="PROJ-010", issue_type="Story", project="PROJ", summary="Issue 10",
                  status="Evaluated", story_points=0.0),
        ]

        metrics = processor.calculate_metrics(issues, sprint_filter="All")

        # 驗證結果
        assert metrics.total_issue_count == 10, "Total Issue Count 應為 10"
        assert metrics.total_story_points == 25.5, "Total Story Points 應為 25.5"
        assert metrics.total_done_item_count == 4, "Total Done Item Count 應為 4"
        assert metrics.done_story_points == 12.5, "Done Story Points 應為 12.5"

    def test_calculate_metrics_empty_dataset(self, processor):
        """
        測試空資料集
        對應 TC-DASHBOARD-003 情境 A
        """
        issues = []

        metrics = processor.calculate_metrics(issues, sprint_filter="All")

        # 所有指標應為 0
        assert metrics.total_issue_count == 0
        assert metrics.total_story_points == 0.0
        assert metrics.total_done_item_count == 0
        assert metrics.done_story_points == 0.0

    def test_calculate_metrics_includes_invalid_status(self, processor):
        """
        測試 Total Issue Count 包含無效 Status 的記錄
        對應 TC-EDGE-002
        """
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Valid 1",
                  status="Done", story_points=5.0),
            Issue(key="PROJ-002", issue_type="Task", project="PROJ", summary="Valid 2",
                  status="In Progress", story_points=3.0),
            # 無效 Status
            Issue(key="PROJ-003", issue_type="Bug", project="PROJ", summary="Invalid 1",
                  status="Unknown", story_points=2.0),
            Issue(key="PROJ-004", issue_type="Story", project="PROJ", summary="Invalid 2",
                  status="Testing", story_points=5.0),
        ]

        metrics = processor.calculate_metrics(issues, sprint_filter="All")

        # Total Issue Count 應包含無效 Status 的記錄
        assert metrics.total_issue_count == 4, "Total Issue Count 應包含所有記錄（含無效 Status）"
        # Total Story Points 應包含無效 Status 的點數
        assert metrics.total_story_points == 15.0, "Total Story Points 應包含所有記錄的點數"
        # Done Count 應只計算 Status == "Done" 的記錄
        assert metrics.total_done_item_count == 1
        assert metrics.done_story_points == 5.0

    def test_calculate_metrics_non_numeric_story_points(self, processor):
        """
        測試非數值 Story Points 視為 0
        對應 TC-EDGE-003
        """
        # Issue.from_row 已處理非數值轉換，這裡測試已轉換後的 Issue
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Valid",
                  status="Done", story_points=5.0),
            Issue(key="PROJ-002", issue_type="Task", project="PROJ", summary="Valid",
                  status="In Progress", story_points=3.5),
            # 非數值已轉換為 0
            Issue(key="PROJ-003", issue_type="Bug", project="PROJ", summary="Non-numeric",
                  status="Done", story_points=0.0),  # 原本是 "TBD"
            Issue(key="PROJ-004", issue_type="Story", project="PROJ", summary="Empty",
                  status="To Do", story_points=0.0),  # 原本是空值
        ]

        metrics = processor.calculate_metrics(issues, sprint_filter="All")

        assert metrics.total_issue_count == 4
        assert metrics.total_story_points == 8.5, "非數值 Story Points 應視為 0"
        assert metrics.total_done_item_count == 2
        assert metrics.done_story_points == 5.0

    def test_calculate_metrics_all_done(self, processor):
        """測試所有 Issue 都完成的情況"""
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Done 1",
                  status="Done", story_points=5.0),
            Issue(key="PROJ-002", issue_type="Task", project="PROJ", summary="Done 2",
                  status="Done", story_points=3.0),
            Issue(key="PROJ-003", issue_type="Bug", project="PROJ", summary="Done 3",
                  status="Done", story_points=2.0),
        ]

        metrics = processor.calculate_metrics(issues, sprint_filter="All")

        assert metrics.total_issue_count == 3
        assert metrics.total_story_points == 10.0
        assert metrics.total_done_item_count == 3
        assert metrics.done_story_points == 10.0

    def test_calculate_metrics_no_done_items(self, processor):
        """測試沒有完成的 Issue"""
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Todo 1",
                  status="To Do", story_points=5.0),
            Issue(key="PROJ-002", issue_type="Task", project="PROJ", summary="InProgress 1",
                  status="In Progress", story_points=3.0),
            Issue(key="PROJ-003", issue_type="Bug", project="PROJ", summary="Waiting 1",
                  status="Waiting", story_points=2.0),
        ]

        metrics = processor.calculate_metrics(issues, sprint_filter="All")

        assert metrics.total_issue_count == 3
        assert metrics.total_story_points == 10.0
        assert metrics.total_done_item_count == 0
        assert metrics.done_story_points == 0.0

    def test_calculate_metrics_with_sprint_filter(self, processor):
        """
        測試 Sprint 篩選功能
        對應 TC-FILTER-006
        """
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Sprint A Issue 1",
                  status="Done", sprint="Sprint A", story_points=5.0),
            Issue(key="PROJ-002", issue_type="Task", project="PROJ", summary="Sprint A Issue 2",
                  status="In Progress", sprint="Sprint A", story_points=3.0),
            Issue(key="PROJ-003", issue_type="Bug", project="PROJ", summary="Sprint B Issue 1",
                  status="Done", sprint="Sprint B", story_points=8.0),
            Issue(key="PROJ-004", issue_type="Story", project="PROJ", summary="No Sprint Issue",
                  status="To Do", sprint=None, story_points=2.0),
        ]

        # 篩選 Sprint A
        metrics = processor.calculate_metrics(issues, sprint_filter="Sprint A")

        assert metrics.total_issue_count == 2, "應只計算 Sprint A 的 Issue"
        assert metrics.total_story_points == 8.0
        assert metrics.total_done_item_count == 1
        assert metrics.done_story_points == 5.0

    def test_calculate_metrics_no_sprints_filter(self, processor):
        """
        測試 "No Sprints" 篩選
        對應 TC-FILTER-007
        """
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Sprint A Issue",
                  status="Done", sprint="Sprint A", story_points=5.0),
            Issue(key="PROJ-002", issue_type="Task", project="PROJ", summary="No Sprint 1",
                  status="Done", sprint=None, story_points=3.0),
            Issue(key="PROJ-003", issue_type="Bug", project="PROJ", summary="No Sprint 2",
                  status="In Progress", sprint="", story_points=2.0),
        ]

        metrics = processor.calculate_metrics(issues, sprint_filter="No Sprints")

        assert metrics.total_issue_count == 2, "應只計算無 Sprint 的 Issue"
        assert metrics.total_story_points == 5.0
        assert metrics.total_done_item_count == 1
        assert metrics.done_story_points == 3.0

    def test_calculate_metrics_decimal_story_points(self, processor):
        """測試小數點 Story Points"""
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Decimal 1",
                  status="Done", story_points=2.5),
            Issue(key="PROJ-002", issue_type="Task", project="PROJ", summary="Decimal 2",
                  status="Done", story_points=3.75),
            Issue(key="PROJ-003", issue_type="Bug", project="PROJ", summary="Decimal 3",
                  status="In Progress", story_points=1.25),
        ]

        metrics = processor.calculate_metrics(issues, sprint_filter="All")

        # 驗證小數點計算精確度（四捨五入到 2 位）
        assert metrics.total_story_points == 7.5
        assert metrics.done_story_points == 6.25

    def test_calculate_metrics_large_dataset(self, processor):
        """測試大量資料集的性能和準確性"""
        issues = []
        expected_done_count = 0
        expected_done_points = 0.0

        for i in range(100):
            status = "Done" if i % 3 == 0 else "In Progress"
            points = float(i % 10)
            issues.append(
                Issue(key=f"PROJ-{i:03d}", issue_type="Story", project="PROJ",
                      summary=f"Issue {i}", status=status, story_points=points)
            )
            if status == "Done":
                expected_done_count += 1
                expected_done_points += points

        metrics = processor.calculate_metrics(issues, sprint_filter="All")

        assert metrics.total_issue_count == 100
        assert metrics.total_done_item_count == expected_done_count
        assert metrics.done_story_points == round(expected_done_points, 2)
