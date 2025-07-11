from pydantic import Field

from packages.mixins.from_to_mixin import FromToMixin


class ThrottleConfig(FromToMixin):
    rps: int = Field(..., description="Requests per second limit")
    rpm: int = Field(..., description="Requests per minute limit")
    rpd: int = Field(..., description="Requests per day limit")
