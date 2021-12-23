from typing import Dict
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseFloat, ParseInteger
from .cast import ParseCastIntegerFloat

class ParseBinaryDivideFloatFloat(ParseBinaryOperator, ParseFloat):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Divide({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseFloat:
        return ParseFloat(self._left.eval(vars).value / self._right.eval(vars).value)

class ParseBinaryDivideIntegerInteger(ParseBinaryDivideFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(ParseCastIntegerFloat(left), ParseCastIntegerFloat(right))
class ParseBinaryDivideIntegerFloat(ParseBinaryDivideFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseFloat):
        super().__init__(ParseCastIntegerFloat(left), right)
class ParseBinaryDivideFloatInteger(ParseBinaryDivideFloatFloat):
    def __init__(self, left: ParseFloat, right: ParseInteger):
        super().__init__(left, ParseCastIntegerFloat(right))

def find_binary_divide(left: ParseAtom, right: ParseAtom):
    if isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryDivideFloatFloat(left, right)
        elif isinstance(right, ParseInteger):
            return ParseBinaryDivideFloatInteger(left, right)
        else:
            return None
    elif isinstance(left, ParseInteger):
        if isinstance(right, ParseInteger):
            return ParseBinaryDivideIntegerInteger(left, right)
        elif isinstance(right, ParseFloat):
            return ParseBinaryDivideIntegerFloat(left, right)
        else:
            return None
    else:
        return None
