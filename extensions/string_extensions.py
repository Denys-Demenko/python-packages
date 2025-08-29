import re


class StringExtensions:
    @classmethod
    def to_kebab_case(cls, literal: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '-', literal).lower()

    @classmethod
    def to_snake_case(cls, literal: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', literal).lower()
    
    @classmethod
    def as_bool(cls, literal: str) -> bool:
        return str(literal).strip().lower() in ("1", "true", "yes", "y", "on")
