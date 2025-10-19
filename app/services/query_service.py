"""
Сервис аналитических SQL-запросов.

Содержит SQL-запросы многократного использования и оболочки, возвращающие результаты запросов
в виде списков словарей.

Запросы включают в себя:
- `rooms_counts()` – количество студентов в комнате.
- `top5_young_avg()` – 5 комнат с самым низким средним возрастом.
- `top5_age_spread()` – 5 комнат с самой большой разницей в возрасте.
- `mixed_gender_rooms()` – комнаты со студентами обоих полов.
"""
import logging
from psycopg2 import ProgrammingError
from app.ports.db import DB

logger = logging.getLogger(__name__)

SQL_ROOMS_COUNT = """
SELECT rooms.id, rooms.name, COUNT(students.room_id)
FROM rooms LEFT JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id
ORDER BY rooms.id;
"""

SQL_TOP5_YOUNG_AVG = """
SELECT rooms.id, rooms.name,
       ROUND(EXTRACT(YEAR FROM AVG(AGE(students.birthday)))) AS avg_age_years
FROM rooms
JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id, rooms.name
ORDER BY avg_age_years ASC
LIMIT 5;
"""

SQL_TOP5_AGE_SPREAD = """
SELECT rooms.id, rooms.name,
       EXTRACT(YEAR FROM MAX(AGE(students.birthday))) -
       EXTRACT(YEAR FROM MIN(AGE(students.birthday))) AS diff_age_years
FROM rooms
JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id, rooms.name
ORDER BY diff_age_years DESC
LIMIT 5;
"""

SQL_MIXED_GENDER = """
SELECT rooms.id, rooms.name
FROM rooms
JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id, rooms.name
HAVING COUNT(DISTINCT students.sex) >= 2
ORDER BY rooms.id;
"""


def rooms_counts(db: DB) -> list[dict]:
    """Функция для выполнения запроса на список комнат и количество студентов в каждой из них"""
    logger.info(
        "Выполняется запрос: Список комнат и количество студентов в каждой из них;")
    try:
        result = db.query(SQL_ROOMS_COUNT)
        return result
    except ProgrammingError as e:
        # Ошибка в синтаксисе SQL или структура таблицы не совпадает
        logger.error("Ошибка SQL-синтаксиса в rooms_counts: %s", e)
        return []

    except (TypeError, ValueError) as e:
        # Ошибки преобразования данных, если что-то не так с типами
        logger.error("Ошибка типов данных при обработке rooms_counts: %s", e)
        return []

    except Exception as e:  # pylint: disable=broad-exception-caught
        # Непредвиденные ошибки — логируем, но не падаем
        logger.exception("Неизвестная ошибка при rooms_counts: %s", e)
        return []


def top5_young_avg(db: DB) -> list[dict]:
    """Функция для выполнения запроса на 5 комнат с наименьшим срденим возрастом студентов"""
    logger.info(
        "Выполняется запрос: 5 комнат с наименьшим средним возрастом студентов;")
    try:
        result = db.query(SQL_TOP5_YOUNG_AVG)
        return result
    except ProgrammingError as e:
        # Ошибка в синтаксисе SQL или структура таблицы не совпадает
        logger.error("Ошибка SQL-синтаксиса в top5_young_avg: %s", e)
        return []

    except (TypeError, ValueError) as e:
        # Ошибки преобразования данных, если что-то не так с типами
        logger.error("Ошибка типов данных при обработке top5_young_avg: %s", e)
        return []

    except Exception as e:  # pylint: disable=broad-exception-caught
        # Непредвиденные ошибки — логируем, но не падаем
        logger.exception("Неизвестная ошибка при top5_young_avg: %s", e)
        return []


def top5_age_spread(db: DB) -> list[dict]:
    """Функция для выполнения запроса 5 комнат с наибольшей разницей в возрасте студентов"""
    logger.info(
        "Выполняется запрос: 5 комнат с наибольшей разницей в возрасте студентов;")
    try:
        result = db.query(SQL_TOP5_AGE_SPREAD)
        return result
    except ProgrammingError as e:
        # Ошибка в синтаксисе SQL или структура таблицы не совпадает
        logger.error("Ошибка SQL-синтаксиса в top5_age_spread: %s", e)
        return []

    except (TypeError, ValueError) as e:
        # Ошибки преобразования данных, если что-то не так с типами
        logger.error("Ошибка типов данных при обработке top5_age_spread: %s", e)
        return []

    except Exception as e:  # pylint: disable=broad-exception-caught
        # Непредвиденные ошибки — логируем, но не падаем
        logger.exception("Неизвестная ошибка при top5_age_spread: %s", e)
        return []


def mixed_gender_rooms(db: DB) -> list[dict]:
    """Функция для выполнения запроса Список комнат, где проживают студенты разного пола;"""
    logger.info(
        "Выполняется запрос: Список комнат, где проживают студенты разного пола;")
    try:
        result = db.query(SQL_MIXED_GENDER)
        return result
    except ProgrammingError as e:
        # Ошибка в синтаксисе SQL или структура таблицы не совпадает
        logger.error("Ошибка SQL-синтаксиса в mixed_gender_rooms: %s", e)
        return []

    except (TypeError, ValueError) as e:
        # Ошибки преобразования данных, если что-то не так с типами
        logger.error("Ошибка типов данных при обработке mixed_gender_rooms: %s", e)
        return []

    except Exception as e:  # pylint: disable=broad-exception-caught
        # Непредвиденные ошибки — логируем, но не падаем
        logger.exception("Неизвестная ошибка при mixed_gender_rooms: %s", e)
        return []
