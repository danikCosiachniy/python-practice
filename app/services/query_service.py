import logging
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
    logger.info("Выполняется запрос: Список комнат и количество студентов в каждой из них;")
    try:
        result = db.query(SQL_ROOMS_COUNT)
        return result
    except Exception as e:
        logger.error("При выполнении rooms_counts: %s", e)
        return []


def top5_young_avg(db: DB) -> list[dict]:
    logger.info("Выполняется запрос: 5 комнат с наименьшим средним возрастом студентов;")
    try:
        result = db.query(SQL_TOP5_YOUNG_AVG)
        return result
    except Exception as e:
        logger.error("При выполнении top5_young_avg: %s", e)
        return []


def top5_age_spread(db: DB) -> list[dict]:
    logger.info("Выполняется запрос: 5 комнат с наибольшей разницей в возрасте студентов;")
    try:
        result = db.query(SQL_TOP5_AGE_SPREAD)
        return result
    except Exception as e:
        logger.error("При выполнении top5_age_spread: %s", e)
        return []


def mixed_gender_rooms(db: DB) -> list[dict]:
    logger.info("Выполняется запрос: Список комнат, где проживают студенты разного пола;")
    try:
        result = db.query(SQL_MIXED_GENDER)
        return result
    except Exception as e:
        logger.error("При выполнении mixed_gender_rooms: %s", e)
        return []