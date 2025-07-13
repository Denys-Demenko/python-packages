from typing import Any, Optional


class DictExtensions:
    @classmethod
    def get_prefixed_key(cls, data: dict[str, Any], prefix: str) -> Optional[str]:
        for key in data:
            if key.startswith(prefix):
                return key
        return None
