"""
Unit tests for DataProcessor.calculate_status_distribution
對應 tasks.md T034

測試目標：
- 驗證所有 9 個狀態都存在於輸出中
- 驗證百分比計算準確性（count / total * 100）
- 驗證無效 Status 值被排除在分布外
- 驗證空資料集處理（所有 count = 0）
- 驗證狀態順序符合 FIXED_STATUSES
"""
import pytest
from src.services.data_processor import DataProcessor
from src.models.issue import Issue
from src.models.metric import FIXED_STATUSES


class TestDataProcessorStatusDistribution:
    """測試 DataProcessor.calculate_status_distribution 方法"""

    @pytest.fixture
    def processor(self):
        """創建 DataProcessor 實例"""
        return DataProcessor()

    def test_status_distribution_all_statuses_present(self, processor):
        """
        測試所有 9 個固定狀態都出現在輸出中
        對應 TC-CHART-002
        """
        # 準備測試資料：涵蓋所有 9 種狀態
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="1",
                  status="Backlog"),
            Issue(key="PROJ-002", issue_type="Story", project="PROJ", summary="2",
                  status="Evaluated"),
            Issue(key="PROJ-003", issue_type="Story", project="PROJ", summary="3",
                  status="To Do"),
            Issue(key="PROJ-004", issue_type="Story", project="PROJ", summary="4",
                  status="In Progress"),
            Issue(key="PROJ-005", issue_type="Story", project="PROJ", summary="5",
                  status="Waiting"),
            Issue(key="PROJ-006", issue_type="Story", project="PROJ", summary="6",
                  status="Ready to Verify"),
            Issue(key="PROJ-007", issue_type="Story", project="PROJ", summary="7",
                  status="Done"),
            Issue(key="PROJ-008", issue_type="Story", project="PROJ", summary="8",
                  status="Invalid"),
            Issue(key="PROJ-009", issue_type="Story", project="PROJ", summary="9",
                  status="Routine"),
        ]

        distribution = processor.calculate_status_distribution(issues, sprint_filter="All")

        # 驗證所有 9 個狀態都存在
        assert len(distribution) == 9, "應返回 9 個狀態"

        # 驗證每個狀態都出現一次
        status_names = [item.status for item in distribution]
        assert status_names == list(FIXED_STATUSES), "狀態順序應符合 FIXED_STATUSES"

        # 驗證每個狀態的 count 都是 1
        for item in distribution:
            assert item.count == 1, f"狀態 {item.status} 的 count 應為 1"

    def test_status_distribution_correct_order(self, processor):
        """
        測試狀態順序正確
        順序：Backlog → Evaluated → To Do → In Progress → Waiting → Ready to Verify → Done → Invalid → Routine
        對應 TC-CHART-002
        """
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="1",
                  status="Done"),
            Issue(key="PROJ-002", issue_type="Story", project="PROJ", summary="2",
                  status="Backlog"),
            Issue(key="PROJ-003", issue_type="Story", project="PROJ", summary="3",
                  status="In Progress"),
        ]

        distribution = processor.calculate_status_distribution(issues, sprint_filter="All")

        # 驗證順序與 FIXED_STATUSES 一致
        expected_order = [
            "Backlog", "Evaluated", "To Do", "In Progress", "Waiting",
            "Ready to Verify", "Done", "Invalid", "Routine"
        ]
        actual_order = [item.status for item in distribution]
        assert actual_order == expected_order, "狀態順序應按固定順序排列"

    def test_status_distribution_percentage_calculation(self, processor):
        """
        測試百分比計算準確性
        對應 TC-CHART-003
        """
        # 總計 27 筆 Issue，其中 5 筆為 "In Progress"
        # 預期百分比：5/27 ≈ 18.52%
        issues = []

        # 5 筆 In Progress
        for i in range(5):
            issues.append(Issue(key=f"PROJ-{i:03d}", issue_type="Story", project="PROJ",
                              summary=f"InProgress {i}", status="In Progress"))

        # 其他 22 筆分散在其他狀態
        for i in range(5, 27):
            status = ["Backlog", "To Do", "Done", "Waiting", "Ready to Verify"][i % 5]
            issues.append(Issue(key=f"PROJ-{i:03d}", issue_type="Story", project="PROJ",
                              summary=f"Other {i}", status=status))

        distribution = processor.calculate_status_distribution(issues, sprint_filter="All")

        # 找到 In Progress 的分布項目
        in_progress_item = next(item for item in distribution if item.status == "In Progress")

        assert in_progress_item.count == 5
        expected_percentage = round(5 / 27 * 100, 2)  # ≈ 18.52
        assert in_progress_item.percentage == expected_percentage

    def test_status_distribution_empty_dataset(self, processor):
        """
        測試空資料集
        對應 TC-CHART-005
        """
        issues = []

        distribution = processor.calculate_status_distribution(issues, sprint_filter="All")

        # 應返回 9 個狀態，但所有 count 和 percentage 都是 0
        assert len(distribution) == 9
        for item in distribution:
            assert item.count == 0, f"狀態 {item.status} 的 count 應為 0"
            assert item.percentage == 0.0, f"狀態 {item.status} 的 percentage 應為 0"

    def test_status_distribution_excludes_invalid_statuses(self, processor):
        """
        測試無效 Status 值被排除在分布外
        對應 TC-CHART-005 和 TC-EDGE-002
        """
        issues = [
            # 有效狀態
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Valid 1",
                  status="Done"),
            Issue(key="PROJ-002", issue_type="Story", project="PROJ", summary="Valid 2",
                  status="In Progress"),
            Issue(key="PROJ-003", issue_type="Story", project="PROJ", summary="Valid 3",
                  status="To Do"),
            # 無效狀態（不在 9 個固定狀態中）
            Issue(key="PROJ-004", issue_type="Story", project="PROJ", summary="Invalid 1",
                  status="Unknown"),
            Issue(key="PROJ-005", issue_type="Story", project="PROJ", summary="Invalid 2",
                  status="Testing"),
            Issue(key="PROJ-006", issue_type="Story", project="PROJ", summary="Invalid 3",
                  status="Archived"),
        ]

        distribution = processor.calculate_status_distribution(issues, sprint_filter="All")

        # 總 Issue 數應為 6（包含無效狀態的記錄）
        total_counted = sum(item.count for item in distribution)
        assert total_counted == 3, "只有有效狀態的 Issue 應計入分布統計"

        # 驗證無效狀態不出現在分布中
        status_names = [item.status for item in distribution]
        assert "Unknown" not in status_names
        assert "Testing" not in status_names
        assert "Archived" not in status_names

    def test_status_distribution_with_sprint_filter(self, processor):
        """
        測試 Sprint 篩選功能
        對應 TC-FILTER-006
        """
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Sprint A Done",
                  status="Done", sprint="Sprint A"),
            Issue(key="PROJ-002", issue_type="Story", project="PROJ", summary="Sprint A InProgress",
                  status="In Progress", sprint="Sprint A"),
            Issue(key="PROJ-003", issue_type="Story", project="PROJ", summary="Sprint B Done",
                  status="Done", sprint="Sprint B"),
            Issue(key="PROJ-004", issue_type="Story", project="PROJ", summary="Sprint B ToDo",
                  status="To Do", sprint="Sprint B"),
        ]

        # 篩選 Sprint A
        distribution = processor.calculate_status_distribution(issues, sprint_filter="Sprint A")

        # 應只統計 Sprint A 的 Issue
        total_counted = sum(item.count for item in distribution)
        assert total_counted == 2, "應只統計 Sprint A 的 Issue"

        # 找到 Done 和 In Progress 的計數
        done_item = next(item for item in distribution if item.status == "Done")
        in_progress_item = next(item for item in distribution if item.status == "In Progress")

        assert done_item.count == 1
        assert in_progress_item.count == 1

    def test_status_distribution_no_sprints_filter(self, processor):
        """
        測試 "No Sprints" 篩選
        對應 TC-FILTER-007
        """
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="With Sprint",
                  status="Done", sprint="Sprint A"),
            Issue(key="PROJ-002", issue_type="Story", project="PROJ", summary="No Sprint 1",
                  status="Done", sprint=None),
            Issue(key="PROJ-003", issue_type="Story", project="PROJ", summary="No Sprint 2",
                  status="In Progress", sprint=""),
        ]

        distribution = processor.calculate_status_distribution(issues, sprint_filter="No Sprints")

        # 應只統計無 Sprint 的 Issue
        total_counted = sum(item.count for item in distribution)
        assert total_counted == 2, "應只統計無 Sprint 的 Issue"

    def test_status_distribution_multiple_same_status(self, processor):
        """測試同一狀態有多筆 Issue"""
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="InProgress 1",
                  status="In Progress"),
            Issue(key="PROJ-002", issue_type="Story", project="PROJ", summary="InProgress 2",
                  status="In Progress"),
            Issue(key="PROJ-003", issue_type="Story", project="PROJ", summary="InProgress 3",
                  status="In Progress"),
            Issue(key="PROJ-004", issue_type="Story", project="PROJ", summary="InProgress 4",
                  status="In Progress"),
            Issue(key="PROJ-005", issue_type="Story", project="PROJ", summary="InProgress 5",
                  status="In Progress"),
        ]

        distribution = processor.calculate_status_distribution(issues, sprint_filter="All")

        # 找到 In Progress 的分布項目
        in_progress_item = next(item for item in distribution if item.status == "In Progress")

        assert in_progress_item.count == 5
        assert in_progress_item.percentage == 100.0  # 所有 Issue 都是 In Progress

    def test_status_distribution_all_statuses_with_counts(self, processor):
        """
        測試符合 testcases.md TC-CHART-002 的完整場景
        包含所有 9 種狀態且有不同數量
        """
        # 按照 testcases.md 的資料集
        issues = []

        # Backlog: 2
        for i in range(2):
            issues.append(Issue(key=f"BL-{i}", issue_type="Story", project="PROJ",
                              summary=f"Backlog {i}", status="Backlog"))
        # Evaluated: 1
        issues.append(Issue(key="EV-1", issue_type="Story", project="PROJ",
                          summary="Evaluated", status="Evaluated"))
        # To Do: 3
        for i in range(3):
            issues.append(Issue(key=f"TD-{i}", issue_type="Story", project="PROJ",
                              summary=f"ToDo {i}", status="To Do"))
        # In Progress: 5
        for i in range(5):
            issues.append(Issue(key=f"IP-{i}", issue_type="Story", project="PROJ",
                              summary=f"InProgress {i}", status="In Progress"))
        # Waiting: 2
        for i in range(2):
            issues.append(Issue(key=f"WT-{i}", issue_type="Story", project="PROJ",
                              summary=f"Waiting {i}", status="Waiting"))
        # Ready to Verify: 4
        for i in range(4):
            issues.append(Issue(key=f"RV-{i}", issue_type="Story", project="PROJ",
                              summary=f"ReadyToVerify {i}", status="Ready to Verify"))
        # Done: 8
        for i in range(8):
            issues.append(Issue(key=f"DN-{i}", issue_type="Story", project="PROJ",
                              summary=f"Done {i}", status="Done"))
        # Invalid: 1
        issues.append(Issue(key="IV-1", issue_type="Story", project="PROJ",
                          summary="Invalid", status="Invalid"))
        # Routine: 1
        issues.append(Issue(key="RT-1", issue_type="Story", project="PROJ",
                          summary="Routine", status="Routine"))

        distribution = processor.calculate_status_distribution(issues, sprint_filter="All")

        # 總計 27 筆
        total = sum(item.count for item in distribution)
        assert total == 27

        # 驗證每個狀態的計數
        expected_counts = {
            "Backlog": 2,
            "Evaluated": 1,
            "To Do": 3,
            "In Progress": 5,
            "Waiting": 2,
            "Ready to Verify": 4,
            "Done": 8,
            "Invalid": 1,
            "Routine": 1,
        }

        for item in distribution:
            assert item.count == expected_counts[item.status], \
                f"狀態 {item.status} 的 count 應為 {expected_counts[item.status]}"
            expected_pct = round(expected_counts[item.status] / 27 * 100, 2)
            assert item.percentage == expected_pct, \
                f"狀態 {item.status} 的 percentage 應為 {expected_pct}"

    def test_status_distribution_zero_count_statuses_still_present(self, processor):
        """測試某些狀態計數為 0 時仍出現在分布中"""
        # 只有 Done 和 In Progress，其他狀態計數為 0
        issues = [
            Issue(key="PROJ-001", issue_type="Story", project="PROJ", summary="Done",
                  status="Done"),
            Issue(key="PROJ-002", issue_type="Story", project="PROJ", summary="InProgress",
                  status="In Progress"),
        ]

        distribution = processor.calculate_status_distribution(issues, sprint_filter="All")

        # 應返回 9 個狀態
        assert len(distribution) == 9

        # 檢查 count 為 0 的狀態
        zero_count_statuses = [item for item in distribution if item.count == 0]
        assert len(zero_count_statuses) == 7, "應有 7 個狀態的 count 為 0"

        # 檢查非零計數的狀態
        done_item = next(item for item in distribution if item.status == "Done")
        in_progress_item = next(item for item in distribution if item.status == "In Progress")

        assert done_item.count == 1
        assert in_progress_item.count == 1
