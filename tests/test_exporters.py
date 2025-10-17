import unittest, tempfile, os, json
from datetime import date, timedelta
from xml.etree import ElementTree as ET
from app.adapters.export_json import JsonExporter
from app.adapters.export_xml import XmlExporter

class TestExporters(unittest.TestCase):
    def setUp(self):
        self.data = {
            "rooms_counts": [{"id": 1, "name": "Room #1", "cnt": 2}],
            "meta": {"today": date(2025, 10, 10), "span": timedelta(days=1, hours=6)},
        }

    def test_json_export(self):
        f = tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json")
        f.close()
        try:
            JsonExporter().dump(self.data, f.name)
            loaded = json.loads(open(f.name, encoding="utf-8").read())
            self.assertIn("rooms_counts", loaded)
            self.assertIsInstance(loaded["meta"]["span"], float)  # timedelta → float days
        finally:
            os.unlink(f.name)

    def test_xml_export(self):
        f = tempfile.NamedTemporaryFile("w+", delete=False, suffix=".xml")
        f.close()
        try:
            XmlExporter().dump(self.data, f.name)
            root = ET.parse(f.name).getroot()
            self.assertEqual("result", root.tag)
            queries = root.findall("query")
            self.assertTrue(queries)
        finally:
            os.unlink(f.name)

if __name__ == "__main__":
    unittest.main()