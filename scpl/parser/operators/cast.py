from re import escape as re_escape
from typing import Dict
from .common import ParseUnaryOperator
from ..operands import ParseAtom, ParseFloat, ParseInteger, ParseRegex, ParseString

class ParseCastIntegerFloat(ParseUnaryOperator, ParseFloat):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastFloat({self._atom!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseFloat:
        return ParseFloat(self._atom.eval(variables).value)

class ParseCastStringRegex(ParseUnaryOperator, ParseRegex):
    def __init__(self, atom: ParseString):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastRegex({self._atom!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseRegex:
        pattern = re_escape(self._atom.eval(variables).value)
        return ParseRegex(None, pattern, set())
