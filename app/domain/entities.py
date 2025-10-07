from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Room:
    id: int
    name: str

@dataclass(frozen=True)
class Student:
    id: int
    name: str
    sex: str        # 'M' | 'F'
    birthday: date
    room_id: int

# helper для валидации студента из сырого json-словаря
def student_from_json(obj: dict) -> Student:
    # извлечь id, name, sex, birthday(str), room -> room_id
    # проверить sex ∈ {'M','F'}
    # распарсить birthday (YYYY-MM-DD) -> date
    # вернуть Student(...)
    pass

def room_from_json(obj: dict) -> Room:
    # простая проверка id:int, name:str
    pass