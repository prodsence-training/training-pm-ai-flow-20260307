"""
Issue 資料模型
對應 Google Sheets rawData 表的 23 個欄位 (A:W, 索引 0-22)
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Issue:
    """
    Issue 表示 Jira 系統中的單一工作項目
    資料來源: rawData 表的一列（索引 0-22）
    """

    # 核心識別 (索引 0-4)
    key: str  # 0: Issue 唯一識別碼
    issue_type: str  # 1: 類型
    project: str  # 2: 專案代碼
    summary: str  # 3: Issue 標題
    parent: Optional[str] = None  # 4: 父級 Issue Key

    # 工作流程 (索引 5-7)
    status: str = ""  # 5: 當前狀態
    sprint: Optional[str] = None  # 6: Sprint 名稱
    due_date: Optional[str] = None  # 7: 預計完成日期

    # 優先級與緊急度 (索引 8-9)
    priority: str = ""  # 8: 優先級等級
    urgency: str = ""  # 9: 緊急程度

    # 估算欄位 (索引 10-15)
    t_size: str = ""  # 10: T-Shirt 大小
    confidence: str = ""  # 11: 估算信心程度
    clients: str = ""  # 12: 相關客戶
    task_tags: str = ""  # 13: 任務標籤
    business_points: float = 0.0  # 14: 商業價值點數
    story_points: float = 0.0  # 15: 故事點數

    # 狀態追蹤 (索引 16-18)
    status_category: str = ""  # 16: 簡化狀態分類
    status_category_changed: Optional[str] = None  # 17: 狀態變更時間
    time_spent: int = 0  # 18: 實際花費時間（秒）

    # 時間軸 (索引 19-22)
    created: str = ""  # 19: Issue 建立時間
    updated: str = ""  # 20: 最後更新時間
    resolved: Optional[str] = None  # 21: 解決時間
    project_name: str = ""  # 22: Jira 專案識別名稱

    @staticmethod
    def from_row(row: list) -> 'Issue':
        """從 CSV 列陣列轉換為 Issue 物件"""
        # 確保 row 至少有 23 個元素
        if len(row) < 23:
            row = row + [''] * (23 - len(row))

        try:
            business_points = float(row[14]) if row[14] else 0.0
        except (ValueError, TypeError):
            business_points = 0.0

        try:
            story_points = float(row[15]) if row[15] else 0.0
        except (ValueError, TypeError):
            story_points = 0.0  # 非數值視為 0 (FR-032)

        try:
            time_spent = int(row[18]) if row[18] else 0
        except (ValueError, TypeError):
            time_spent = 0

        return Issue(
            key=row[0] or '',
            issue_type=row[1] or '',
            project=row[2] or '',
            summary=row[3] or '',
            parent=row[4] if row[4] else None,
            status=row[5] or '',
            sprint=row[6] if row[6] else None,
            due_date=row[7] if row[7] else None,
            priority=row[8] or '',
            urgency=row[9] or '',
            t_size=row[10] or '',
            confidence=row[11] or '',
            clients=row[12] or '',
            task_tags=row[13] or '',
            business_points=business_points,
            story_points=story_points,
            status_category=row[16] or '',
            status_category_changed=row[17] if row[17] else None,
            time_spent=time_spent,
            created=row[19] or '',
            updated=row[20] or '',
            resolved=row[21] if row[21] else None,
            project_name=row[22] or '',
        )

    def is_done(self) -> bool:
        """檢查 Issue 是否完成"""
        return self.status == 'Done'

    def has_valid_status(self) -> bool:
        """檢查 Status 是否在 9 個預定義值內"""
        valid_statuses = {
            'Backlog', 'Evaluated', 'To Do', 'In Progress',
            'Waiting', 'Ready to Verify', 'Done', 'Invalid', 'Routine'
        }
        return self.status in valid_statuses
