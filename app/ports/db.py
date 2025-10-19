"""
Интерфейс для взаимодействия с базой данных (порт DB).

Этот модуль определяет протокол `DB`, который описывает контракт для всех
реализаций подключения к базе данных. Такой подход обеспечивает гибкость и
позволяет использовать различные СУБД (PostgreSQL, SQLite, MySQL и т.д.),
не изменяя основную бизнес-логику.

Методы:
    connect() -> None:
        Устанавливает соединение с базой данных.

    close() -> None:
        Закрывает текущее соединение.

    execute(sql: str, params: tuple | dict | None = None) -> None:
        Выполняет одиночный SQL-запрос без возврата данных (INSERT, UPDATE, DELETE).

    executemany(sql: str, params_seq: Iterable[tuple]) -> None:
        Выполняет пакетную вставку данных (bulk insert).

    query(sql: str, params: tuple | dict | None = None) -> list[dict]:
        Выполняет SQL-запрос с выборкой данных и возвращает результат
        в виде списка словарей.

    transaction() -> ContextManager[None]:
        Контекстный менеджер для выполнения транзакций.
        Пример:
            with db.transaction():
                db.execute(...)
                db.execute(...)

    __enter__() / __exit__():
        Поддержка контекстного менеджера на уровне соединения с БД.
"""
from typing import Protocol, Iterable, Mapping, ContextManager

class DB(Protocol):
    def connect(self) -> None: ...
    def close(self) -> None: ...
    def execute(self, sql: str, params: tuple | Mapping | None = None) -> None: ...
    def executemany(self, sql: str, params_seq: Iterable[tuple]) -> None: ...
    def query(self, sql: str, params: tuple | Mapping | None = None) -> list[dict]: ...
    def transaction(self) -> ContextManager[None]: ...  # with db.transaction(): ...

    # опционально: контекстный менеджер для всего подключения
    def __enter__(self) -> "DB": ...
    def __exit__(self, exc_type, exc, tb) -> None: ...
