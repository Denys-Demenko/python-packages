import logging

from packages.throttling.throttle_config import ThrottleConfig
from packages.throttling.throttle_token_bucket import ThrottleTokenBucket


class ThrottleService:
    """Token bucket throttling implementation."""

    def __init__(self, config: ThrottleConfig):
        """Initialize _throttler with configuration."""
        self._config = config
        self._logger = logging.getLogger(__name__)
        self._buckets = [
            ThrottleTokenBucket(rate_per_sec=config.rps, capacity=config.rps) if config.rps else None,
            ThrottleTokenBucket(rate_per_sec=config.rpm / 60, capacity=config.rpm) if config.rpm else None,
            ThrottleTokenBucket(rate_per_sec=config.rpd / 86400, capacity=config.rpd) if config.rpd else None,
        ]

    async def throttle_async(self) -> bool:
        for bucket in self._buckets:
            if bucket and not bucket.allow():
                return False
        return True
