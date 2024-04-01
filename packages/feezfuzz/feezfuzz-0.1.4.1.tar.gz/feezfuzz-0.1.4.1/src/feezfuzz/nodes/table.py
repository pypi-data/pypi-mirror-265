import re
import xml.etree.ElementTree as ET

from .row import Row
from .uint import Uint
from .uuid import Uuid


class Table:
    def __init__(self, rows=None):
        if rows == None:
            rows = []
        self.rows = rows

    @classmethod
    def from_fbs(cls, f):
        return cls(
            [Row.from_fbs(f) for index in range(Uint(f).value)]
        )

    def xml(self):
        element = ET.Element("Table")
        for row in self.rows:
            element.append(row.xml())
        return element

    def fbs(self):
        return (
            Uint(len(self.rows)).fbs()
            + b"".join(item.fbs() for item in self.rows)
        )

    def get_text(self, uid):
        for row in self.rows:
            if row.uid.value == int(uid, 16):
                return row.cells[0].item.value
        print(f"Malformed DB: text uid {uid} missing")
        return self.rows[0].cells[0].item.value

    def get_toml_text(self, uid):
        text = self.get_text(uid)
        sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
        if not len(re.findall(r"[\.\?\!] ", text)):
            return f"<{' '.join(sentences)}>"
        sentences = "\n    ".join(sentences)
        return f"<\n    {sentences}\n>"

    def add(self, row):
        self.rows.append(row)

    def register_text(self, text: str, npc_id: int) -> Uuid:
        for row in self.rows:
            if row.cells[0].item.value == text:
                return row.uid
        uuid = self.new_uid()
        self.add(Row.new_text(uuid.uid, text, npc_id))
        return uuid

    def new_uid(self) -> Uuid:
        table_suffix = "5"
        hex_len = Uint(len(self.rows)).hex()
        if hex_len[0] != "0":
            raise IndexError("Too many uids in table")
        uid_str = hex_len[1:] + table_suffix
        return Uuid(uid_str)
