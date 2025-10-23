"""
Сущности предметной области и валидаторы JSON.

Определяет неизменяемые классы данных:
- `Room`
- `Student`

Предоставляет вспомогательные функции:
- `room_from_json()` – проверяет и преобразует необработанный словарь в Room.
- `student_from_json()` – проверяет и преобразует необработанный словарь в Student,
поддерживая JSON-ключи «room» и «room_id», а также даты в формате ISO.
"""
from dataclasses import dataclass
from datetime import date, datetime
import logging
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Room:
    '''The data class for Room.'''
    id: int
    name: str

@dataclass(frozen=True)
class Student:
    '''The data class for Student'''
    id: int
    name: str
    sex: str        # 'M' | 'F'
    birthday: date
    room_id: int

# helper для валидации студента из сырого json-словаря
def student_from_json(obj: dict) -> Student:
    '''Это функция для преобразования данных студента из словаря JSON в класс данных Student.'''
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
        room_id = obj.get("room_id", obj.get("room"))
        if room_id is None:
            raise KeyError("room_id")
        room_id = int(room_id)
        # вернуть Student(...)
        return Student(student_id, name, sex, birthday, room_id)
    # Обработка ошибок
    except KeyError as e:
        logger.error("Пропущен студент — отсутствует поле '%s': %s", e.args[0], obj)
        raise ValueError(f"Missing field {e.args[0]} in student JSON: {obj}") from e
    except (TypeError, ValueError) as e:
        logger.error("Пропущен студент — некорректные данные: %s (%s)", obj, e)
        raise ValueError(f"Invalid student data {obj}: {e}") from e
# helper для валидации комнаты из сырого json-словаря
def room_from_json(obj: dict) -> Room | None:
    '''Это функция для преобразования данных студента из словаря JSON в класс данных Room.'''
    try:
        # простая проверка id:int, name:str
        return Room(
            id=int(obj.get("id")),
            name=str(obj.get("name", "")).strip(),
        )
    except KeyError as e:
        logger.error("Пропущена комната — отсутствует поле '%s': %s", e.args[0], obj)
        return None

    except (TypeError, ValueError) as e:
        logger.error("Пропущена комната — некорректные данные: %s (%s)", obj, e)
        return None
