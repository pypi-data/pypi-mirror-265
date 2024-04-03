import xml.etree.ElementTree as ET

from .string import String
from .uint import Uint


class Column:
    def __init__(self, f):
        self.type = Uint(f)
        self.name = String(f)

    def xml(self):
        element = ET.Element("Column", attrib={"type": f"{self.type.value}"})
        element.append(self.name.xml())
        return element

    def fbs(self):
        return (
            self.type.fbs()
            + self.name.fbs()
        )
