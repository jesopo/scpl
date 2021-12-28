from typing import Dict
from .casemapped import ParseUnaryCasemappedRegex, ParseUnaryCasemappedString
from .common import ParseBinaryOperator
from .complement import ParseUnaryComplementRegex
from ..operands import ParseAtom, ParseBool, ParseRegex, ParseString

class ParseBinaryMatchStringUnregex(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseString, right: ParseRegex):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Match({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        reference = self._left.eval(vars).value
        regex = self._right.eval(vars)
        match = bool(regex.compiled.search(reference))
        return ParseBool(match == regex.expected)

class ParseBinaryMatchStringRegex(ParseBinaryOperator, ParseString):
    def __init__(self, left: ParseString, right: ParseRegex):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Match({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseString:
        reference = self._left.eval(vars).value
        regex = self._right.eval(vars)
        match = regex.compiled.search(reference)
        if match is not None and regex.expected:
            return ParseString(None, match.group(0))
        else:
            return ParseString(None, "")

def find_binary_match(left: ParseAtom, right: ParseAtom):
    if isinstance(right, ParseUnaryComplementRegex):
        if isinstance(left, ParseUnaryCasemappedString):
            c_right = ParseUnaryCasemappedRegex(right, left.table)
            return ParseBinaryMatchStringUnregex(left, c_right)
        elif isinstance(left, ParseString):
            return ParseBinaryMatchStringUnregex(left, right)
    elif isinstance(right, ParseRegex):
        if isinstance(left, ParseUnaryCasemappedString):
            c_right = ParseUnaryCasemappedRegex(right, left.table)
            return ParseBinaryMatchStringRegex(left, c_right)
        elif isinstance(left, ParseString):
            return ParseBinaryMatchStringRegex(left, right)
        else:
            return None
    else:
        return None
