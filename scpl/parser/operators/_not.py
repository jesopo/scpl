from ..operands import *

class ParseUnaryNotString(ParseBool):
    def __init__(self, atom: ParseString):
        self._atom = atom
    def __repr__(self) -> str:
        return f"Not({self._atom!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        return ParseBool(not bool(self._atom.value))

class ParseUnaryNotInteger(ParseBool):
    def __init__(self, atom: ParseInteger):
        self._atom = atom
    def __repr__(self) -> str:
        return f"Not({self._atom!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        return ParseBool(not bool(self._atom.value))

class ParseUnaryNotFloat(ParseBool):
    def __init__(self, atom: ParseFloat):
        self._atom = atom
    def __repr__(self) -> str:
        return f"Not({self._atom!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        return ParseBool(not bool(self._atom.value))

def find_unary_not(atom: ParseAtom):
    if isinstance(atom, ParseString):
        return ParseUnaryNotString(atom)
    elif isinstance(atom, ParseInteger):
        return ParseUnaryNotInteger(atom)
    elif isinstance(atom, ParseFloat):
        return ParseUnaryNotFloat(atom)
    else:
        return None
