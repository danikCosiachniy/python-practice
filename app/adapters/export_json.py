import json
import logging
from app.ports.exporter import Exporter
from datetime import date, datetime, timedelta
from decimal import Decimal

logger = logging.getLogger(__name__)

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
        logger.info("Экспорт данных в JSON")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2, cls=_EnhancedJSONEncoder)
            logger.info("Экспорт завершён успешно")
        except Exception as e:
            logger.error("Ошибка при экспорте JSON (%s): %s", path, e)
            raise
