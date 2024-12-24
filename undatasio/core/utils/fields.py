from pydantic import BaseModel


class Field(BaseModel):
    name: str = None
    rule: str = None
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
