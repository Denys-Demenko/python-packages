from pydantic import Field, BaseModel

from packages.mixins.from_to_mixin import FromToMixin


class ThrottleConfig(BaseModel, FromToMixin):
    rps: int = Field(..., description="Requests per second limit")
    rpm: int = Field(..., description="Requests per minute limit")
    rpd: int = Field(..., description="Requests per day limit")
