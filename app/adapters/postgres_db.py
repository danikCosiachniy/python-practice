from contextlib import contextmanager
from typing import Iterable, Mapping
import psycopg2
from psycopg2.extras import RealDictCursor
from app.ports.db import DB


class PostgresDB(DB):
    """
    Реализация порта DB для PostgreSQL на psycopg2.
    Возвращает строки как dict, поддерживает:
      - контекстный менеджер для подключения (with PostgresDB(...))
      - явные транзакции (with db.transaction())
      - execute / executemany / query
    """

    
    def __init__(self, dsn: str, autocommit : bool = False):
        """
        dsn-пример:
        postgresql://app:app@localhost:5432/university
        """

        self._dsn = dsn
        self._conn = None
        self._autocommit = autocommit
    
    
    # ---- lifecycle ----
    def connect(self) -> None:
        if self._conn is None:
            self._conn = psycopg2.connect(self._dsn, cursor_factory=RealDictCursor)
            self._conn.autocommit = self._autocommit
    

    def close(self) -> None:
        if self._conn is not None:
            try:
                self._conn.close()
            finally:
                self._conn = None
    

    def __enter__(self) -> "PostgresDB":
        self.connect()
        return self


    def __exit__(self, exc_type, exc, tb) -> None:
        # Если работаем не в autocommit и вышли из with:
        if self._conn and not self._autocommit:
            if exc_type is None:
                self._conn.commit()
            else:
                self._conn.rollback()
        self.close()
    

    # ---- transaction validator ----
    @contextmanager
    def transaction(self):
        """
        Использование:
            with db.transaction():
                db.execute(...)
                db.executemany(...)
        """
        if self._conn is None:
            self.connect()
        # Начало «явной» транзакции для блока
        try:
            yield
        except Exception:
            if self._conn and not self._autocommit:
                self._conn.rollback()
            raise
        else:
            if self._conn and not self._autocommit:
                self._conn.commit()
    

    # ---- low-level ops ----
    def execute(self, sql: str, params: tuple | Mapping | None = None) -> None:
        if self._conn is None:
            self.connect()
        with self._conn.cursor() as cursor:
            cursor.execute(sql, params)
    

    def executemany(self, sql: str, params : Iterable[tuple]) -> None:
        if self._conn is None:
            self.connect()
        with self._conn.cursor() as cursor:
            cursor.executemany(sql, params)


    def query(self, sql: str, params: tuple | Mapping | None = None) -> list[dict]:
        if self._conn is None:
            self.connect()
        with self._conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            # RealDictCursor уже даёт dict-подобные объекты
            return [dict(r) for r in rows]
