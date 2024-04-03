import io
import xml.etree.ElementTree as ET

from .uint import Uint
from ..enums import UUID_TYPES


class Uuid:
    def __init__(self, f):
        if isinstance(f, io.IOBase):
            self.uid = Uint(f)
            self.type = Uint(f)
        elif isinstance(f, str):
            self.uid = Uint(str(int(f, 16)))
            self.type = Uint("1242636") # impossible to correctly determine?
        else:
            raise TypeError(type(f))

    def xml(self):
        element = ET.Element("Uuid", attrib={"type": f"{UUID_TYPES[self.type.value]}"})
        element.text = self.uid.hex()
        return element

    def fbs(self):
        return self.uid.fbs() + self.type.fbs()

    def hex(self):
        return self.uid.hex()
