import typer
from app.adapters.postgres_db import PostgresDB
from app.adapters.export_json import JsonExporter
from app.adapters.export_xml import XmlExporter
from app.services import schema_service, load_service, query_service

def app():
    # Принимаем необходимые параметры
    # 5.1. students (путь к файлу со студентами);
    # 5.2. Rooms (путь к файлу со комнатами);
    # 5.3. format (выходной формат: xml или json);

    students_json_path = input("Введите путь до файла студентов в формате json\n")
    rooms_json_path = input("Введите путь к json файлу комнат \n")
    form = input("Введите выходной формат: xml или json\n").lower()
    name_of_file = input("Введите название файла для выгрузки результата\n")
    if form not in name_of_file:
        name_of_file += '.' + form
    db_url = input("Введите ссылку на бд \n")
    if form == 'json':
        exporter = JsonExporter()
    else:
        exporter = XmlExporter()
    with PostgresDB(db_url) as db:

        imported_rooms = load_service.load_rooms(db, rooms_json_path)
        imported_students = load_service.load_students(db, students_json_path)
        result = {
            "count_student_in_rooms" : query_service.rooms_counts(db),
            "top5_young_avg" : query_service.top5_young_avg(db),
            "top5_age_spread": query_service.top5_age_spread(db),
            "rooms_with_mixed_gender": query_service.mixed_gender_rooms(db),
            "meta": {"inserted_rooms": imported_rooms, "inserted_students": imported_students},
        }
        print(result["top5_young_avg"])
        exporter.dump(result, name_of_file)

if __name__ == "__main__":
    app()