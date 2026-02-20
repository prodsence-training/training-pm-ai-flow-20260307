"""
Logging Configuration
設定後端應用的日誌系統
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

# 建立 logs 目錄
logs_dir = Path(__file__).parent.parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

# 設定日誌格式
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# 建立 logger
logger = logging.getLogger("jira_dashboard")

# 設定日誌等級
log_level = logging.INFO

# 建立 console handler（輸出到標準輸出）
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(log_level)
console_formatter = logging.Formatter(log_format, datefmt=date_format)
console_handler.setFormatter(console_formatter)

# 建立 file handler（輸出到檔案）
log_file = logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(log_level)
file_formatter = logging.Formatter(log_format, datefmt=date_format)
file_handler.setFormatter(file_formatter)

# 新增 handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(log_level)


def log_error(context: str, error: Exception, details: dict = None) -> None:
    """
    記錄錯誤

    Args:
        context: 錯誤上下文（例如 "GoogleSheetsService.fetch_raw_data"）
        error: 例外物件
        details: 額外詳細資訊字典
    """
    message = f"[{context}] {str(error)}"
    if details:
        message += f" | Details: {details}"

    logger.error(message, exc_info=True)


def log_warning(context: str, message: str, details: dict = None) -> None:
    """
    記錄警告
    """
    msg = f"[{context}] {message}"
    if details:
        msg += f" | Details: {details}"

    logger.warning(msg)


def log_info(context: str, message: str, details: dict = None) -> None:
    """
    記錄資訊
    """
    msg = f"[{context}] {message}"
    if details:
        msg += f" | Details: {details}"

    logger.info(msg)
