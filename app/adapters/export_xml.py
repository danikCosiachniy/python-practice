from datetime import date, datetime, timedelta
from decimal import Decimal
import xml.etree.ElementTree as ET
from app.ports.exporter import Exporter


class XmlExporter(Exporter):
    """
    Реализация экспортера для сохранения данных в формате XML.

    Пример:
        >>> data = {"rooms": [{"id": 1, "name": "Room #1"}]}
        >>> XmlExporter().dump(data, "result.xml")
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
        root = ET.Element("result")

        # Каждый раздел (ключ в словаре) = отдельный <query name="...">
        for section, rows in data.items():
            query_elem = ET.SubElement(root, "query", name=section)

            # Если секция — список записей
            if isinstance(rows, list):
                for row in rows:
                    row_elem = ET.SubElement(query_elem, "row")
                    if isinstance(row, dict):
                        for key, value in row.items():
                            ET.SubElement(row_elem, key).text = self._convert_value(value)
                    else:
                        # если это не dict — просто текстом
                        ET.SubElement(row_elem, "value").text = self._convert_value(row)

            # Если секция — просто словарь (например, meta)
            elif isinstance(rows, dict):
                row_elem = ET.SubElement(query_elem, "row")
                for key, value in rows.items():
                    ET.SubElement(row_elem, key).text = self._convert_value(value)

            # Если секция — одиночное значение
            else:
                ET.SubElement(query_elem, "value").text = self._convert_value(rows)

        # Запись в файл с декларацией XML
        tree = ET.ElementTree(root)
        
        try:
            ET.indent(tree, space="  ", level=0)
        except AttributeError:
            pass  
        tree.write(path, encoding="utf-8", xml_declaration=True)