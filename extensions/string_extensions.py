import re


class StringExtensions:
    @classmethod
    def to_kebab_case(cls, literal: str):
        return re.sub(r'(?<!^)(?=[A-Z])', '-', literal).lower()

    @classmethod
    def to_snake_case(cls, literal: str):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', literal).lower()
