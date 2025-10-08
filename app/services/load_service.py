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
    
    # Поддержим оба возможных формата: [ {...}, ... ] или {"rooms": [ {...}, ... ]}
    if isinstance(read_json, dict) and "rooms" in read_json:
        items = read_json["rooms"]
    elif isinstance(read_json, list):
        items = read_json
    else:
        raise ValueError(f"Ожидался список комнат или ключ 'rooms' в {rooms_path}, получено: {type(data)}")

    # преобразовать в Room + tuples (id, name)
    rooms_tuple: list[tuple] = []
    for i, obj in enumerate(items, 1):
        if not isinstance(obj, dict):
            print(f"[WARN] Skipping invalid room at index {i}: {obj!r} (not a dict)")
            continue
        try:
            r = room_from_json(obj)              # <-- сюда всегда dict
            rooms_tuple.append((r.id, r.name))
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
    with open(students_path, encoding="utf-8") as file:
        read_json = json.load(file)
    # Поддержим оба возможных формата: [ {...}, ... ] или {"students": [ {...}, ... ]}
    if isinstance(read_json, dict) and "students" in read_json:
        items = read_json["students"]
    elif isinstance(read_json, list):
        items = read_json
    else:
        raise ValueError(
            f"Ожидался список студентов или ключ 'students' в {students_path}, получено: {type(read_json)}"
        )

    # преобразовать в Student + tuples (id, name, sex, birthday, room_id)
    students_tuple: list[tuple] = []
    for i, obj in enumerate(items, 1):
        # пропускаем невалидные элементы (если вдруг встретится список или строка)
        if not isinstance(obj, dict):
            print(f"[WARN] Skipping invalid student at index {i}: {obj!r} (not a dict)")
            continue
        try:
            # преобразуем JSON → объект Student
            s = student_from_json(obj)
            students_tuple.append((s.id, s.name, s.sex, s.birthday, s.room_id))
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