import asyncio
import logging

from packages.throttling.throttle_config import ThrottleConfig
from packages.throttling.throttle_token_bucket import ThrottleTokenBucket


class ThrottleService:
    """Token bucket throttling implementation."""
    WAIT_TIME_THRESHOLD_SECONDS = 20

    def __init__(self, config: ThrottleConfig):
        """Initialize _throttler with configuration."""
        self._config = config
        self._logger = logging.getLogger(__name__)
        self._buckets = [
            ThrottleTokenBucket(rate_per_sec=config.rps, wait=True) if config.rps else None,
            ThrottleTokenBucket(rate_per_sec=config.rpm / 60, wait=True) if config.rpm else None,
            ThrottleTokenBucket(rate_per_sec=config.rpd / 86400) if config.rpd else None,
        ]

    async def throttle_async(self) -> bool:
        for bucket in self._buckets:
            if bucket:
                wait_time = bucket.locked_for()
                if wait_time:
                    if bucket.wait or wait_time < self.WAIT_TIME_THRESHOLD_SECONDS:
                        await asyncio.sleep(wait_time)
                    else:
                        return False
        return True
