import io
import struct
import xml.etree.ElementTree as ET


class Uint:
    def __init__(self, f):
        if isinstance(f, io.IOBase):
            self.value = struct.unpack("<I", f.read(4))[0]
        elif isinstance(f, str):
            try:
                self.value = int(f)
            except ValueError:
                self.value = 0
                print(f"Warning: Malformed integer: {f}")
        elif isinstance(f, int):
            self.value = f
        else:
            raise TypeError(type(f))

    def xml(self):
        element = ET.Element("Uint")
        element.text = f"{self.value}"
        return element

    def fbs(self):
        return struct.pack("<I", self.value)

    def hex(self):
        return hex(self.value).upper()[2:].zfill(8)
