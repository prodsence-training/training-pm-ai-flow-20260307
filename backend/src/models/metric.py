"""
Metric 資料模型
包含 DashboardMetrics 和 StatusDistribution
"""
from dataclasses import dataclass
from typing import List


@dataclass
class DashboardMetrics:
    """表示儀表板四個統計卡片的數據"""

    total_issue_count: int  # 指標 1: 總 Issue 數（包含所有記錄）
    total_story_points: float  # 指標 2: 總故事點數（支援小數）
    total_done_item_count: int  # 指標 3: 已完成 Issue 數
    done_story_points: float  # 指標 4: 已完成故事點數


@dataclass
class StatusDistribution:
    """表示 Issue 在各狀態的分布情況"""

    status: str  # 狀態名稱
    count: int  # Issue 數量
    percentage: float  # 佔比百分比


# 固定狀態順序（不變）
FIXED_STATUSES = [
    'Backlog',
    'Evaluated',
    'To Do',
    'In Progress',
    'Waiting',
    'Ready to Verify',
    'Done',
    'Invalid',
    'Routine',
]
