import threading
import time


class ThrottleTokenBucket:
    def __init__(self, rate_per_sec: float, capacity: int):
        self.rate = rate_per_sec
        self.capacity = float(capacity)
        self.available = float(capacity)
        self.last_refill = time.time()
        self._lock = threading.Lock()

    def allow(self) -> bool:
        now = time.time()
        with self._lock:
            elapsed = now - self.last_refill
            refill = elapsed * self.rate
            self.available = min(self.capacity, self.available + refill)
            self.last_refill = now

            if self.available >= 1:
                self.available -= 1
                return True
            return False
