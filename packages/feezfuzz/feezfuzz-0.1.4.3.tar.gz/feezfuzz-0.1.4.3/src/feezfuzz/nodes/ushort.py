import struct
import xml.etree.ElementTree as ET


class Ushort:
    def __init__(self, f):
        self.value = struct.unpack("<H", f.read(2))[0]

    def xml(self):
        element = ET.Element("Ushort")
        element.text = f"{self.value}"
        return element

    def fbs(self):
        return struct.pack("<H", self.value)
