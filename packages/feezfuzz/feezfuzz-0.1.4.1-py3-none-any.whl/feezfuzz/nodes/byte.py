import io
import struct
import xml.etree.ElementTree as ET


class Byte:
    def __init__(self, f):
        if isinstance(f, io.IOBase):
            self.value = struct.unpack("<B", f.read(1))[0]
        elif isinstance(f, int):
            self.value = f
        else:
            raise TypeError(f)

    def xml(self):
        element = ET.Element("Byte")
        element.text = f"{self.value}"
        return element

    def fbs(self):
        return struct.pack("<B", self.value)
