import json
from app.ports.exporter import Exporter


class JsonExporter(Exporter):
    """
    Реализация экспортера для сохранения данных в формате JSON.

    Пример использования:
        >>> data = {"rooms": [{"id": 1, "name": "Room #1"}]}
        >>> JsonExporter().dump(data, "result.json")
    """
    def dump(self, data: dict, path: str) -> None:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)