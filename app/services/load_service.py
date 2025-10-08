import json
from itertools import islice
from datetime import date
from typing import Iterable, Iterator, Sequence
from app.domain.entities import room_from_json, student_from_json
from app.ports.db import DB

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

#DB/JSON/rooms.json
def load_rooms(db: DB, rooms_path: str, batch_size: int = 1000) -> int:
    """
    Загружает данные о комнатах из JSON-файла и вставляет их в БД пакетами.
    Возвращает количество успешно обработанных записей.
    """
    # прочитать json (список)
    with open(rooms_path, encoding="utf-8") as file:
        read_json = json.load(file)
        file.close()
    # преобразовать в Room + tuples (id, name)
    rooms_tuple = []
    for obj in _batched(read_json):
        try:
            converted = room_from_json(obj)
            rooms_tuple.append((converted.id, converted.name))
        except Exception as e:
            print(f"[WARN] пропущена запись комнаты {obj}: {e}")
    # вставляем в Бд пакетами
    inserted = 0
    with db.transaction():
        for batch in _batched(rooms_tuple, batch_size):
            db.executemany(ROOMS_INSERT, batch)
            inserted += len(batch)
    # вернуть количество вставленных (или обработанных)
    print(f"[INFO] Загружено комнат: {inserted}")
    return inserted

def load_students(db: DB, students_path: str, batch_size: int = 1000) -> int:
    """
    Загружает данные о студентах из JSON-файла и вставляет их в БД пакетами.
    Возвращает количество успешно обработанных записей.
    """
    # прочитать json (список)
    with open(students_path) as file:
        read_json = json.load(file)
        file.close()
    # преобразовать в Student + tuples (id, name, sex, birthday, room_id)
    students_tuple = []
    for obj in _batched(read_json):
        try:
            converted = student_from_json(obj)
            students_tuple.append((converted.id, converted.name, converted.sex, converted.birthday, converted.room_id))
        except Exception as e:
            print(f"[WARN] пропущена запись студента {obj}: {e}")
    # with db.transaction(): executemany batched
    inserted = 0
    with db.transaction():
        for batch in _batched(students_tuple, batch_size):
            db.executemany(STUDENTS_INSERT, batch)
            inserted += len(batch)
    # вернуть количество вставленных (или обработанных)
    print(f"[INFO] Загружено студентов: {inserted}")
    return inserted