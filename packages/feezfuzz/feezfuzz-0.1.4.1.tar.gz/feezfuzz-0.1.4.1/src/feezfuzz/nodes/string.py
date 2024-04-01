import io
import struct
import xml.etree.ElementTree as ET

from .uint import Uint


ENCODING = "cp1251"


class String:
    def __init__(self, f):
        if isinstance(f, io.IOBase):
            # pascal-like. the first 4 bytes are string length. not null terminated.
            length = Uint(f).value
            self.value = (
                struct.unpack(f"<{length}s", f.read(length))[0]
                .decode(ENCODING, "replace")
                .replace("\0", "")
            )
        elif isinstance(f, str):
            self.value = f
        else:
            raise TypeError(type(f))

    def xml(self):
        element = ET.Element("String")
        element.text = self.value
        return element

    def fbs(self):
        value = self.value + "\0"
        length = len(value)
        return (
            Uint(length).fbs()
            + struct.pack(f"<{length}s", value.encode(ENCODING))
        )
