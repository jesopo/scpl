from .common import ParseUnaryOperator
from ..operands import *

class ParseUnaryNegativeInteger(ParseUnaryOperator, ParseInteger):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Negative({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(-self._atom.eval(vars).value)

class ParseUnaryNegativeFloat(ParseUnaryOperator, ParseFloat):
    def __init__(self, atom: ParseFloat):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Negative({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseFloat:
        return ParseFloat(-self._atom.eval(vars).value)

def find_unary_negative(atom: ParseAtom):
    if isinstance(atom, ParseInteger):
        return ParseUnaryNegativeInteger(atom)
    elif isinstance(atom, ParseFloat):
        return ParseUnaryNegativeFloat(atom)
    else:
        return None