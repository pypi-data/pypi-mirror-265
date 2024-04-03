import xml.etree.ElementTree as ET

from .column import Column
from .uint import Uint


class IndexTable:
    def __init__(self, f):
        self.value = [Column(f) for index in range(Uint(f).value)]

    def xml(self):
        element = ET.Element("IndexTable")
        for item in self.value:
            element.append(item.xml())
        return element

    def fbs(self):
        return (
            Uint(len(self.value)).fbs()
            + b"".join(item.fbs() for item in self.value)
        )
