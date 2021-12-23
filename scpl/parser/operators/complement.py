from typing import Dict, Optional
from .common import ParseUnaryOperator
from ..operands import ParseAtom, ParseInteger

class ParseUnaryComplementInteger(ParseUnaryOperator, ParseInteger):
    def __init__(self, atom: ParseInteger):
        self._atom = atom
    def __repr__(self) -> str:
        return f"Complement({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(~self._atom.eval(vars).value)

def find_unary_complement(atom: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(atom, ParseInteger):
        return ParseUnaryComplementInteger(atom)
    else:
        return None
