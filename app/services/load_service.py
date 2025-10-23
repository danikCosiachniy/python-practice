"""
Сервис загрузки данных.

Обрабатывает чтение JSON-файлов и пакетную вставку данных в базу данных.

Функции:
- `_batched()` – создание итерируемых фрагментов для эффективной массовой вставки.
- `load_rooms()` – загрузка и вставка данных о комнатах.
- `load_students()` – загрузка и вставка данных о студентах.

Вся проверка данных делегируется `room_from_json` и `student_from_json`.
"""
import json
import logging
from typing import Iterable, Iterator, Sequence
from app.domain.entities import room_from_json, student_from_json
from app.ports.db import DB
logger = logging.getLogger(__name__)

ROOMS_INSERT = """
INSERT INTO rooms(id, name)
VALUES (%s, %s)
ON CONFLICT (id) DO NOTHING;
"""

STUDENTS_INSERT = """
INSERT INTO students(id, name, sex, birthday, room_id)
VALUES (%s,%s,%s,%s,%s)
ON CONFLICT (id) DO NOTHING;
"""

def _batched(iterable: Iterable, batch_size: int) -> Iterator[Sequence]:
    """
    Генератор, возвращающий последовательные фрагменты (батчи)
    из iterable размером не более batch_size.

    Пример:
        >>> list(_batched([1,2,3,4,5], 2))
        [[1,2], [3,4], [5]]
    """
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

def _load_run(db: DB, path: str, type_of_data: str, batch_size: int = 1000) -> int:
    """Функция для унификации функций загрузки данных студентов и комнат"""
    logger.info("Запущена функция load_%s", type_of_data)
    if type_of_data == "students":
        logger.info("Читаем файл студентов")
    elif type_of_data == "rooms":
        logger.info("Читаем файл комнат")
    # прочитать json (список)
    with open(path, encoding="utf-8") as file:
        read_json = json.load(file)
    # Поддержим оба возможных формата: [ {...}, ... ] или {"students": [ {...}, ... ]}
    if isinstance(read_json, dict) and type_of_data in read_json:
        items = read_json[type_of_data]
    elif isinstance(read_json, list):
        items = read_json
    else:
        logger.error("Ожидался список данных или ключ '%s' в %s, получено: %s",
                    type_of_data,
                    path,
                    type(read_json))
        raise ValueError(
            f"Ожидался список данных или ключ в {path}, получено: {type(read_json)}"
        )
    logger.info("Преобразовываем в %s и записываем в кортеж", type_of_data)
    # преобразовать в Student + tuples (id, name, sex, birthday, room_id)
    data_tuple: list[tuple] = []
    for i, obj in enumerate(items, 1):
        # пропускаем невалидные элементы (если вдруг встретится список или строка)
        if not isinstance(obj, dict):
            logger.error("Skipping invalid %s at index %s: %r (not a dict)",type_of_data,i,obj)
            continue
        try:
            if type_of_data == "students":
                # преобразуем JSON → объект Student
                s = student_from_json(obj)
                data_tuple.append((s.id, s.name, s.sex, s.birthday, s.room_id))
            elif type_of_data == "rooms":
                # преобразуем JSON → объект Room
                r = room_from_json(obj)
                data_tuple.append((r.id, r.name))
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Пропущена запись %s: %s",obj, e)
    logger.info("Вставляем в Бд пакетами")
    # Вставляем в бд пакетами
    inserted = 0
    with db.transaction():
        for batch in _batched(data_tuple, batch_size):
            if type_of_data == "students":
                db.executemany(STUDENTS_INSERT, batch)
                inserted += len(batch)
            elif type_of_data == "rooms":
                db.executemany(ROOMS_INSERT, batch)
                inserted += len(batch)
    # вернуть количество вставленных (или обработанных)
    logger.info("Загружено %s: %s", type_of_data, inserted)
    return inserted

def load_rooms(db: DB, rooms_path: str, batch_size: int = 1000) -> int:
    """
    Загружает данные о комнатах из JSON-файла и вставляет их в БД пакетами.
    Возвращает количество успешно обработанных записей.
    """
    return _load_run(db, rooms_path, "rooms", batch_size)

def load_students(db: DB, students_path: str, batch_size: int = 1000) -> int:
    """
    Загружает данные о студентах из JSON-файла и вставляет их в БД пакетами.
    Возвращает количество успешно обработанных записей.
    """
    return _load_run(db, students_path, "students", batch_size)
