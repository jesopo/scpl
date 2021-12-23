from typing import Dict, Optional
from .cast import ParseCastIntegerFloat
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseBool, ParseFloat, ParseInteger

class ParseBinaryLesserIntegerInteger(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        self._left = left
        self._right = right
    def __repr__(self):
        return f"Lesser({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(self._left.eval(vars).value < self._right.eval(vars).value)

class ParseBinaryLesserFloatFloat(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        self._left = left
        self._right = right
    def __repr__(self):
        return f"Lesser({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(self._left.eval(vars).value < self._right.eval(vars).value)
class ParseBinaryLesserFloatInteger(ParseBinaryLesserFloatFloat):
    def __init__(self, left: ParseFloat, right: ParseInteger):
        super().__init__(left, ParseCastIntegerFloat(right))
class ParseBinaryLesserIntegerFloat(ParseBinaryLesserFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseFloat):
        super().__init__(ParseCastIntegerFloat(left), right)

def find_binary_lesser(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger):
        if isinstance(right, ParseInteger):
            return ParseBinaryLesserIntegerInteger(left, right)
        elif isinstance(right, ParseFloat):
            return ParseBinaryLesserIntegerFloat(left, right)
        else:
            return None
    elif isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryLesserFloatFloat(left, right)
        elif isinstance(right, ParseInteger):
            return ParseBinaryLesserFloatInteger(left, right)
        else:
            return None
    else:
        return None
