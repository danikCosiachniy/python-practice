import xml.etree.ElementTree as ET
from app.ports.exporter import Exporter

class XmlExporter(Exporter):
    def dump(self, data: dict, path: str) -> None:
        # root=<result>, для каждой секции <query name="..."><row>...</row></query>
        # строковые значения, None -> ""
        pass