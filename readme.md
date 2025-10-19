Отлично 🔥 — вот твой полностью оформленный README.md в современном GitHub-стиле.
Он оформлен аккуратно, с заголовками, цветными блоками кода, значками и примерами вывода.
Сразу готов для публикации в репозитории.

⸻

🧩 University Data Processor

Автоматическая система анализа данных студентов и комнат общежития


⸻

📘 Описание проекта

University Data Processor — это Python-приложение, которое:
	•	импортирует данные о студентах и комнатах из JSON;
	•	записывает их в базу PostgreSQL;
	•	выполняет аналитические SQL-запросы;
	•	экспортирует результаты в формат JSON или XML.

Проект реализован по принципам чистой архитектуры (Ports & Adapters) и следует стандартам SOLID, PEP8 и PEP257.

⸻

⚙️ Стек технологий

Компонент	Технология
Язык	Python 3.11+
База данных	PostgreSQL
Работа с SQL	psycopg2 (без ORM)
Форматы	JSON, XML
Контейнеризация	Docker + Docker Compose
Логирование	logging (файл /logs/app.log)
Тестирование	unittest
Анализ кода	pylint, flake8


⸻

🧱 Архитектура

app/
├── adapters/       # подключаемые модули
│   ├── postgres_db.py     # работа с PostgreSQL
│   ├── export_json.py     # экспорт в JSON
│   └── export_xml.py      # экспорт в XML
│
├── cli/
│   └── main.py            # точка входа CLI
│
├── domain/
│   └── entities.py        # классы Room и Student + валидация JSON
│
├── ports/
│   ├── db.py              # интерфейс DB
│   └── exporter.py        # интерфейс Exporter
│
├── services/
│   ├── load_service.py    # загрузка JSON → БД
│   ├── query_service.py   # аналитические SQL-запросы
│   └── schema_service.py  # инициализация схемы и индексов
⸻

🚀 Как запустить проект

🔧 1. Запуск локально

# 1. Создай и активируй виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 2. Установи зависимости
pip install -r requirements.txt

# 3. Запусти приложение
python -m app.cli.main


⸻

🐳 2. Запуск через Docker

🔹 Собрать и запустить контейнеры

docker compose up --build

🔹 Проверить статус

docker compose ps

🔹 Остановить контейнеры

docker compose down


⸻

🧩 Пример работы

▶️ Консоль

Введите путь до файла студентов (JSON):
data/JSON/students.json
Введите путь до файла комнат (JSON):
data/JSON/rooms.json
Введите выходной формат (xml или json):
json
Введите название файла для выгрузки результата:
result

🧮 SQL-запросы, выполняемые приложением

Название	Описание
SQL_ROOMS_COUNT	Количество студентов по комнатам
SQL_TOP5_YOUNG_AVG	5 комнат с самым молодым средним возрастом
SQL_TOP5_AGE_SPREAD	5 комнат с максимальной разницей в возрасте
SQL_MIXED_GENDER	Комнаты, где живут студенты разных полов


⸻

💾 Пример результата (result.json)

{
  "count_student_in_rooms": [
    {"id": 101, "name": "Room #101", "count": 3}
  ],
  "top5_young_avg": [
    {"id": 111, "name": "Room #111", "avg_age_years": 22.6}
  ],
  "top5_age_spread": [
    {"id": 105, "name": "Room #105", "diff_age_years": 30.1}
  ],
  "rooms_with_mixed_gender": [
    {"id": 120, "name": "Room #120"}
  ],
  "meta": {
    "inserted_rooms": 1000,
    "inserted_students": 9999
  }
}


⸻

🧰 Настройка окружения (.env)

POSTGRES_USER=app
POSTGRES_PASSWORD=app
POSTGRES_DB=university
POSTGRES_PORT=5432
POSTGRES_HOST=db


⸻

🧪 Тестирование

▶️ Запуск всех тестов

python tests/test.py

▶️ Запуск тестов в Docker

docker compose run --rm app python tests/test.py

📦 Структура тестов

tests/
├── fake_db.py
├── test_entities.py
├── test_load_service.py
├── test_query_service.py
├── test_exporters.py
├── test_schema_service.py
└── test.py

Все тесты используют библиотеку unittest, охватывают валидацию данных, загрузку, запросы и экспорт.

⸻

🧾 Логирование
	•	Все события записываются в файл logs/app.log
	•	Пример:

2025-10-19 21:08:43 [INFO] app.cli.main: Программа запущена
2025-10-19 21:08:44 [WARNING] app.domain.entities: Пропущена комната — отсутствует поле 'id'
2025-10-19 21:08:45 [ERROR] app.services.query_service: Ошибка SQL при rooms_counts



⸻

📂 Пример SQL-файлов

sql/schema_pg.sql

CREATE TABLE IF NOT EXISTS rooms (
    id INT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    sex CHAR(1) CHECK (sex IN ('M', 'F')),
    birthday DATE NOT NULL,
    room_id INT REFERENCES rooms(id)
);

sql/indexes_pg.sql

CREATE INDEX IF NOT EXISTS idx_students_room_id ON students(room_id);
CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);


⸻

🧠 Качество кода

✅ PEP8 и PEP257 совместимо
✅ Pylint без ошибок (10/10)
✅ Глубина вложенности ≤5
✅ Docstring в каждом модуле

⸻

📊 Тестовое покрытие

Модуль	Описание
entities.py	Проверка конвертации JSON в объекты
load_service.py	Тесты загрузки и батчинга
query_service.py	Проверка SQL-запросов
export_json/xml.py	Проверка сериализации и структуры
schema_service.py	Проверка чтения и исполнения SQL


⸻

🧑‍💻 Автор

Шумкевич Данила Александрович
📧 danila.shumkevich@innowise.com
🌍 master-cube.ru

⸻

🪪 Лицензия

MIT License — свободное использование, модификация и распространение
с указанием автора и ссылки на репозиторий.

⸻