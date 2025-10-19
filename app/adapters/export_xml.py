"""
Экспортер XML.

Предоставляет `XmlExporter`, который преобразует словари и списки
в корректно сформированный XML-документ.

Возможности:
- Поддержка вложенных структур и разделов метаданных.
- Преобразование специальных типов (дата, десятичное число, дельта времени) в строки.
- Формирование форматированного (с отступом) XML-вывода с заголовком объявления.
"""
from datetime import date, datetime, timedelta
from decimal import Decimal
import logging
import xml.etree.ElementTree as ET
from app.ports.exporter import Exporter

logger = logging.getLogger(__name__)

class XmlExporter(Exporter):
    """
    Реализация экспортера для сохранения данных в формате XML.

    Пример:
        >>> data = {
        ...     "rooms": [{"id": 1, "name": "Room #1"}],
        ...     "students": [{"id": 5, "name": "Alice"}]
        ... }
        >>> XmlExporter().dump(data, "result.xml")

    Результат:
        <?xml version="1.0" encoding="utf-8"?>
        <result>
            <query name="rooms">
                <row>
                    <id>1</id>
                    <name>Room #1</name>
                </row>
            </query>
            <query name="students">
                <row>
                    <id>5</id>
                    <name>Alice</name>
                </row>
            </query>
        </result>
    """

    def _convert_value(self, value):
        """Преобразует сложные типы (date, Decimal, timedelta и т.д.) в строки."""
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        if isinstance(value, timedelta):
            # переводим в дни (с дробной частью)
            return str(round(value.total_seconds() / 86400.0, 4))
        if isinstance(value, Decimal):
            return str(float(value))
        if isinstance(value, (list, tuple)):
            return ", ".join(str(self._convert_value(v)) for v in value)
        if isinstance(value, dict):
            # рекурсивно преобразуем словарь в плоскую строку key=value
            return ", ".join(f"{k}={self._convert_value(v)}" for k, v in value.items())
        return str(value) if value is not None else ""

    def dump(self, data: dict, path: str) -> None:
        """Сохраняет данные в XML-файл."""
        logger.info("Экспорт данных в XML")
        try:
            root = ET.Element("result")

            # Каждый раздел (ключ в словаре) = отдельный <query name="...">
            total_records = 0
            for section, rows in data.items():
                query_elem = ET.SubElement(root, "query", name=section)

                if isinstance(rows, list):
                    for row in rows:
                        row_elem = ET.SubElement(query_elem, "row")
                        total_records += 1
                        if isinstance(row, dict):
                            for key, value in row.items():
                                ET.SubElement(row_elem, key).text = self._convert_value(value)
                        else:
                            ET.SubElement(row_elem, "value").text = self._convert_value(row)

                elif isinstance(rows, dict):
                    row_elem = ET.SubElement(query_elem, "row")
                    total_records += 1
                    for key, value in rows.items():
                        ET.SubElement(row_elem, key).text = self._convert_value(value)

                else:
                    ET.SubElement(query_elem, "value").text = self._convert_value(rows)
                    total_records += 1

            # Запись в файл
            tree = ET.ElementTree(root)
            try:
                ET.indent(tree, space="  ", level=0)
            except AttributeError:
                pass  # Python < 3.9
            tree.write(path, encoding="utf-8", xml_declaration=True)

            logger.info("XML экспорт завершён")

        except Exception as e:
            logger.error("При экспорте XML (%s): %s", path, e)
            raise
