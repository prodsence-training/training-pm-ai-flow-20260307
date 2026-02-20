"""
Data Processor Service
處理 Google Sheets 原始資料並計算指標
"""
from typing import List, Dict
from ..models.issue import Issue
from ..models.sprint import Sprint
from ..models.metric import DashboardMetrics, StatusDistribution, FIXED_STATUSES


class DataProcessor:
    """資料處理服務"""

    def parse_issues(self, raw_data: List[List[str]]) -> List[Issue]:
        """
        解析原始 CSV 資料為 Issue 物件列表

        Args:
            raw_data: CSV 資料列表（每列是字串列表）

        Returns:
            List[Issue]: Issue 物件列表
        """
        issues = []
        for row in raw_data:
            if not row or len(row) == 0:
                continue  # 跳過空列

            try:
                issue = Issue.from_row(row)
                issues.append(issue)
            except Exception as e:
                print(f"Error parsing issue row: {e}")
                continue

        return issues

    def parse_sprints(self, sprint_data: List[List[str]]) -> List[Sprint]:
        """
        解析 Sprint 資料為 Sprint 物件列表

        Args:
            sprint_data: CSV 資料列表

        Returns:
            List[Sprint]: Sprint 物件列表
        """
        sprints = []
        for row in sprint_data:
            if not row or len(row) == 0:
                continue

            try:
                sprint = Sprint.from_row(row)
                sprints.append(sprint)
            except Exception as e:
                print(f"Error parsing sprint row: {e}")
                continue

        return sprints

    def calculate_metrics(
        self, issues: List[Issue], sprint_filter: str = "All"
    ) -> DashboardMetrics:
        """
        計算儀表板指標

        Args:
            issues: Issue 物件列表
            sprint_filter: Sprint 篩選條件 ("All", "No Sprints", 或特定 Sprint 名稱)

        Returns:
            DashboardMetrics: 計算後的指標
        """
        # 應用 Sprint 篩選
        filtered_issues = self.filter_issues_by_sprint(issues, sprint_filter)

        # 指標 1: Total Issue Count（包含所有記錄，即使 Status 無效）
        total_issue_count = len(filtered_issues)

        # 指標 2: Total Story Points
        total_story_points = sum(issue.story_points for issue in filtered_issues)

        # 指標 3: Total Done Item Count
        done_issues = [issue for issue in filtered_issues if issue.is_done()]
        total_done_item_count = len(done_issues)

        # 指標 4: Done Story Points
        done_story_points = sum(issue.story_points for issue in done_issues)

        return DashboardMetrics(
            total_issue_count=total_issue_count,
            total_story_points=round(total_story_points, 2),
            total_done_item_count=total_done_item_count,
            done_story_points=round(done_story_points, 2),
        )

    def calculate_status_distribution(
        self, issues: List[Issue], sprint_filter: str = "All"
    ) -> List[StatusDistribution]:
        """
        計算狀態分布（只顯示 9 個固定狀態）

        Args:
            issues: Issue 物件列表
            sprint_filter: Sprint 篩選條件

        Returns:
            List[StatusDistribution]: 狀態分布列表（按 FIXED_STATUSES 順序）
        """
        # 應用 Sprint 篩選
        filtered_issues = self.filter_issues_by_sprint(issues, sprint_filter)

        total_issues = len(filtered_issues)
        distribution = []

        # 統計每個固定狀態的數量
        for status in FIXED_STATUSES:
            count = sum(1 for issue in filtered_issues if issue.status == status)
            percentage = (count / total_issues * 100) if total_issues > 0 else 0

            distribution.append(
                StatusDistribution(
                    status=status, count=count, percentage=round(percentage, 2)
                )
            )

        return distribution

    def filter_issues_by_sprint(
        self, issues: List[Issue], sprint_name: str
    ) -> List[Issue]:
        """
        按 Sprint Name 篩選 Issue

        Args:
            issues: Issue 物件列表
            sprint_name: Sprint 名稱 ("All", "No Sprints", 或特定名稱)

        Returns:
            List[Issue]: 篩選後的 Issue 列表
        """
        if sprint_name == "All":
            return issues
        elif sprint_name == "No Sprints":
            # 篩選空 Sprint 欄位
            return [issue for issue in issues if not issue.sprint or issue.sprint.strip() == '']
        else:
            # 篩選指定 Sprint Name
            # 處理重複 Sprint Name 的情況（格式：「Sprint Name (Sprint ID)」）
            # 需要提取括號前的名稱
            import re
            match = re.match(r'^(.+)\s+\((\d+)\)$', sprint_name)
            if match:
                actual_sprint_name = match.group(1)
            else:
                actual_sprint_name = sprint_name

            return [issue for issue in issues if issue.sprint == actual_sprint_name]

    def generate_sprint_options(self, sprints: List[Sprint]) -> List[str]:
        """
        生成 Sprint 篩選選項（處理重複名稱）

        Args:
            sprints: Sprint 物件列表

        Returns:
            List[str]: Sprint 選項列表（包含 "All" 和 "No Sprints"）
        """
        options = ['All']

        # 建立 Sprint Name 到 Sprint ID 的映射
        name_to_ids: Dict[str, List[int]] = {}
        for sprint in sprints:
            if sprint.sprint_name:
                if sprint.sprint_name not in name_to_ids:
                    name_to_ids[sprint.sprint_name] = []
                name_to_ids[sprint.sprint_name].append(sprint.sprint_id)

        # 生成選項（排序）
        sorted_names = sorted(name_to_ids.keys())
        for name in sorted_names:
            ids = name_to_ids[name]
            if len(ids) > 1:
                # 有重複：為每個 ID 生成選項
                for sprint_id in sorted(ids):
                    options.append(f"{name} ({sprint_id})")
            else:
                # 無重複：只顯示名稱
                options.append(name)

        options.append('No Sprints')

        return options
