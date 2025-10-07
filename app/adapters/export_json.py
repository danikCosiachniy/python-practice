import json
from app.ports.exporter import Exporter

class JsonExporter(Exporter):
    def dump(self, data: dict, path: str) -> None:
        # json.dump(data, file, ensure_ascii=False, indent=2)
        pass