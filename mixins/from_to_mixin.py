from typing import Type, TypeVar
from sqlalchemy.inspection import inspect

T = TypeVar("T")
DB = TypeVar("DB")


class FromToMixin:
    @classmethod
    def from_kwargs(cls: Type[T], **kwargs) -> T:
        return cls(**kwargs)

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        return cls(**data)

    @classmethod
    def from_db(cls: Type[T], db_obj) -> T:
        return cls.from_dict(FromToMixin.to_dict(db_obj))

    def to_dict(self, **extra) -> dict:
        # Check if this is a SQLAlchemy model
        if hasattr(self, '__table__'):
            # SQLAlchemy model
            result = {}
            mapper = inspect(self.__class__)
            for column in mapper.columns:
                val = getattr(self, column.name)
                if not column.primary_key or val is not None:
                    result[column.name] = val
        else:
            # Regular object
            result = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        
        # Add extra key-value pairs
        result.update(extra)
        return result
    
    def to_db(self, db_class: Type[DB], **extra) -> DB:
        """Конвертирует в модель БД"""
        data = self.to_dict(**extra)
        return db_class(**data)
