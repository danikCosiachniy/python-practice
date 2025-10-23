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
SELECT r.id, r.name, COUNT(s.room_id)
FROM rooms AS r LEFT JOIN students AS s ON r.id = s.room_id
GROUP BY r.id
ORDER BY r.id;
"""

SQL_TOP5_YOUNG_AVG = """
SELECT r.id, r.name,
       ROUND(EXTRACT(YEAR FROM AVG(AGE(s.birthday)))) AS avg_age_years
FROM rooms AS r
JOIN students AS s ON r.id = s.room_id
GROUP BY r.id, r.name
ORDER BY avg_age_years ASC
LIMIT 5;
"""

SQL_TOP5_AGE_SPREAD = """
SELECT r.id, r.name,
       EXTRACT(YEAR FROM MAX(AGE(s.birthday))) -
       EXTRACT(YEAR FROM MIN(AGE(s.birthday))) AS diff_age_years
FROM rooms AS r
JOIN students AS s ON r.id = s.room_id
GROUP BY r.id, r.name
ORDER BY diff_age_years DESC
LIMIT 5;
"""

SQL_MIXED_GENDER = """
SELECT r.id, r.name
FROM rooms AS r
JOIN students AS s ON r.id = s.room_id
GROUP BY r.id, r.name
HAVING COUNT(DISTINCT s.sex) >= 2
ORDER BY r.id;
"""

def _query_run(db : DB, sql: str, name: str)-> list[dict]:
    """Функция унификации запросов"""
    if name == "rooms_counts":
        logger.info(
        "Выполняется запрос: Список комнат и количество студентов в каждой из них;")
    elif name == "top5_young_avg":
        logger.info(
        "Выполняется запрос: 5 комнат с наименьшим средним возрастом студентов;")
    elif name == "top5_age_spread":
        logger.info(
        "Выполняется запрос: 5 комнат с наибольшей разницей в возрасте студентов;")
    elif name == "mixed_gender_rooms":
        logger.info(
        "Выполняется запрос: Список комнат, где проживают студенты разного пола;")
    else:
        logger.info(
        "Выполняется запрос: %s", name)
    try:
        result = db.query(sql)
        return result
    except ProgrammingError as e:
        # Ошибка в синтаксисе SQL или структура таблицы не совпадает
        logger.error("Ошибка SQL-синтаксиса в %s: %s", name, e)
        return []

    except (TypeError, ValueError) as e:
        # Ошибки преобразования данных, если что-то не так с типами
        logger.error("Ошибка типов данных при обработке %s: %s", name, e)
        return []

    except Exception as e:  # pylint: disable=broad-exception-caught
        # Непредвиденные ошибки — логируем, но не падаем
        logger.exception("Неизвестная ошибка при %s: %s", name, e)
        return []

def rooms_counts(db: DB) -> list[dict]:
    """Функция для выполнения запроса на список комнат и количество студентов в каждой из них"""
    return _query_run(db, SQL_ROOMS_COUNT, "rooms_counts")


def top5_young_avg(db: DB) -> list[dict]:
    """Функция для выполнения запроса на 5 комнат с наименьшим срденим возрастом студентов"""
    return _query_run(db, SQL_TOP5_YOUNG_AVG, "top5_young_avg")


def top5_age_spread(db: DB) -> list[dict]:
    """Функция для выполнения запроса 5 комнат с наибольшей разницей в возрасте студентов"""
    return _query_run(db, SQL_TOP5_AGE_SPREAD, "top5_age_spread")


def mixed_gender_rooms(db: DB) -> list[dict]:
    """Функция для выполнения запроса Список комнат, где проживают студенты разного пола;"""
    return _query_run(db, SQL_MIXED_GENDER, "mixed_gender_rooms")
