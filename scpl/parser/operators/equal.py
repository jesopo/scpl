from typing import Dict, Optional
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseBool, ParseInteger

class ParseBinaryEqualBoolBool(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseBool, right: ParseBool):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Equal({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(self._left.eval(vars).value == self._right.eval(vars).value)

class ParseBinaryEqualIntegerInteger(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Equal({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(self._left.eval(vars).value == self._right.eval(vars).value)

def find_binary_equal(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseBool) and isinstance(right, ParseBool):
        return ParseBinaryEqualBoolBool(left, right)
    elif isinstance(left, ParseInteger) and isinstance(right, ParseInteger):
        return ParseBinaryEqualIntegerInteger(left, right)
    else:
        return None
