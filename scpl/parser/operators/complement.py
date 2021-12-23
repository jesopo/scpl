from typing import Dict, Optional
from .common import ParseUnaryOperator
from ..operands import ParseAtom, ParseInteger, ParseRegex, ParseRegexset

class ParseUnaryComplementInteger(ParseUnaryOperator, ParseInteger):
    def __init__(self, atom: ParseInteger):
        self._atom = atom
    def __repr__(self) -> str:
        return f"Complement({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(~self._atom.eval(vars).value)

class ParseUnaryComplementRegex(ParseUnaryOperator, ParseRegexset):
    def __init__(self, atom: ParseRegex):
        self._atom = atom
    def __repr__(self) -> str:
        return f"Complement({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseRegexset:
        return ParseRegexset({(True, self._atom.eval(vars))})

def find_unary_complement(atom: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(atom, ParseInteger):
        return ParseUnaryComplementInteger(atom)
    elif isinstance(atom, ParseRegex):
        return ParseUnaryComplementRegex(atom)
    else:
        return None
