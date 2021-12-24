from typing import Dict, Optional
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseBool, ParseInteger, ParseString

class ParseBinaryEqualBoolBool(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseBool, right: ParseBool):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Equal({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(self._left.eval(vars).value == self._right.eval(vars).value)

class ParseBinaryEqualIntegerInteger(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Equal({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(self._left.eval(vars).value == self._right.eval(vars).value)

class ParseBinaryEqualStringString(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseString, right: ParseString):
        super().__init__(left, right)
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
    elif isinstance(left, ParseString) and isinstance(right, ParseString):
        return ParseBinaryEqualStringString(left, right)
    else:
        return None
