from pydantic import Field


class ThrottleConfig:
    rps: int = Field(..., description="Requests per second limit")
    rpm: int = Field(..., description="Requests per minute limit")
    rpd: int = Field(..., description="Requests per day limit")
