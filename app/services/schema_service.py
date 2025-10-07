from pathlib import Path
from app.ports.db import DB

def _read_sql(path: str) -> str:
    # Path(path).read_text(encoding="utf-8")
    pass

def ensure_schema(db: DB, schema_path: str = "sql/schema_pg.sql") -> None:
    # sql = _read_sql(schema_path)
    # db.execute(sql)  # допускается multi-statement, или по частям
    pass

def ensure_indexes(db: DB, indexes_path: str = "sql/indexes_pg.sql") -> None:
    # аналогично
    pass