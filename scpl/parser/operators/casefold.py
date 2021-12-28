from typing import Dict, Optional
from .common import ParseUnaryOperator
from ..operands import ParseAtom, ParseString

class ParseUnaryCasefoldString(ParseUnaryOperator, ParseString):
    def __init__(self, atom: ParseString, table: Optional[Dict[str, str]]):
        super().__init__(atom)
        self._atom = atom
        self._table: Optional[Dict[int, int]] = None
        if table is not None:
            self._table = str.maketrans(table)
    def __repr__(self) -> str:
        return f"Casefold({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseString:
        atom = self._atom.eval(vars)
        if self._table is not None:
            out = atom.value.translate(self._table)
        else:
            out = atom.value.lower()
        return ParseString(None, out)
