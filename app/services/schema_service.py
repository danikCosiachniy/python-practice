"""
DСлужба управления схемами и индексами ATABASE.

Считывает файлы схем SQL и индексов с диска и применяет их к базе данных.

Функции:
- `_read_sql()` – считывает содержимое файла SQL как строку.
- `ensure_schema()` – выполняет SQL-запрос для создания схемы.
- `ensure_indexes()` – выполняет SQL-запрос для создания индекса.
"""
import logging
from pathlib import Path
from app.ports.db import DB

logger = logging.getLogger(__name__)

def _read_sql(path: str) -> str:
    """Читает SQL-файл и возвращает его содержимое."""
    try:
        sql = Path(path).read_text(encoding="utf-8")
        logger.info("SQL-файл прочитан: %s (%d символов)", path, len(sql))
        return sql
    except FileNotFoundError:
        logger.error("SQL-файл не найден: %s", path)
        raise
    except Exception as e:
        logger.error("При чтении SQL-файла %s: %s", path, e)
        raise


def ensure_schema(db: DB, schema_path: str = "sql/schema_pg.sql") -> None:
    """Создаёт таблицы и структуру БД из schema_pg.sql."""
    logger.info("Применяем схему: %s", schema_path)
    try:
        db.execute(_read_sql(schema_path))
        logger.info("Схема успешно применена")
    except Exception as e:
        logger.error("При применении схемы (%s): %s", schema_path, e)
        raise


def ensure_indexes(db: DB, indexes_path: str = "sql/indexes_pg.sql") -> None:
    """Создаёт или обновляет индексы БД из indexes_pg.sql."""
    logger.info("Применяем индексы")
    try:
        db.execute(_read_sql(indexes_path))
        logger.info("Индексы успешно применены")
    except Exception as e:
        logger.error("При применении индексов (%s): %s", indexes_path, e)
        raise
