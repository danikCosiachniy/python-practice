import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

class PostgresDB:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._conn = None

    def connect(self) -> None:
        if not self._conn:
            # connect cursor_factory=RealDictCursor, autocommit=False
            pass

    def close(self) -> None:
        # закрыть соединение при наличии
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        # commit если нет ошибок, иначе rollback; закрыть
        pass

    @contextmanager
    def transaction(self):
        # BEGIN; yield; COMMIT или ROLLBACK
        pass

    def execute(self, sql, params=None):
        # with cursor: cur.execute(sql, params)
        pass

    def executemany(self, sql, params_seq):
        # with cursor: cur.executemany(sql, params_seq)
        pass

    def query(self, sql, params=None) -> list[dict]:
        # with cursor: execute; rows = cur.fetchall(); return list(dict(row) ...)
        pass