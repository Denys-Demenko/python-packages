import json
from datetime import date
from typing import Any, Optional

from pydantic import BaseModel


class GenericExtensions:
    @classmethod
    def to_json(cls, obj, path: str):
        def _serialize(x):
            if isinstance(x, BaseModel):
                return {k: _serialize(v) for k, v in x.model_dump().items()}
            if isinstance(x, list):
                return [_serialize(i) for i in x]
            if isinstance(x, dict):
                return {k: _serialize(v) for k, v in x.items()}
            if isinstance(x, date):
                return x.isoformat()
            return x

        with open(path, "w") as f:
            json.dump(_serialize(obj), f, indent=4, ensure_ascii=False)
