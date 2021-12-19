from typing import Dict, Optional
from ..operands import *

class ParseUnaryGet(ParseAtom):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"Get({self.name!r})"

    def is_constant(self) -> bool:
        return False

    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        return variables[self.name]

class ParseUnaryGetString(ParseUnaryGet, ParseString):
    pass
class ParseUnaryGetInteger(ParseUnaryGet, ParseInteger):
    pass
class ParseUnaryGetFloat(ParseUnaryGet, ParseFloat):
    pass
class ParseUnaryGetRegex(ParseUnaryGet, ParseRegex):
    pass
class ParseUnaryGetIPv4(ParseUnaryGet, ParseIPv4):
    pass
class ParseUnaryGetIPv6(ParseUnaryGet, ParseIPv6):
    pass

def find_variable(
        name: str, types: Dict[str, type]
        ) -> Optional[ParseAtom]:

    if types[name] == ParseString:
        return ParseUnaryGetString(name)
    elif types[name] == ParseInteger:
        return ParseUnaryGetInteger(name)
    elif types[name] == ParseFloat:
        return ParseUnaryGetFloat(name)
    elif types[name] == ParseRegex:
        return ParseUnaryGetRegex(name)
    elif types[name] == ParseIPv4:
        return ParseUnaryGetIPv4(name)
    elif types[name] == ParseIPv6:
        return ParseUnaryGetIPv6(name)
    else:
        return None
