from typing import Dict
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseRegex, ParseString

class ParseBinaryMatchStringRegex(ParseBinaryOperator, ParseString):
    def __init__(self, left: ParseString, right: ParseRegex):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Match({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseString:
        reference = self._left.eval(vars).value
        match = self._right.eval(vars).compiled.search(reference)
        if match is not None:
            return ParseString(None, match.group(0))
        else:
            return ParseString(None, "")

def find_binary_match(left: ParseAtom, right: ParseAtom):
    if isinstance(left, ParseString):
        if isinstance(right, ParseRegex):
            return ParseBinaryMatchStringRegex(left, right)
        else:
            return None
    else:
        return None
