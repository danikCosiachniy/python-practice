import xml.etree.ElementTree as ET
from app.ports.exporter import Exporter


class XmlExporter(Exporter):
    """
    Реализация экспортера для сохранения данных в формате XML.

    Пример:
        >>> data = {"rooms": [{"id": 1, "name": "Room #1"}]}
        >>> XmlExporter().dump(data, "result.xml")
    """

    def dump(self, data: dict, path: str) -> None:
        root = ET.Element("result")

        for section, rows in data.items():
            query_elem = ET.SubElement(root, "query", name=section)
            for row in rows:
                row_elem = ET.SubElement(query_elem, "row")
                for key, value in row.items():
                    ET.SubElement(row_elem, key).text = str(value) if value is not None else ""

        tree = ET.ElementTree(root)
        tree.write(path, encoding="utf-8", xml_declaration=True)