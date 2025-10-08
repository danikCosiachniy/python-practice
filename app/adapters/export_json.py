import json
from app.ports.exporter import Exporter
from datetime import date, datetime, timedelta
from decimal import Decimal

class _EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        if isinstance(o, timedelta):
            return o.total_seconds() / 86400.0
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


class JsonExporter(Exporter):
    """
    Реализация экспортера для сохранения данных в формате JSON.

    Пример использования:
        >>> data = {"rooms": [{"id": 1, "name": "Room #1"}]}
        >>> JsonExporter().dump(data, "result.json")
    """
    def dump(self, data: dict, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, cls=_EnhancedJSONEncoder)
