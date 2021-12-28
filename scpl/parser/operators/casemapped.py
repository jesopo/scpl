from typing import Dict, Optional
from .common import ParseUnaryOperator
from ..operands import ParseAtom, ParseString, ParseRegex
from ... import regex

class ParseUnaryCasemappedString(ParseUnaryOperator, ParseString):
    def __init__(self, atom: ParseString, table: Dict[str, str]):
        self._atom = atom
        self.table = str.maketrans(table)
    def __repr__(self) -> str:
        return f"Casemapped({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseString:
        return self._atom

class ParseUnaryCasemappedRegex(ParseUnaryOperator, ParseRegex):
    def __init__(self, atom: ParseRegex, table: Dict[int, str]):
        self._atom = atom
        self.table = str.maketrans(table)
    def __repr__(self) -> str:
        return f"Casemapped({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseRegex:
        atom = self._atom.eval(vars)
        if "i" in atom.flags:
            tokens = regex.translator.translate(
                regex.lexer.tokenise(atom.pattern),
                self.table
            )
            folded = "".join(t.text for t in tokens)
            flags = atom.flags - set("i")
            return ParseRegex(atom.delimiter, folded, flags, atom.expected)
        else:
            return atom
