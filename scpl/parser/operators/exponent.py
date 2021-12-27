from typing import Dict, Optional
from .cast import ParseCastIntegerFloat
from .common import ParseBinaryOperator
from .negative import ParseUnaryNegativeFloat, ParseUnaryNegativeInteger
from ..operands import ParseAtom, ParseInteger, ParseFloat

class ParseBinaryExponentIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Exponent({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(self._left.eval(vars).value ** self._right.eval(vars).value)

class ParseBinaryExponentFloatFloat(ParseBinaryOperator, ParseFloat):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Exponent({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseFloat:
        return ParseFloat(self._left.eval(vars).value ** self._right.eval(vars).value)
class ParseBinaryExponentFloatInteger(ParseBinaryExponentFloatFloat):
    def __init__(self, left: ParseFloat, right: ParseInteger):
        super().__init__(left, ParseCastIntegerFloat(right))
class ParseBinaryExponentIntegerFloat(ParseBinaryExponentFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseFloat):
        super().__init__(ParseCastIntegerFloat(left), right)
# Exponent(Integer, Negative(Integer)) produces a float
class ParseBinaryExponentIntegerNegative(ParseBinaryExponentFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseUnaryNegativeInteger):
        super().__init__(ParseCastIntegerFloat(left), ParseCastIntegerFloat(right))

def find_binary_exponent(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger):
        if isinstance(right, ParseUnaryNegativeInteger):
            return ParseBinaryExponentIntegerNegative(left, right)
        elif isinstance(right, ParseInteger):
            return ParseBinaryExponentIntegerInteger(left, right)
        elif isinstance(right, ParseFloat):
            return ParseBinaryExponentIntegerFloat(left, right)
        else:
            return None
    elif isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryExponentFloatFloat(left, right)
        elif isinstance(right, ParseInteger):
            return ParseBinaryExponentFloatInteger(left, right)
        else:
            return None
    else:
        return None
