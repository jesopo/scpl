from typing import Dict, Optional
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseFloat, ParseInteger
from .cast import ParseCastIntegerFloat

class ParseBinarySubtractIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Subtract({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(self._left.eval(vars).value - self._right.eval(vars).value)

class ParseBinarySubtractFloatFloat(ParseBinaryOperator, ParseFloat):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Subtract({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseFloat:
        return ParseFloat(self._left.eval(vars).value - self._right.eval(vars).value)
class ParseBinarySubtractFloatInteger(ParseBinarySubtractFloatFloat):
    def __init__(self, left: ParseFloat, right: ParseInteger):
        super().__init__(left, ParseCastIntegerFloat(right))
class ParseBinarySubtractIntegerFloat(ParseBinarySubtractFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseFloat):
        super().__init__(ParseCastIntegerFloat(left), right)

def find_binary_subtract(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger):
        if isinstance(right, ParseInteger):
            return ParseBinarySubtractIntegerInteger(left, right)
        elif isinstance(right, ParseFloat):
            return ParseBinarySubtractIntegerFloat(left, right)
        else:
            return None
    elif isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinarySubtractFloatFloat(left, right)
        elif isinstance(right, ParseInteger):
            return ParseBinarySubtractFloatInteger(left, right)
        else:
            return None
    else:
        return None
