import os
import logging
from app.adapters.postgres_db import PostgresDB
from app.adapters.export_json import JsonExporter
from app.adapters.export_xml import XmlExporter
from app.services import schema_service, load_service, query_service
logger = logging.getLogger(__name__)

def app():
    # Настраиваем логгер 
    logging.basicConfig(filename="logs/app.log",level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")
    logger.info("Программа запущена")
    logger.info("Принимаем параметры")

    # Принимаем необходимые параметры
    # students (путь к файлу со студентами);
    students_json_path = input("Введите путь до файла студентов в формате json\n")
    logger.info(f"Задан путь для файла со студентами {students_json_path}")
    # Rooms (путь к файлу со комнатами);
    rooms_json_path = input("Введите путь к json файлу комнат \n")
    logger.info(f"Задан путь для файла с комнатами {rooms_json_path}")
    # format (выходной формат: xml или json);
    form = input("Введите выходной формат: xml или json\n").lower()
    # название файла для выгрузки результатов
    name_of_file = input("Введите название файла для выгрузки результата\n")
    logger.info(f"Задано название файла результатов {name_of_file}")
    
    # Проверка на добавление формата файла к файлу результата
    if form not in name_of_file:
        logger.info(f"Добавлен формат к названию файла")
        name_of_file += '.' + form
    
    # Читаем параметры для создания ссылки для подключения к БД
    logger.info("Читаем параметры для подключения к БД")
    host = os.environ.get("PGHOST", "localhost")
    port = os.environ.get("PGPORT", "5432")
    user = os.environ.get("PGUSER", "app")
    pwd = os.environ.get("PGPASSWORD", "app")
    dbn = os.environ.get("PGDATABASE", "university")
    logger.info("Создаем ссылку на БД")
    db_url = f"postgresql://{user}:{pwd}@{host}:{port}/{dbn}"

    # Задаем экспортер файла результатов
    if form == 'json':
        logger.info("Инициализирован экспортер для JSON")
        exporter = JsonExporter()
    else:
        logger.info("Инициализиован экспотер для XML")
        exporter = XmlExporter()
    
    # Начинаем работу с БД
    with PostgresDB(db_url) as db:
        logger.info("Успешное подулючение к БД")
        # Задаем схему БД
        logger.info("Задаем схему БД")
        schema_service.ensure_schema(db)
        
        # Добавляем индексы
        logger.info("Добавляем индексы")
        schema_service.ensure_indexes(db)
        
        # Загружаем данные из файлов в БД
        logger.info("Загружаем файл студентов в БД")
        imported_rooms = load_service.load_rooms(db, rooms_json_path)
        logger.info("Загружаем файл комнат в БД")
        imported_students = load_service.load_students(db, students_json_path)
        logger.info("Выполняем запросы к БД и записываем реузльтат в словарь")
        # словарь для результатов запросов к БД
        result = {
            "count_student_in_rooms" : query_service.rooms_counts(db),
            "top5_young_avg" : query_service.top5_young_avg(db),
            "top5_age_spread": query_service.top5_age_spread(db),
            "rooms_with_mixed_gender": query_service.mixed_gender_rooms(db),
            "meta": {"inserted_rooms": imported_rooms, "inserted_students": imported_students},
        } 
        logger.info("Экспортируем результат")
        # Экспортируем результат
        exporter.dump(result, "data/results/" + name_of_file)

if __name__ == "__main__":
    app()
