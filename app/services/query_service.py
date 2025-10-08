from app.ports.db import DB

SQL_ROOMS_COUNT = """
SELECT rooms.id, rooms.name, COUNT(students.room_id)
FROM rooms left join students on rooms.id = students.room_id
GROUP BY rooms.id
ORDER BY rooms.id;
"""

SQL_TOP5_YOUNG_AVG = """
SELECT rooms.id, rooms.name, AVG(AGE(students.birthday)) AS avg_age_years FROM rooms JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id, rooms.name
ORDER BY avg_age_years ASC
LIMIT 5;
"""

SQL_TOP5_AGE_SPREAD = """
SELECT rooms.id, rooms.name, MAX(AGE(students.birthday)) - min(age(students.birthday)) AS DIFF_age_years FROM rooms JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id, rooms.name
ORDER BY DIFF_age_years DESC
LIMIT 5;
"""

SQL_MIXED_GENDER = """
SELECT rooms.id, rooms.name FROM rooms JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id, rooms.name
HAVING COUNT(distinct students.sex) >= 2
ORDER BY rooms.id;
"""

def rooms_counts(db: DB) -> list[dict]:
    return db.query(SQL_ROOMS_COUNT)

def top5_young_avg(db: DB) -> list[dict]:
    return db.query(SQL_TOP5_YOUNG_AVG)

def top5_age_spread(db: DB) -> list[dict]:
    return db.query(SQL_TOP5_AGE_SPREAD)


def mixed_gender_rooms(db: DB) -> list[dict]:
    return db.query(SQL_MIXED_GENDER)
