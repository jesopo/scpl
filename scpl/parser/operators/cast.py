from re import escape as re_escape
from typing import Dict, Optional
from .common import ParseUnaryOperator
from ..operands import (ParseAtom, ParseBool, ParseFloat, ParseInteger, ParseRegex,
    ParseString)

class ParseCastIntegerFloat(ParseUnaryOperator, ParseFloat):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastFloat({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseFloat:
        return ParseFloat(self._atom.eval(vars).value)

class ParseCastStringRegex(ParseUnaryOperator, ParseRegex):
    def __init__(self, atom: ParseString):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastRegex({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseRegex:
        pattern = re_escape(self._atom.eval(vars).value)
        return ParseRegex(None, pattern, set(), True)

class ParseCastStringBool(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseString):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastBool({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(len(self._atom.eval(vars).value) > 0)
class ParseCastRegexBool(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseRegex):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastBool({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(len(self._atom.eval(vars).pattern) > 0)
class ParseCastIntegerBool(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastBool({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(not self._atom.eval(vars).value == 0)
class ParseCastFloatBool(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseFloat):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastBool({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(not self._atom.eval(vars).value == 0.0)

class ParseCastHash(ParseUnaryOperator):
    def __init__(self, atom: ParseAtom):
        self._base_atom = atom
    def __repr__(self) -> str:
        return f"CastHash({self._base_atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        raise NotImplementedError()
class ParseCastHashInteger(ParseCastHash, ParseInteger):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(hash(self._atom.eval(vars)))
class ParseCastHashString(ParseCastHash, ParseInteger):
    def __init__(self, atom: ParseString):
        super().__init__(atom)
        self._atom = atom
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(hash(self._atom.eval(vars)))
class ParseCastHashRegex(ParseCastHash, ParseInteger):
    def __init__(self, atom: ParseRegex):
        super().__init__(atom)
        self._atom = atom
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(hash(self._atom.eval(vars)))

def find_cast_bool(atom: ParseAtom) -> Optional[ParseBool]:
    if isinstance(atom, ParseBool):
        return atom
    elif isinstance(atom, ParseString):
        return ParseCastStringBool(atom)
    elif isinstance(atom, ParseRegex):
        return ParseCastRegexBool(atom)
    elif isinstance(atom, ParseInteger):
        return ParseCastIntegerBool(atom)
    elif isinstance(atom, ParseFloat):
        return ParseCastFloatBool(atom)
    else:
        return None

def find_cast_hash(atom: ParseAtom) -> Optional[ParseCastHash]:
    if isinstance(atom, ParseInteger):
        return ParseCastHashInteger(atom)
    elif isinstance(atom, ParseString):
        return ParseCastHashString(atom)
    elif isinstance(atom, ParseRegex):
        return ParseCastHashRegex(atom)
    else:
        return None
