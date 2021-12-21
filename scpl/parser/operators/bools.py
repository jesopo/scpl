from typing import Dict, Optional, Tuple
from .common import ParseBinaryOperator
from .cast import find_cast_bool
from ..operands import ParseAtom, ParseBool

class ParseBinaryAnd(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseBool, right: ParseBool):
        self._left = left
        self._right = right
    def __repr__(self):
        return f"And({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(self._left.eval(vars).value and self._right.eval(vars).value)

class ParseBinaryOr(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseBool, right: ParseBool):
        self._left = left
        self._right = right
    def __repr__(self):
        return f"Or({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(self._left.eval(vars).value or self._right.eval(vars).value)

def _double_cast(
        aleft: ParseAtom, aright: ParseAtom
        ) -> Optional[Tuple[ParseBool, ParseBool]]:

    if ((left := find_cast_bool(aleft)) is not None
            and (right := find_cast_bool(aright)) is not None):
        return (left, right)
    else:
        return None

def find_binary_and(left: ParseAtom, right: ParseAtom) -> Optional[ParseBool]:
    if (dcast := _double_cast(left, right)) is not None:
        return ParseBinaryAnd(*dcast)
    else:
        return None

def find_binary_or(left: ParseAtom, right: ParseAtom) -> Optional[ParseBool]:
    if (dcast := _double_cast(left, right)) is not None:
        return ParseBinaryOr(*dcast)
    else:
        return None
