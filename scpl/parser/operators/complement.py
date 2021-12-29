from typing import Dict, Optional
from .common import ParseUnaryOperator
from ..operands import ParseAtom, ParseInteger, ParseRegex

class ParseUnaryComplementInteger(ParseUnaryOperator, ParseInteger):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Complement({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return ~self._atom.eval(vars)


def find_unary_complement(atom: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(atom, ParseInteger):
        return ParseUnaryComplementInteger(atom)
    else:
        return None
