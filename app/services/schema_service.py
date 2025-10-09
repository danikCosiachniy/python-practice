from pathlib import Path
from app.ports.db import DB

def _read_sql(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def ensure_schema(db: DB, schema_path: str = "sql/schema_pg.sql") -> None:
    db.execute(_read_sql(schema_path))
    print(f"[INFO] ✅ Схема применена ({schema_path})")

def ensure_indexes(db: DB, indexes_path: str = "sql/indexes_pg.sql") -> None:
    db.execute(_read_sql(indexes_path))
    print(f"[INFO] ✅ Индексы применены ({indexes_path})")