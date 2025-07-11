from packages.http.http_throttled_service import HttpThrottledService
from packages.throttling.throttle_config import ThrottleConfig
from packages.throttling.throttle_service import ThrottleService


class HttpThrottledServiceFactory:
    def create(self, base_url: str, headers: dict[str, str], throttle_config: ThrottleConfig):
        return HttpThrottledService(base_url, headers, ThrottleService(throttle_config))
