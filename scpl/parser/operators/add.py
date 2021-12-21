from typing import Dict, Optional
from .common import ParseBinaryOperator
from ..operands import (ParseAtom, ParseFloat, ParseInteger, ParseRegex,
    ParseString)
from .cast import ParseCastStringRegex

class ParseBinaryAddIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(self._left.eval(vars).value + self._right.eval(vars).value)

class ParseBinaryAddFloatFloat(ParseBinaryOperator, ParseFloat):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseFloat:
        return ParseFloat(self._left.eval(vars).value + self._right.eval(vars).value)

class ParseBinaryAddStringString(ParseBinaryOperator, ParseString):
    def __init__(self, left: ParseString, right: ParseString):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseString:
        left = self._left.eval(vars)
        right = self._right.eval(vars)

        delim: Optional[str] = None
        if (left.delimiter is not None
                and left.delimiter == right.delimiter):
            delim = left.delimiter

        return ParseString(delim, left.value + right.value)

class ParseBinaryAddRegexRegex(ParseBinaryOperator, ParseRegex):
    def __init__(self, left: ParseRegex, right: ParseRegex):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseRegex:
        left = self._left.eval(vars)
        right = self._right.eval(vars)

        common_flags = left.flags & right.flags
        regex_1      = left.pattern
        regex_2      = right.pattern

        if uncommon := left.flags - common_flags:
            regex_1 = f"(?{''.join(uncommon)}:{regex_1})"
        if uncommon := right.flags - common_flags:
            regex_2 = f"(?{''.join(uncommon)}:{regex_2})"

        delim: Optional[str] = None
        if (left.delimiter is not None
                and left.delimiter == right.delimiter):
            delim = left.delimiter

        return ParseRegex(delim, regex_1 + regex_2, common_flags)
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
        else:
            return None
    elif isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryAddFloatFloat(left, right)
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
