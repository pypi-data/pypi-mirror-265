import xml.etree.ElementTree as ET

from .byte import Byte
from .ushort import Ushort
from ..enums import (
    SLOT_NAMES,
    SPELL_CLASSES,
)

class Level:
    def __init__(self, f):
        byte = Byte(f).value
        self.first = byte & 0x0F
        self.second = byte >> 4
        byte = Byte(f).value
        self.third = byte & 0x0F
        self.slot = byte >> 4
        self.level = Ushort(f)

    def xml(self):
        element = ET.Element("Level")
        if self.level.value == 65535:
            return element
        element.append(ET.Element("Nibble", text=f"{SPELL_CLASSES[self.first]}"))
        element.append(ET.Element("Nibble", text=f"{SPELL_CLASSES[self.second]}"))
        element.append(ET.Element("Nibble", text=f"{SPELL_CLASSES[self.third]}"))
        element.append(ET.Element("Nibble", text=f"{SLOT_NAMES[self.slot]}"))
        element.append(self.level.xml())
        return element

    def fbs(self):
        return (
            Byte(self.first & self.second << 4).fbs()
            + Byte(self.third & self.slot << 4).fbs()
            + self.level.fbs()
        )
