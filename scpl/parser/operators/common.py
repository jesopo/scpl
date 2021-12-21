from typing import Dict
from ..operands import ParseAtom

class ParseOperator(ParseAtom):
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseAtom:
        raise NotImplementedError()

class ParseBinaryOperator(ParseOperator):
    def __init__(self, left: ParseAtom, right: ParseAtom):
        self._base_left = left
        self._base_right = right

    def is_constant(self) -> bool:
        return self._base_left.is_constant() and self._base_right.is_constant()

class ParseUnaryOperator(ParseOperator):
    def __init__(self, atom: ParseAtom):
        self._base_atom = atom

    def is_constant(self) -> bool:
        return self._base_atom.is_constant()

