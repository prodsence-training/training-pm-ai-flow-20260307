"""
應用程式配置
"""
import os
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()


class Settings:
    """應用程式設定"""

    # Google Sheets 配置
    GOOGLE_SHEETS_SHEET_ID: str = os.getenv(
        'GoogleSheets__SheetId', '1RmJjghgiV3XWLl2BaxT-md8CP3pqb1Wuk-EhFoqp1VM'
    )
    GOOGLE_SHEETS_RAW_DATA_SHEET: str = os.getenv('GoogleSheets__RawDataSheet', 'rawData')
    GOOGLE_SHEETS_SPRINT_SHEET: str = os.getenv(
        'GoogleSheets__SprintSheet', 'GetJiraSprintValues'
    )

    # 快取配置
    CACHE_DURATION: int = int(os.getenv('CacheDuration', '300'))  # 5 分鐘

    # 伺服器配置
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')


settings = Settings()
