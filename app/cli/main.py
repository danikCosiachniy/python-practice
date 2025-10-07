# псевдокод

import typer
from app.adapters.postgres_db import PostgresDB
from app.adapters.export_json import JsonExporter
from app.adapters.export_xml import XmlExporter
from app.services import schema_service, load_service, query_service

app = typer.Typer()

@app.command()
def run(
    students: str = typer.Option(..., help="Путь к students.json"),
    rooms: str = typer.Option(..., help="Путь к rooms.json"),
    format: str = typer.Option("json", help="json|xml"),
    out: str = typer.Option("result.json", help="Имя файла результата"),
    db_url: str = typer.Option(..., envvar="DB_URL", help="postgresql://user:pass@host:port/db"),
):
    exporter = JsonExporter() if format.lower() == "json" else XmlExporter()
    with PostgresDB(db_url) as db:
        # 1) схема/индексы
        schema_service.ensure_schema(db)
        schema_service.ensure_indexes(db)

        # 2) загрузка данных
        inserted_rooms = load_service.load_rooms(db, rooms)
        inserted_students = load_service.load_students(db, students)

        # 3) запросы
        result = {
            "rooms_counts":    query_service.rooms_counts(db),
            "top5_young_avg":  query_service.top5_young_avg(db),
            "top5_age_spread": query_service.top5_age_spread(db),
            "mixed_gender":    query_service.mixed_gender_rooms(db),
            "meta": {"inserted_rooms": inserted_rooms, "inserted_students": inserted_students},
        }

        # 4) экспорт
        exporter.dump(result, out)
        # print короткой сводки
        pass

if __name__ == "__main__":
    app()