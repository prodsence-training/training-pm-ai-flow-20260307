"""
In-Memory Cache Service
提供簡單的 TTL (Time-To-Live) 快取機制
"""
from datetime import datetime, timedelta
from typing import Optional, Any, Dict, Tuple
import os


class CacheService:
    """In-memory TTL 快取服務"""

    def __init__(self, ttl_seconds: int = 300):
        """
        初始化快取服務

        Args:
            ttl_seconds: 快取過期時間（秒），預設 5 分鐘
        """
        self.ttl_seconds = int(os.getenv('CacheDuration', ttl_seconds))
        self.cache: Dict[str, Tuple[Any, datetime]] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        取得快取值

        Args:
            key: 快取鍵名

        Returns:
            快取值，如果不存在或已過期則返回 None
        """
        if key not in self.cache:
            return None

        data, timestamp = self.cache[key]

        # 檢查是否過期
        if datetime.utcnow() - timestamp > timedelta(seconds=self.ttl_seconds):
            # 移除過期的快取
            del self.cache[key]
            return None

        return data

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """
        設置快取值

        Args:
            key: 快取鍵名
            value: 快取值
            ttl_seconds: 自訂 TTL（可選），如不指定則使用預設值
        """
        self.cache[key] = (value, datetime.utcnow())

    def clear(self, key: Optional[str] = None) -> None:
        """
        清除快取

        Args:
            key: 要清除的快取鍵名，如為 None 則清除所有快取
        """
        if key:
            self.cache.pop(key, None)
        else:
            self.cache.clear()

    def has_key(self, key: str) -> bool:
        """
        檢查快取鍵是否存在且未過期

        Args:
            key: 快取鍵名

        Returns:
            True 如果存在且未過期，否則 False
        """
        return self.get(key) is not None
