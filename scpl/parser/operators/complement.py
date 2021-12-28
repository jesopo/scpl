from typing import Dict, Optional
from .common import ParseUnaryOperator
from ..operands import ParseAtom, ParseInteger, ParseRegex

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
    # don't double complement regexes.
    # a normal regex returns the substring that matched but a complemented
    # regex is zero-width because it's "does not match". if we shorten
    # comp(comp(regex)) to just a regex here, we preserve the substring stuff.
    elif isinstance(atom, ParseUnaryComplementRegex):
        return atom._atom
    elif isinstance(atom, ParseRegex):
        return ParseUnaryComplementRegex(atom)
    else:
        return None
