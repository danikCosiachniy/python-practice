from typing import Protocol

class Exporter(Protocol):
    def dump(self, data: dict, path: str) -> None: ...