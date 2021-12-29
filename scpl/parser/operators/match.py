from typing import Dict
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseBool, ParseRegex, ParseString

class ParseBinaryMatchStringRegex(ParseBinaryOperator, ParseString):
    def __init__(self, left: ParseString, right: ParseRegex):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Match({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> str:
        reference = self._left.eval(vars)
        regex = self._right.eval(vars)
        match = regex.search(reference)

        if match is not None:
            return match.group(0)
        else:
            return ""

def find_binary_match(left: ParseAtom, right: ParseAtom):
    if isinstance(right, ParseRegex) and isinstance(left, ParseString):
        return ParseBinaryMatchStringRegex(left, right)
    else:
        return None
