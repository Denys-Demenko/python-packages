import aiohttp

from typing import Optional, Dict, Any
from packages.throttling.throttle_service import ThrottleService


class HttpThrottledService:
    def __init__(self, base_url: str, headers: dict[str, str], throttler: ThrottleService):
        self._base_url = base_url.rstrip('/')
        self._headers = headers
        self._throttler = throttler

    async def get_async(self, rel_url: str, query: Optional[Dict[str, Any]] = None) -> Optional[dict]:
        """GET implementation"""
        if not await self._throttler.throttle_async():
            return None

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"{self._base_url}/{rel_url.lstrip('/')}",
                    params=query,
                    headers=self._headers) as response:
                return await response.json()

    async def post_async(
            self, rel_url: str, query: Optional[dict] = None, body: Optional[dict] = None) -> Optional[dict]:
        """POST implementation"""
        if not await self._throttler.throttle_async():
            return None

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"{self._base_url}/{rel_url.lstrip('/')}",
                    params=query,
                    json=body,
                    headers=self._headers) as response:
                return await response.json()

    async def put_async(
            self, rel_url: str, query: Optional[dict] = None, body: Optional[dict] = None) -> Optional[dict]:
        """PUT implementation"""
        if not await self._throttler.throttle_async():
            return None

        async with aiohttp.ClientSession() as session:
            async with session.put(
                    f"{self._base_url}/{rel_url.lstrip('/')}",
                    params=query,
                    json=body,
                    headers=self._headers) as response:
                return await response.json()
