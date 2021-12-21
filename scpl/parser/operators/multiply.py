from typing import Dict
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseFloat, ParseInteger
from .cast import ParseCastIntegerFloat

class ParseBinaryMultiplyFloatFloat(ParseBinaryOperator, ParseFloat):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Multiply({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseFloat:
        return ParseFloat(self._left.eval(vars).value * self._right.eval(vars).value)
class ParseBinaryMultiplyFloatInteger(ParseBinaryMultiplyFloatFloat):
    def __init__(self, left: ParseFloat, right: ParseInteger):
        super().__init__(left, ParseCastIntegerFloat(right))
class ParseBinaryMultiplyIntegerFloat(ParseBinaryMultiplyFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseFloat):
        super().__init__(ParseCastIntegerFloat(left), right)

class ParseBinaryMultiplyIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Multiply({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(self._left.eval(vars).value * self._right.eval(vars).value)

def find_binary_multiply(left: ParseAtom, right: ParseAtom):
    if isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryMultiplyFloatFloat(left, right)
        elif isinstance(right, ParseInteger):
            return ParseBinaryMultiplyFloatInteger(left, right)
        else:
            return None
    elif isinstance(left, ParseInteger):
        if isinstance(right, ParseInteger):
            return ParseBinaryMultiplyIntegerInteger(left, right)
        elif isinstance(right, ParseFloat):
            return ParseBinaryMultiplyIntegerFloat(left, right)
        else:
            return None
    else:
        return None
