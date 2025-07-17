from django.forms.models import model_to_dict
from django.db import models
from typing import Type, TypeVar

T = TypeVar("T")


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

    def to_dict(self) -> dict:
        if isinstance(self, models.Model):
            data = model_to_dict(self)
            for field in self._meta.fields:
                if field.is_relation and field.name in data:
                    data[field.name + '_id'] = getattr(self, field.attname)
                    del data[field.name]
            return data
        return self.__dict__
