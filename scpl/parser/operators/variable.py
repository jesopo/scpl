from typing import cast, Dict, Optional, Pattern
from ..operands import (ParseAtom, ParseBool, ParseFloat, ParseIPv4,
    ParseIPv6, ParseInteger, ParseRegex, ParseString)

class ParseVariable(ParseAtom):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        type = self.__class__.__name__.replace("ParseVariable", "", 1)
        return f"Get{type}({self.name!r})"

    def is_constant(self) -> bool:
        return False

class ParseVariableString(ParseVariable, ParseString):
    def eval(self, vars: Dict[str, ParseAtom]) -> str:
        return cast(ParseString, vars[self.name]).value
class ParseVariableInteger(ParseVariable, ParseInteger):
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return cast(ParseInteger, vars[self.name]).value
class ParseVariableFloat(ParseVariable, ParseFloat):
    def eval(self, vars: Dict[str, ParseAtom]) -> float:
        return cast(ParseFloat, vars[self.name]).value
class ParseVariableRegex(ParseVariable, ParseRegex):
    def eval(self, vars: Dict[str, ParseAtom]) -> Pattern:
        return cast(ParseRegex, vars[self.name]).eval(vars)
class ParseVariableBool(ParseVariable, ParseBool):
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        return cast(ParseBool, vars[self.name]).value
class ParseVariableIPv4(ParseVariable, ParseIPv4):
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseIPv4:
        return cast(ParseIPv4, vars[self.name])
class ParseVariableIPv6(ParseVariable, ParseIPv6):
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseIPv6:
        return cast(ParseIPv6, vars[self.name])

def find_variable(name: str, var_type: type) -> Optional[ParseAtom]:
    if var_type == ParseString:
        return ParseVariableString(name)
    elif var_type == ParseInteger:
        return ParseVariableInteger(name)
    elif var_type == ParseFloat:
        return ParseVariableFloat(name)
    elif var_type == ParseRegex:
        return ParseVariableRegex(name)
    elif var_type == ParseBool:
        return ParseVariableBool(name)
    elif var_type == ParseIPv4:
        return ParseVariableIPv4(name)
    elif var_type == ParseIPv6:
        return ParseVariableIPv6(name)
    else:
        return None
