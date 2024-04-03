import re
import xml.etree.ElementTree as ET

from ..enums import INSTRUCTIONS


def Text(x, locale):
    int(x, 16) # check if string is hex value
    return locale.get_toml_text(x)


def Uid(x):
    try:
        int(x, 16) # check if string is hex value
    except ValueError:
        print(f"Malformed DB: {x} is not a valid UID")
    return x


def Int(x):
    try:
        int(x) # check if string is int
    except ValueError:
        print(f"Malformed DB: {x} is not an integer")
    return x


def String(x):
    return x



SHORT =         [char           for (char, string, args) in INSTRUCTIONS]
LONG =          [string         for (char, string, args) in INSTRUCTIONS]
SHORT_TO_LONG = {char: string   for (char, string, args) in INSTRUCTIONS}
LONG_TO_SHORT = {string: char   for (char, string, args) in INSTRUCTIONS}
ARGTYPES =      {char: args     for (char, string, args) in INSTRUCTIONS}


class Command:
    def __init__(self, string, longform: bool = False):
        self.args = []
        self.instruction = None

        if string := string.replace("\0", ""):
            self.args = string.split(".")
            self.instruction = self.parse_instruction(self.args.pop(0), longform)
            arglen = len(ARGTYPES[self.instruction])

            if len(self.args) != arglen:
                # Suppress warnings for commands of format "J.textid":
                # they are used extensively by vanilla
                if (self.instruction != "J" and len(self.args) != 1):
                    print(f"Malformed DB: command {string.encode()}: {len(self.args)} args given, {arglen} expected")

            # pad missing arguments with zeroes, if needed
            self.args = (self.args + ["0", "0", "0"])[:arglen]
            self.parse_args()

    def parse_instruction(self, string: str, longform: bool) -> str:
        if string in LONG:
            return LONG_TO_SHORT[string]

        if longform:
            # Instructions are supposed to be strings.
            # An incorrect string is likely a typo or
            # An upper/lowercase error.
            longs_lower = [*map(str.lower, LONG)]
            if string.lower() in longs_lower:
                print(f"Malformed DB: command {string.encode()}: command name is capitalised incorrectly")
                return SHORT[longs_lower.index(string.lower())]
            raise ValueError(f"Malformed DB: {string.encode()}")

        # Instructions are supposed to be characters.
        # An incorrect string is likely a char + extra junk
        if len(string) != 1:
            print(f"Malformed DB: command {string.encode()}: command name not a single char")
            string = string[0]
        if string in SHORT:
            return string
        raise ValueError(f"Malformed DB: {string.encode()} not a valid instruction")

    def parse_args(self):
        argtypes = ARGTYPES[self.instruction]

        # deployNpcAtTrigger: special case, has two possible argtypes
        if self.instruction == "P" and self.args[1] in ("0", "1"):
            argtypes = ["int", "int"]

        parsed = []
        for argtype, arg in zip(argtypes, self.args):
            if argtype == "int":
                parsed.append(Int(arg))
            elif argtype == "str":
                parsed.append(String(arg))
            elif "id" in argtype:
                parsed.append(Uid(arg))
            else:
                raise ValueError("Unsupported arg type: {argtype} {arg}")

    def xml(self):
        return ET.Element("Command", text=self.string())

    def toml(self, locale):
        if not self.instruction:
            return ""
        args = []
        argtypes = ARGTYPES[self.instruction]
        for argtype, arg in zip(argtypes, self.args):
            if argtype == "id6":
                args.append(locale.get_toml_text(arg))
            else:
                args.append(arg)
        return ".".join([SHORT_TO_LONG[self.instruction], *args])

    def string(self):
        if not self.instruction:
            return ""
        return ".".join([self.instruction, *self.args])
