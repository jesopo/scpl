from typing import Dict, Optional
from .common import ParseUnaryOperator
from ..operands import ParseAtom, ParseFloat, ParseInteger

class ParseUnaryNegativeInteger(ParseUnaryOperator, ParseInteger):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Negative({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return -self._atom.eval(vars)

class ParseUnaryNegativeFloat(ParseUnaryOperator, ParseFloat):
    def __init__(self, atom: ParseFloat):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Negative({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> float:
        return -self._atom.eval(vars)

def find_unary_negative(atom: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(atom, ParseUnaryNegativeInteger):
        return atom._atom
    elif isinstance(atom, ParseUnaryNegativeFloat):
        return atom._atom
    elif isinstance(atom, ParseInteger):
        return ParseUnaryNegativeInteger(atom)
    elif isinstance(atom, ParseFloat):
        return ParseUnaryNegativeFloat(atom)
    else:
        return None
