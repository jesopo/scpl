from typing import Dict
from .common import ParseUnaryOperator
from ..operands import ParseAtom, ParseFloat, ParseInteger

class ParseUnaryPositiveInteger(ParseUnaryOperator, ParseInteger):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Positive({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return +self._atom.eval(vars)

class ParseUnaryPositiveFloat(ParseUnaryOperator, ParseFloat):
    def __init__(self, atom: ParseFloat):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Positive({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> float:
        return +self._atom.eval(vars)

def find_unary_positive(atom: ParseAtom):
    if isinstance(atom, ParseInteger):
        return ParseUnaryPositiveInteger(atom)
    elif isinstance(atom, ParseFloat):
        return ParseUnaryPositiveFloat(atom)
    else:
        return None
