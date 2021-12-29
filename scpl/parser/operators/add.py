import re
from typing import Dict, Optional, Pattern
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseFloat, ParseInteger, ParseRegex, ParseString
from .cast import ParseCastIntegerFloat, ParseCastStringRegex

class ParseBinaryAddIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return self._left.eval(vars) + self._right.eval(vars)

class ParseBinaryAddFloatFloat(ParseBinaryOperator, ParseFloat):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> float:
        return self._left.eval(vars) + self._right.eval(vars)
class ParseBinaryAddFloatInteger(ParseBinaryAddFloatFloat):
    def __init__(self, left: ParseFloat, right: ParseInteger):
        super().__init__(left, ParseCastIntegerFloat(right))
class ParseBinaryAddIntegerFloat(ParseBinaryAddFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseFloat):
        super().__init__(ParseCastIntegerFloat(left), right)

class ParseBinaryAddStringString(ParseBinaryOperator, ParseString):
    def __init__(self, left: ParseString, right: ParseString):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> str:
        return self._left.eval(vars) + self._right.eval(vars)

def _reflags(flags: int):
    sflags = ""
    if flags & re.I:
        sflags += "i"
    return sflags

class ParseBinaryAddRegexRegex(ParseBinaryOperator, ParseRegex):
    def __init__(self, left: ParseRegex, right: ParseRegex):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> Pattern:
        left = self._left.eval(vars)
        right = self._right.eval(vars)

        common_flags = left.flags & right.flags
        regex_1      = left.pattern
        regex_2      = right.pattern

        if uncommon := left.flags - common_flags:
            regex_1 = f"(?{_reflags(uncommon)}:{regex_1})"
        if uncommon := right.flags - common_flags:
            regex_2 = f"(?{_reflags(uncommon)}:{regex_2})"

        return re.compile(regex_1 + regex_2, common_flags)
class ParseBinaryAddRegexString(ParseBinaryAddRegexRegex):
    def __init__(self, left: ParseRegex, right: ParseString):
        super().__init__(left, ParseCastStringRegex(right))
class ParseBinaryAddStringRegex(ParseBinaryAddRegexRegex):
    def __init__(self, left: ParseString, right: ParseRegex):
        super().__init__(ParseCastStringRegex(left), right)

def find_binary_add(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger):
        if isinstance(right, ParseInteger):
            return ParseBinaryAddIntegerInteger(left, right)
        elif isinstance(right, ParseFloat):
            return ParseBinaryAddIntegerFloat(left, right)
        else:
            return None
    elif isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryAddFloatFloat(left, right)
        elif isinstance(right, ParseInteger):
            return ParseBinaryAddFloatInteger(left, right)
        else:
            return None
    elif isinstance(left, ParseString):
        if isinstance(right, ParseString):
            return ParseBinaryAddStringString(left, right)
        elif isinstance(right, ParseRegex):
            return ParseBinaryAddStringRegex(left, right)
        else:
            return None
    elif isinstance(left, ParseRegex):
        if isinstance(right, ParseRegex):
            return ParseBinaryAddRegexRegex(left, right)
        elif isinstance(right, ParseString):
            return ParseBinaryAddRegexString(left, right)
        else:
            return None
    else:
        return None
