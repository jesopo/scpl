from typing import Dict, Optional
from .cast import ParseCastIntegerFloat
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseInteger, ParseFloat

class ParseBinaryModuloIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Modulo({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return self._left.eval(vars) % self._right.eval(vars)

class ParseBinaryModuloFloatFloat(ParseBinaryOperator, ParseFloat):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Modulo({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> float:
        return self._left.eval(vars) % self._right.eval(vars)
class ParseBinaryModuloFloatInteger(ParseBinaryModuloFloatFloat):
    def __init__(self, left: ParseFloat, right: ParseInteger):
        super().__init__(left, ParseCastIntegerFloat(right))
class ParseBinaryModuloIntegerFloat(ParseBinaryModuloFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseFloat):
        super().__init__(ParseCastIntegerFloat(left), right)

def find_binary_modulo(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger):
        if isinstance(right, ParseInteger):
            return ParseBinaryModuloIntegerInteger(left, right)
        elif isinstance(right, ParseFloat):
            return ParseBinaryModuloIntegerFloat(left, right)
        else:
            return None
    elif isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryModuloFloatFloat(left, right)
        elif isinstance(right, ParseInteger):
            return ParseBinaryModuloFloatInteger(left, right)
        else:
            return None
    else:
        return None
