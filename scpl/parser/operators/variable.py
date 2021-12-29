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
        return cast(ParseString, vars[self.name]).eval(vars)
class ParseVariableInteger(ParseVariable, ParseInteger):
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return cast(ParseInteger, vars[self.name]).eval(vars)
class ParseVariableFloat(ParseVariable, ParseFloat):
    def eval(self, vars: Dict[str, ParseAtom]) -> float:
        return cast(ParseFloat, vars[self.name]).eval(vars)
class ParseVariableRegex(ParseVariable, ParseRegex):
    def eval(self, vars: Dict[str, ParseAtom]) -> Pattern:
        return cast(ParseRegex, vars[self.name]).eval(vars)
class ParseVariableBool(ParseVariable, ParseBool):
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        return cast(ParseBool, vars[self.name]).eval(vars)
class ParseVariableIPv4(ParseVariable, ParseIPv4):
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return cast(ParseIPv4, vars[self.name]).eval(vars)
class ParseVariableIPv6(ParseVariable, ParseIPv6):
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return cast(ParseIPv6, vars[self.name]).eval(vars)

def find_variable(name: str, var_type: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(var_type, ParseString):
        return ParseVariableString(name)
    elif isinstance(var_type, ParseInteger):
        return ParseVariableInteger(name)
    elif isinstance(var_type, ParseFloat):
        return ParseVariableFloat(name)
    elif isinstance(var_type, ParseRegex):
        return ParseVariableRegex(name)
    elif isinstance(var_type, ParseBool):
        return ParseVariableBool(name)
    elif isinstance(var_type, ParseIPv4):
        return ParseVariableIPv4(name)
    elif isinstance(var_type, ParseIPv6):
        return ParseVariableIPv6(name)
    else:
        return None
