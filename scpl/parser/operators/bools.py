from typing import Dict, Optional, Tuple
from .common import ParseBinaryOperator, ParseUnaryOperator
from .cast import find_cast_bool
from ..operands import ParseAtom, ParseBool

class ParseBinaryBoth(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseBool, right: ParseBool):
        self._left = left
        self._right = right
    def __repr__(self):
        return f"Both({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(self._left.eval(vars).value and self._right.eval(vars).value)

class ParseBinaryEither(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseBool, right: ParseBool):
        self._left = left
        self._right = right
    def __repr__(self):
        return f"Either({self._left!r}, {self._right!r})"
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
def _cast(aatom: ParseAtom) -> Optional[ParseBool]:
    if (atom := find_cast_bool(aatom)) is not None:
        return atom
    else:
        return None

def find_binary_both(left: ParseAtom, right: ParseAtom) -> Optional[ParseBool]:
    if (dcast := _double_cast(left, right)) is not None:
        return ParseBinaryBoth(*dcast)
    else:
        return None

def find_binary_either(left: ParseAtom, right: ParseAtom) -> Optional[ParseBool]:
    if (dcast := _double_cast(left, right)) is not None:
        return ParseBinaryEither(*dcast)
    else:
        return None

class ParseUnaryNot(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseBool):
        self._atom = atom
    def __repr__(self) -> str:
        return f"Not({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(not self._atom.eval(vars).value)

def find_unary_not(atom: ParseAtom) -> Optional[ParseBool]:
    if (cast := _cast(atom)) is not None:
        return ParseUnaryNot(cast)
    else:
        return None
