import threading
import time


class ThrottleTokenBucket:
    def __init__(self, rate_per_sec: float, wait: bool = False):
        self.wait = wait
        self.rate = float(rate_per_sec)
        self.capacity = float(1)
        self.available = 0
        self.last_refill = time.time()
        self._lock = threading.Lock()

    def locked_for(self) -> float:
        now = time.time()
        with self._lock:
            elapsed = now - self.last_refill
            if elapsed > 0:
                self.available = min(self.capacity, self.available + elapsed * self.rate)
                self.last_refill = now

            if self.available >= 1.0:
                self.available -= 1.0
                return 0

            needed = 1.0 - self.available
            wait_seconds = needed / self.rate if self.rate > 0 else 0.0
            return max(0.0, wait_seconds)
