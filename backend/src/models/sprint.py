"""
Sprint 資料模型
對應 Google Sheets GetJiraSprintValues 表的 9 個欄位 (A:I)
"""
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class SprintState(str, Enum):
    """Sprint 生命週期狀態"""
    FUTURE = 'future'  # 未來計劃
    ACTIVE = 'active'  # 進行中
    CLOSED = 'closed'  # 已結束


@dataclass
class Sprint:
    """表示 GetJiraSprintValues 工作表的一列"""

    board_id: int  # A: 看板 ID
    board_name: str  # B: 看板名稱
    sprint_name: str  # C: Sprint 名稱（用於篩選）
    sprint_id: int  # D: Sprint ID
    state: SprintState  # E: 當前狀態
    start_date: str  # F: 開始日期
    end_date: str  # G: 結束日期
    complete_date: Optional[str] = None  # H: 完成日期
    goal: str = ""  # I: Sprint 目標

    @staticmethod
    def from_row(row: list) -> 'Sprint':
        """從 CSV 列陣列轉換為 Sprint 物件"""
        # 確保 row 至少有 9 個元素
        if len(row) < 9:
            row = row + [''] * (9 - len(row))

        try:
            board_id = int(row[0]) if row[0] else 0
        except (ValueError, TypeError):
            board_id = 0

        try:
            sprint_id = int(row[3]) if row[3] else 0
        except (ValueError, TypeError):
            sprint_id = 0

        # 解析 state
        state_value = row[4].lower() if row[4] else 'future'
        if state_value in ['future', 'active', 'closed']:
            state = SprintState(state_value)
        else:
            state = SprintState.FUTURE

        return Sprint(
            board_id=board_id,
            board_name=row[1] or '',
            sprint_name=row[2] or '',
            sprint_id=sprint_id,
            state=state,
            start_date=row[5] or '',
            end_date=row[6] or '',
            complete_date=row[7] if row[7] else None,
            goal=row[8] or '',
        )
