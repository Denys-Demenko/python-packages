import asyncio
import logging
import time

from packages.throttling.throttle_config import ThrottleConfig


class ThrottleService:
    """Simple rate limiter with uniform intervals."""

    def __init__(self, config: ThrottleConfig):
        """Initialize throttler with configuration."""
        self._config = config
        self._logger = logging.getLogger(__name__)
        self._last_execution_time = None
        
        # Calculate interval from config
        if config.rps and config.rps > 0:
            self._interval = 1.0 / config.rps
        elif config.rpm and config.rpm > 0:
            self._interval = 60.0 / config.rpm
        elif config.rpd and config.rpd > 0:
            self._interval = 86400.0 / config.rpd
        else:
            self._interval = 0

    async def throttle_async(self) -> bool:
        if self._interval > 0:
            await self._wait_for_interval()
        self._log_execution()
        return True

    def throttle(self) -> bool:
        """Synchronous throttle method."""
        if self._interval > 0:
            self._wait_for_interval_sync()
        self._log_execution()
        return True

    def _wait_for_interval_sync(self):
        """Wait for the required interval synchronously."""
        if self._last_execution_time:
            elapsed = time.time() - self._last_execution_time
            wait_time = self._interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)

    async def _wait_for_interval(self):
        """Wait for the required interval asynchronously."""
        if self._last_execution_time:
            elapsed = time.time() - self._last_execution_time
            wait_time = self._interval - elapsed
            if wait_time > 0:
                await asyncio.sleep(wait_time)

    def _log_execution(self):
        """Log execution with time span from previous execution."""
        current_time = time.time()
        if self._last_execution_time:
            time_span = current_time - self._last_execution_time
            self._logger.info(f"Throttle executed. Time span from previous: {time_span:.2f}s")
        else:
            self._logger.info("Throttle executed. First execution.")
        self._last_execution_time = current_time
