from typing import Dict
from .common import ParseBinaryOperator
from ..operands import (ParseAtom, ParseCIDRv4, ParseCIDRv6, ParseIPv4,
    ParseIPv6, ParseFloat, ParseInteger)
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

class ParseBinaryDivideIPv4Integer(ParseBinaryOperator, ParseCIDRv4):
    def __init__(self, left: ParseIPv4, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Divide({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseCIDRv4:
        return ParseCIDRv4(self._left.eval(vars).integer, self._right.eval(vars).value)
class ParseBinaryDivideIPv6Integer(ParseBinaryOperator, ParseCIDRv6):
    def __init__(self, left: ParseIPv6, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Divide({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseCIDRv6:
        return ParseCIDRv6(self._left.eval(vars).integer, self._right.eval(vars).value)

def find_binary_divide(left: ParseAtom, right: ParseAtom):
    if isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryDivideFloatFloat(left, right)
        else:
            return None
    elif isinstance(left, ParseInteger):
        if isinstance(right, ParseInteger):
            return ParseBinaryDivideIntegerInteger(left, right)
        else:
            return None
    elif isinstance(left, ParseIPv4):
        if isinstance(right, ParseInteger):
            return ParseBinaryDivideIPv4Integer(left, right)
        else:
            return None
    elif isinstance(left, ParseIPv6):
        if isinstance(right, ParseInteger):
            return ParseBinaryDivideIPv6Integer(left, right)
        else:
            return None
    else:
        return None
