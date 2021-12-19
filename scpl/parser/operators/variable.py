from typing import cast, Dict, Optional
from ..operands import *

class ParseVariable(ParseAtom):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        type = self.__class__.__name__.replace("ParseVariable", "", 1)
        return f"Get{type}({self.name!r})"

    def is_constant(self) -> bool:
        return False

class ParseVariableString(ParseVariable, ParseString):
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseString:
        return cast(ParseString, variables[self.name])
class ParseVariableInteger(ParseVariable, ParseInteger):
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseInteger:
        return cast(ParseInteger, variables[self.name])
class ParseVariableFloat(ParseVariable, ParseFloat):
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseFloat:
        return cast(ParseFloat, variables[self.name])
class ParseVariableRegex(ParseVariable, ParseRegex):
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseRegex:
        return cast(ParseRegex, variables[self.name])
class ParseVariableIPv4(ParseVariable, ParseIPv4):
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseIPv4:
        return cast(ParseIPv4, variables[self.name])
class ParseVariableIPv6(ParseVariable, ParseIPv6):
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseIPv6:
        return cast(ParseIPv6, variables[self.name])

def find_variable(
        name: str, types: Dict[str, type]
        ) -> Optional[ParseAtom]:

    if types[name] == ParseString:
        return ParseVariableString(name)
    elif types[name] == ParseInteger:
        return ParseVariableInteger(name)
    elif types[name] == ParseFloat:
        return ParseVariableFloat(name)
    elif types[name] == ParseRegex:
        return ParseVariableRegex(name)
    elif types[name] == ParseIPv4:
        return ParseVariableIPv4(name)
    elif types[name] == ParseIPv6:
        return ParseVariableIPv6(name)
    else:
        return None
