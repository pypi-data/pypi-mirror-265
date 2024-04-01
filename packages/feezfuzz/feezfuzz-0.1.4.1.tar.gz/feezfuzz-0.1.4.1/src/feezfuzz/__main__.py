import argparse
import os.path
from pathlib import Path

from .build import build


def dir_path(path):
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError(f"{path} is not a valid path")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Feezfuzz",
        description="A WIP build system for Zanzarah's Data files.",
    )
    parser.add_argument(
        "--fbs",
        action="store_true",
        default=True,
        help="Export all tables to fbs",
    )
    parser.add_argument(
        "--xml",
        action="store_true",
        default=False,
        help="Export all tables to xml",
    )
    parser.add_argument(
        "--toml",
        action="store_true",
        default=False,
        help="Export NPCs and Dialogs to toml",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        default=False,
        help="Test all functionality",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=dir_path,
        default=".",
        help="Data files directory",
    )
    args = parser.parse_args()
    build(Path(args.path), args.fbs, args.xml, args.toml, args.test)
