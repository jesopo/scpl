from typing import Dict, Optional
from .common import ParseUnaryOperator
from ..operands import ParseAtom, ParseInteger, ParseRegex, ParseRegexset

class ParseUnaryComplementInteger(ParseUnaryOperator, ParseInteger):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Complement({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(~self._atom.eval(vars).value)

class ParseUnaryComplementRegex(ParseUnaryOperator, ParseRegex):
    def __init__(self, atom: ParseRegex):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"Complement({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseRegex:
        regex = self._atom.eval(vars)
        return ParseRegex(regex.delimiter, regex.pattern, regex.flags, not regex.expected)

def find_unary_complement(atom: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(atom, ParseInteger):
        return ParseUnaryComplementInteger(atom)
    elif isinstance(atom, ParseRegex):
        return ParseUnaryComplementRegex(atom)
    else:
        return None
