"""
Google Sheets CSV API Service
使用公開 CSV 匯出 URL 下載 Google Sheets 資料
"""
import httpx
import csv
from io import StringIO
from typing import List, Optional
import os


class GoogleSheetsService:
    """Google Sheets CSV API 服務"""

    BASE_URL = "https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    def __init__(self):
        self.sheet_id = os.getenv('GoogleSheets__SheetId', '1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM')
        self.raw_data_sheet = os.getenv('GoogleSheets__RawDataSheet', 'rawData')
        self.sprint_sheet = os.getenv('GoogleSheets__SprintSheet', 'GetJiraSprintValues')

        # GID mapping (需要從 Google Sheets URL 取得)
        # 預設假設 rawData 在第一個 sheet (gid=0)
        self.gid_mapping = {
            'rawData': 0,
            'GetJiraSprintValues': 1
        }

    async def fetch_raw_data(self) -> List[List[str]]:
        """
        下載 rawData 工作表的 CSV 資料

        Returns:
            List[List[str]]: CSV 資料的列表（每列是一個字串列表）

        Raises:
            httpx.HTTPError: 連接失敗時拋出
        """
        gid = self.gid_mapping.get(self.raw_data_sheet, 0)
        url = self.BASE_URL.format(sheet_id=self.sheet_id, gid=gid)

        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()
                csv_content = response.text

                # 解析 CSV
                return self._parse_csv(csv_content)
        except httpx.HTTPError as e:
            print(f"Error fetching Google Sheets data: {e}")
            raise

    async def fetch_sprint_data(self) -> List[List[str]]:
        """
        提取 Sprint 資料（從 rawData 中提取唯一的 Sprint 值）

        Returns:
            List[List[str]]: Sprint 資料的列表

        Raises:
            httpx.HTTPError: 連接失敗時拋出
        """
        try:
            # 從 rawData 中取得所有資料
            raw_data = await self.fetch_raw_data()

            # Sprint 欄位在索引 6（從 0 開始計數）
            sprint_index = 6

            # 提取唯一的 Sprint 值
            sprint_set = set()
            for row in raw_data:
                if len(row) > sprint_index and row[sprint_index].strip():
                    sprint_set.add(row[sprint_index].strip())

            # 將 Sprint 值轉換為列表，每個 Sprint 一列
            sprint_list = [[sprint] for sprint in sorted(sprint_set)]

            return sprint_list
        except httpx.HTTPError as e:
            print(f"Error fetching sprint data: {e}")
            raise

    def _parse_csv(self, csv_content: str) -> List[List[str]]:
        """
        解析 CSV 字串為列表

        Args:
            csv_content: CSV 字串內容

        Returns:
            List[List[str]]: 解析後的 CSV 資料（不含標題列）
        """
        reader = csv.reader(StringIO(csv_content))
        rows = list(reader)

        # 移除標題列（第一列）
        if len(rows) > 0:
            rows = rows[1:]

        return rows
