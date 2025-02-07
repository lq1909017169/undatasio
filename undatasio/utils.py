from pydantic import BaseModel
from typing import List


class Field(BaseModel):
    name: str = None
    rule: str = None
    value: str = None
    content: str = None


class StringField(Field):
    attribute: str = 'str'


class FloatField(Field):
    attribute: str = 'float'


class IntField(Field):
    attribute: str = 'int'


class ListField(Field):
    attribute: str = 'list'


class DictField(Field):
    attribute: str = 'dict'
    keys: List

