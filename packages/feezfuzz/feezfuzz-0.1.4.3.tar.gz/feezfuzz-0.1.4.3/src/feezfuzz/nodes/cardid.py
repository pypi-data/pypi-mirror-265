import xml.etree.ElementTree as ET

from .byte import Byte
from .ushort import Ushort
from ..enums import CARD_TYPES


class CardId:
    def __init__(self, f):
        Byte(f) # always 0xff
        self.type = Byte(f)
        self.id = Ushort(f)

    def xml(self):
        element = ET.Element("CardId", attrib={"type": f"{CARD_TYPES[self.type.value]}"})
        element.append(self.id.xml())
        return element

    def fbs(self):
        return (
            Byte(0).fbs()
            + self.type.fbs()
            + self.id.fbs()
        )
