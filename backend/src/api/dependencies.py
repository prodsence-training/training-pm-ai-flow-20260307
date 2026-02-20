"""
FastAPI 依賴注入
提供 Service 實例給 route handlers
"""
from ..services.google_sheets_service import GoogleSheetsService
from ..services.cache_service import CacheService
from ..services.data_processor import DataProcessor

# 全域單例實例
_google_sheets_service = None
_cache_service = None
_data_processor = None


def get_google_sheets_service() -> GoogleSheetsService:
    """取得 GoogleSheetsService 單例"""
    global _google_sheets_service
    if _google_sheets_service is None:
        _google_sheets_service = GoogleSheetsService()
    return _google_sheets_service


def get_cache_service() -> CacheService:
    """取得 CacheService 單例"""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service


def get_data_processor() -> DataProcessor:
    """取得 DataProcessor 實例"""
    global _data_processor
    if _data_processor is None:
        _data_processor = DataProcessor()
    return _data_processor
