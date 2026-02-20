"""
FastAPI Routes
定義所有 API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from datetime import datetime

from .dependencies import (
    get_google_sheets_service,
    get_cache_service,
    get_data_processor,
)
from ..services.google_sheets_service import GoogleSheetsService
from ..services.cache_service import CacheService
from ..services.data_processor import DataProcessor
from ..models.metric import DashboardMetrics, StatusDistribution
from ..utils import log_error, log_info

router = APIRouter()


@router.get("/dashboard/metrics")
async def get_metrics(
    sprint: str = Query("All", description="Sprint 篩選條件"),
    sheets_service: GoogleSheetsService = Depends(get_google_sheets_service),
    cache_service: CacheService = Depends(get_cache_service),
    data_processor: DataProcessor = Depends(get_data_processor),
) -> Dict[str, Any]:
    """
    取得儀表板指標（4 個統計卡片）

    Args:
        sprint: Sprint 篩選條件（"All", "No Sprints", 或特定 Sprint 名稱）

    Returns:
        包含 4 個指標的 JSON 回應
    """
    cache_key = f"metrics:{sprint}"

    # 檢查快取
    cached_data = cache_service.get(cache_key)
    if cached_data:
        return {
            **cached_data,
            "cacheHit": True,
            "timestamp": datetime.utcnow().isoformat(),
        }

    try:
        # 從 Google Sheets 取得原始資料
        raw_data = await sheets_service.fetch_raw_data()

        # 解析為 Issue 物件
        issues = data_processor.parse_issues(raw_data)

        # 計算指標
        metrics = data_processor.calculate_metrics(issues, sprint)

        # 轉換為字典
        result = {
            "totalIssueCount": metrics.total_issue_count,
            "totalStoryPoints": metrics.total_story_points,
            "totalDoneItemCount": metrics.total_done_item_count,
            "doneStoryPoints": metrics.done_story_points,
            "timestamp": datetime.utcnow().isoformat(),
            "cacheHit": False,
        }

        # 儲存到快取
        cache_service.set(cache_key, result)

        return result

    except Exception as e:
        log_error("GET /dashboard/metrics", e, {"sprint": sprint})
        raise HTTPException(status_code=500, detail=f"Failed to calculate metrics: {str(e)}")


@router.get("/dashboard/status-distribution")
async def get_status_distribution(
    sprint: str = Query("All", description="Sprint 篩選條件"),
    sheets_service: GoogleSheetsService = Depends(get_google_sheets_service),
    cache_service: CacheService = Depends(get_cache_service),
    data_processor: DataProcessor = Depends(get_data_processor),
) -> Dict[str, Any]:
    """
    取得狀態分布資料（9 個固定狀態）

    Args:
        sprint: Sprint 篩選條件

    Returns:
        包含狀態分布的 JSON 回應
    """
    cache_key = f"status-distribution:{sprint}"

    # 檢查快取
    cached_data = cache_service.get(cache_key)
    if cached_data:
        return {
            **cached_data,
            "cacheHit": True,
            "timestamp": datetime.utcnow().isoformat(),
        }

    try:
        # 從 Google Sheets 取得原始資料
        raw_data = await sheets_service.fetch_raw_data()

        # 解析為 Issue 物件
        issues = data_processor.parse_issues(raw_data)

        # 計算狀態分布
        distribution = data_processor.calculate_status_distribution(issues, sprint)

        # 轉換為字典列表
        distribution_data = [
            {
                "status": item.status,
                "count": item.count,
                "percentage": item.percentage,
            }
            for item in distribution
        ]

        result = {
            "distribution": distribution_data,
            "totalIssueCount": len(data_processor.filter_issues_by_sprint(issues, sprint)),
            "timestamp": datetime.utcnow().isoformat(),
            "cacheHit": False,
        }

        # 儲存到快取
        cache_service.set(cache_key, result)

        return result

    except Exception as e:
        log_error("GET /dashboard/status-distribution", e, {"sprint": sprint})
        raise HTTPException(
            status_code=500, detail=f"Failed to calculate status distribution: {str(e)}"
        )


@router.get("/sprints")
async def get_sprints(
    sheets_service: GoogleSheetsService = Depends(get_google_sheets_service),
    cache_service: CacheService = Depends(get_cache_service),
    data_processor: DataProcessor = Depends(get_data_processor),
) -> Dict[str, Any]:
    """
    取得 Sprint 篩選選項

    Returns:
        包含 Sprint 選項的 JSON 回應
    """
    cache_key = "sprints:list"

    # 檢查快取
    cached_data = cache_service.get(cache_key)
    if cached_data:
        return {
            **cached_data,
            "cacheHit": True,
            "timestamp": datetime.utcnow().isoformat(),
        }

    try:
        # 從 Google Sheets 取得 Sprint 資料（唯一的 Sprint 名稱列表）
        sprint_data = await sheets_service.fetch_sprint_data()

        # 提取 Sprint 名稱列表（sprint_data 是 [[name], [name], ...]）
        sprint_names = [row[0] for row in sprint_data if row and row[0]]

        # 生成選項（簡單版本，不需要處理重複，因為已經過濾）
        options = ["All"] + sorted(sprint_names) + ["No Sprints"]

        result = {
            "options": options,
            "totalSprints": len(sprint_names),
            "timestamp": datetime.utcnow().isoformat(),
            "cacheHit": False,
        }

        # 儲存到快取
        cache_service.set(cache_key, result)

        return result

    except Exception as e:
        log_error("GET /api/sprints", e, {})
        raise HTTPException(status_code=500, detail=f"Failed to fetch sprints: {str(e)}")
