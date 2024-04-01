from pathlib import Path
import xml.etree.ElementTree as ET

import tomli
import tomli_w

from .nodes.indextable import IndexTable
from .nodes.table import Table
from .nodes.row import Row
from .nodes.script import Script


def read_fbs(path: Path) -> IndexTable | Table:
        with open(path, "rb") as f:
            if path.stem == "_fb0x00":
                return IndexTable(f)
            return Table.from_fbs(f)


def write_xml(table: IndexTable | Table, path: Path):
    tree = ET.ElementTree(table.xml())
    ET.indent(tree, space = "  ")
    tree.write(path, encoding="utf8")


def write_fbs(table: IndexTable | Table, path: Path):
    with open(path, "wb") as f:
        f.write(table.fbs())


def write_toml(path: Path, tables: dict[int, Table | IndexTable]):
    npcs = tables[5]
    locale = tables[6]

    print(f"Writing {len(npcs.rows)} TOML files")
    filenames = set()
    for row in npcs.rows:
        script = {
            "UID": row.uid.hex(),
            "Name": row.cells[0].item.uid.hex(),
            "TriggerScript": row.cells[1].item.toml(locale),
            "InitScript": row.cells[2].item.toml(locale),
            "UpdateScript": row.cells[3].item.toml(locale),
            "DefeatedScript": row.cells[4].item.toml(locale),
            "VictoriousScript": row.cells[5].item.toml(locale),
        }
        script = {k: v for k, v in script.items() if v}
        filename = row.cells[-1].item.value.replace('\0', '')

        # Make sure no filename collisions happen!
        while filename.upper() in filenames:
            filename += "_"
        filenames.add(filename.upper())

        with open(path / f"{filename}.toml", "wb") as f:
            tomli_w.dump(script, f, multiline_strings=True)


def get_tomls(path) -> list[Path]:
    return list(sorted(path.glob("**/*.toml")))


def read_toml(path) -> tuple[Table, Table]:
    locale = Table()
    npcs = Table()

    files = get_tomls(path)
    print(f"Reading {len(files)} TOML files")
    for filepath in files:
        with open(filepath, "rb") as f:
            npcs.add(Row.from_script_toml(
                filepath.stem,
                tomli.load(f),
                locale,
            ))
    return npcs, locale


def read_tables(path: Path) -> dict[int, Table | IndexTable]:
    tables = {}
    for filepath in sorted(path.glob("*.fbs")):
        print(f"Reading {filepath}")
        table_id = int(filepath.stem[-1])
        tables[table_id] = read_fbs(filepath)
    return tables


def build(path: Path, fbs: bool, xml: bool, toml: bool, test: bool):
    if test:
        fbs, xml, toml = True, True, True

    FBS_IN = path
    TOML_IN = path / "scripts"
    FBS_OUT = path / "build"
    TOML_OUT = path / "build" / "scripts"

    print(f"Building Data files in {path.resolve()}")

    tables = read_tables(FBS_IN)

    if get_tomls(TOML_IN):
        print("Found TOML scripts, reading them as _fb0x05.fbs and _fb0x06.fbs")
        tables[5], tables[6] = read_toml(TOML_IN)

    if fbs:
        FBS_OUT.mkdir(exist_ok=True)
        for index, table in tables.items():
            out = FBS_OUT / f"_fb0x0{index}.fbs"
            print(f"Writing {out}")
            write_fbs(table, out)
    if xml:
        FBS_OUT.mkdir(exist_ok=True)
        for index, table in tables.items():
            out = FBS_OUT / f"_fb0x0{index}.xml"
            print(f"Writing {out}")
            write_xml(table, out)
    if toml:
        TOML_OUT.mkdir(exist_ok=True)
        write_toml(TOML_OUT, tables)

    if test:
        print("Check tables are not broken")
        read_tables(FBS_OUT)

