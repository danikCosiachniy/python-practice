import json
from itertools import islice
from datetime import date
from app.domain.entities import room_from_json, student_from_json
from app.ports.db import DB

def _batched(iterable, batch_size: int):
    # yield chunks (list/tuple) по batch_size
    pass

def load_rooms(db: DB, rooms_path: str, batch_size: int = 1000) -> int:
    # прочитать json (список)
    # преобразовать в Room + tuples (id, name)
    # with db.transaction(): executemany batched
    # вернуть количество вставленных (или обработанных)
    pass

def load_students(db: DB, students_path: str, batch_size: int = 1000) -> int:
    # прочитать json (список)
    # map -> Student (валидировать sex, дату)
    # tuples: (id, name, sex, birthday, room_id)
    # with db.transaction(): executemany batched
    pass