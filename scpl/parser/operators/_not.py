from .common import ParseUnaryOperator
from ..operands import *

class ParseUnaryNotString(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseString):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Not({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(not bool(self._atom.eval(vars).value))

class ParseUnaryNotInteger(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Not({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(not bool(self._atom.eval(vars).value))

class ParseUnaryNotFloat(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseFloat):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Not({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(not bool(self._atom.eval(vars).value))

def find_unary_not(atom: ParseAtom):
    if isinstance(atom, ParseString):
        return ParseUnaryNotString(atom)
    elif isinstance(atom, ParseInteger):
        return ParseUnaryNotInteger(atom)
    elif isinstance(atom, ParseFloat):
        return ParseUnaryNotFloat(atom)
    else:
        return None
