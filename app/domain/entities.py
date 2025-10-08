from dataclasses import dataclass
from datetime import date, datetime

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
    try:
        # извлечь id, name, sex, birthday(str), room -> room_id
        student_id = int(obj["id"])
        name = str(obj["name"])
        sex = str(obj["sex"])
        # проверить sex ∈ {'M','F'}
        if sex not in {"M", "F"}:
            raise ValueError(f"Invalid sex '{sex}' (expected M/F)")
        # распарсить birthday (YYYY-MM-DD) -> date
        bday_raw = obj["birthday"]
        birthday = datetime.fromisoformat(bday_raw).date()
        room_id = int(obj["room"])
        # вернуть Student(...)
        return Student(student_id, name, sex, birthday, room_id)
    # Обработка ошибок
    except KeyError as e:
        raise ValueError(f"Missing field {e.args[0]} in student JSON: {obj}") from e
    except Exception as e:
        raise ValueError(f"Invalid student data {obj}: {e}") from e

# helper для валидации комнаты из сырого json-словаря
def room_from_json(obj: dict) -> Room | None:
    try:
        # простая проверка id:int, name:str
        return Room(
            id=int(obj.get("id")),
            name=str(obj.get("name", "")).strip(),
        )
    except Exception as e:
        print(f"[WARN] Skipping invalid room: {obj} ({e})")
        return None