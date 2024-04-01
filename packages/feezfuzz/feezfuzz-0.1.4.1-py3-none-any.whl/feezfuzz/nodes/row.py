import xml.etree.ElementTree as ET

from .cell import Cell
from .uint import Uint
from .uuid import Uuid
from .script import Script
from .string import String


class Row:
    def __init__(self, uid, cells):
        self.uid = uid
        self.cells = cells

    @classmethod
    def from_fbs(cls, f):
        uid = Uint(f)
        cells = [Cell.from_fbs(f) for index in range(Uint(f).value)]
        return cls(uid, cells)

    def xml(self):
        element = ET.Element("Row", attrib={"uid": f"{self.uid.hex()}"})
        for item in self.cells:
            element.append(item.xml())
        return element

    def fbs(self):
        return (
            self.uid.fbs()
            + Uint(len(self.cells)).fbs()
            + b"".join(item.fbs() for item in self.cells)
        )

    @classmethod
    def from_script_toml(
            cls,
            filename: str,
            data: dict,
            locale: "Table",
        ):
        script = {
            1: data["TriggerScript"] if "TriggerScript" in data else "",
            2: data["InitScript"] if "InitScript" in data else "",
            3: data["UpdateScript"] if "UpdateScript" in data else "",
            4: data["DefeatedScript"] if "DefeatedScript" in data else "",
            5: data["VictoriousScript"] if "VictoriousScript" in data else "",
        }
        return cls(
            Uuid(data["UID"]).uid,
            [
                Cell(Uint(3), Uint(3), Uuid(data["Name"])),
                Cell(Uint(0), Uint(24), Script.from_toml(script[1], locale, data["Name"])),
                Cell(Uint(0), Uint(25), Script.from_toml(script[2], locale, data["Name"])),
                Cell(Uint(0), Uint(26), Script.from_toml(script[3], locale, data["Name"])),
                Cell(Uint(0), Uint(27), Script.from_toml(script[4], locale, data["Name"])),
                Cell(Uint(0), Uint(28), Script.from_toml(script[5], locale, data["Name"])),
                Cell(Uint(0), Uint(19), String(filename)),
            ],
        )

    @classmethod
    def new_text(
            cls,
            uid: Uint,
            text: str,
            npc_id: int,
        ):
        return cls(
            uid,
            [
                Cell(Uint(0), Uint(0), String(text)),
                Cell(Uint(1), Uint(29), Uint(npc_id)),
                Cell(Uint(0), Uint(30), String("")),
            ],
        )
