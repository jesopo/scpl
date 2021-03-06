from typing import Dict, Optional
from .cast import ParseCastIntegerFloat
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseBool, ParseFloat, ParseInteger

class ParseBinaryGreaterIntegerInteger(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self):
        return f"Greater({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        return self._left.eval(vars) > self._right.eval(vars)

class ParseBinaryGreaterFloatFloat(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self):
        return f"Greater({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        return self._left.eval(vars) > self._right.eval(vars)
class ParseBinaryGreaterFloatInteger(ParseBinaryGreaterFloatFloat):
    def __init__(self, left: ParseFloat, right: ParseInteger):
        super().__init__(left, ParseCastIntegerFloat(right))
class ParseBinaryGreaterIntegerFloat(ParseBinaryGreaterFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseFloat):
        super().__init__(ParseCastIntegerFloat(left), right)

def find_binary_greater(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger):
        if isinstance(right, ParseInteger):
            return ParseBinaryGreaterIntegerInteger(left, right)
        elif isinstance(right, ParseFloat):
            return ParseBinaryGreaterIntegerFloat(left, right)
        else:
            return None
    elif isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryGreaterFloatFloat(left, right)
        elif isinstance(right, ParseInteger):
            return ParseBinaryGreaterFloatInteger(left, right)
        else:
            return None
    else:
        return None
