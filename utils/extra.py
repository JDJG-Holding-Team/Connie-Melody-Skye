from typing import TYPE_CHECKING, Any, NamedTuple

class ServiceObject(NamedTuple):
    Service: str

    def __str__(self) -> str:
        return self.Service