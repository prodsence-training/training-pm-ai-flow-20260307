"""
Pytest configuration and shared fixtures for all tests
"""
import pytest
from fastapi.testclient import TestClient
from typing import List
from unittest.mock import AsyncMock

from src.main import app
from src.services.google_sheets_service import GoogleSheetsService
from src.services.cache_service import CacheService
from src.services.data_processor import DataProcessor
from src.api.dependencies import (
    get_google_sheets_service,
    get_cache_service,
    get_data_processor,
)
from tests.fixtures.sample_raw_data import (
    SAMPLE_RAW_DATA_BASIC,
    SAMPLE_RAW_DATA_ALL_STATUSES,
    SAMPLE_RAW_DATA_INVALID_STATUS,
    SAMPLE_RAW_DATA_NON_NUMERIC_POINTS,
    SAMPLE_RAW_DATA_EMPTY,
)
from tests.fixtures.sample_sprint_data import (
    SAMPLE_SPRINT_DATA_BASIC,
    SAMPLE_SPRINT_DATA_DUPLICATES,
    SAMPLE_SPRINT_DATA_EMPTY,
)


class MockGoogleSheetsService:
    """Mock Google Sheets Service for testing"""

    def __init__(self):
        self.raw_data_fixture = SAMPLE_RAW_DATA_BASIC
        self.sprint_data_fixture = SAMPLE_SPRINT_DATA_BASIC

    async def fetch_raw_data(self) -> List[List[str]]:
        """返回模擬的 rawData"""
        # 跳過 header row
        return self.raw_data_fixture[1:]

    async def fetch_sprint_data(self) -> List[List[str]]:
        """返回模擬的 Sprint 資料"""
        # 跳過 header row
        return self.sprint_data_fixture[1:]

    def set_raw_data_fixture(self, fixture: List[List[str]]):
        """設置 raw data fixture"""
        self.raw_data_fixture = fixture

    def set_sprint_data_fixture(self, fixture: List[List[str]]):
        """設置 sprint data fixture"""
        self.sprint_data_fixture = fixture


@pytest.fixture
def mock_sheets_service():
    """提供 Mock Google Sheets Service"""
    return MockGoogleSheetsService()


@pytest.fixture
def mock_cache_service():
    """提供 Mock Cache Service（無快取）"""
    cache = CacheService()
    # 清空快取
    cache.cache.clear()
    return cache


@pytest.fixture
def data_processor():
    """提供 DataProcessor 實例"""
    return DataProcessor()


@pytest.fixture
def test_client(mock_sheets_service, mock_cache_service, data_processor):
    """
    提供 FastAPI TestClient，並注入 mock dependencies
    """

    # Override dependencies
    app.dependency_overrides[get_google_sheets_service] = lambda: mock_sheets_service
    app.dependency_overrides[get_cache_service] = lambda: mock_cache_service
    app.dependency_overrides[get_data_processor] = lambda: data_processor

    client = TestClient(app)

    yield client

    # 清理 dependency overrides
    app.dependency_overrides.clear()
