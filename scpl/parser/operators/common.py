from ..operands import ParseAtom

class ParseBinaryOperator(ParseAtom):
    def __init__(self, left: ParseAtom, right: ParseAtom):
        self._base_left = left
        self._base_right = right

    def is_constant(self) -> bool:
        return self._base_left.is_constant() and self._base_right.is_constant()

class ParseUnaryOperator(ParseAtom):
    def __init__(self, atom: ParseAtom):
        self._base_atom = atom

    def is_constant(self) -> bool:
        return self._base_atom.is_constant()

