from typing import TYPE_CHECKING, Any, NamedTuple

class ServiceObject(NamedTuple):
    name: str

    def __str__(self) -> str:
        return self.Service
    

class DataObject(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)