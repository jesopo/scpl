from re import compile as re_compile, escape as re_escape
from typing import Dict, Optional, Pattern
from .common import ParseUnaryOperator
from ..operands import (ParseAtom, ParseBool, ParseFloat, ParseInteger, ParseIPv4,
    ParseIPv6, ParseRegex, ParseString)

class ParseCastIntegerFloat(ParseUnaryOperator, ParseFloat):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastFloat({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> float:
        return float(self._atom.eval(vars))

class ParseCastStringRegex(ParseUnaryOperator, ParseRegex):
    def __init__(self, atom: ParseString):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastRegex({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> Pattern:
        return re_compile(re_escape(self._atom.eval(vars)))

class ParseCastStringBool(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseString):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastBool({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        return len(self._atom.eval(vars)) > 0
class ParseCastRegexBool(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseRegex):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastBool({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        return len(self._atom.eval(vars).pattern) > 0
class ParseCastIntegerBool(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastBool({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        return not (self._atom.eval(vars) == 0)
class ParseCastFloatBool(ParseUnaryOperator, ParseBool):
    def __init__(self, atom: ParseFloat):
        super().__init__(atom)
        self._atom = atom
    def __repr__(self) -> str:
        return f"CastBool({self._atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        return not (self._atom.eval(vars) == 0.0)

class ParseCastHash(ParseUnaryOperator):
    def __init__(self, atom: ParseAtom):
        self.atom = atom
    def __repr__(self) -> str:
        return f"CastHash({self.atom!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        raise NotImplementedError()
class ParseCastHashInteger(ParseCastHash, ParseInteger):
    def __init__(self, atom: ParseInteger):
        super().__init__(atom)
        self._atom = atom
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return hash(self._atom.eval(vars))
class ParseCastHashFloat(ParseCastHash, ParseInteger):
    def __init__(self, atom: ParseFloat):
        super().__init__(atom)
        self._atom = atom
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return hash(self._atom.eval(vars))
class ParseCastHashString(ParseCastHash, ParseInteger):
    def __init__(self, atom: ParseString):
        super().__init__(atom)
        self._atom = atom
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return hash(self._atom.eval(vars))
class ParseCastHashRegex(ParseCastHash, ParseInteger):
    def __init__(self, atom: ParseRegex):
        super().__init__(atom)
        self._atom = atom
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return hash(self._atom.eval(vars))
class ParseCastHashIPv4(ParseCastHash, ParseInteger):
    def __init__(self, atom: ParseIPv4):
        super().__init__(atom)
        self._atom = atom
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return hash(self._atom.eval(vars))
class ParseCastHashIPv6(ParseCastHash, ParseInteger):
    def __init__(self, atom: ParseIPv6):
        super().__init__(atom)
        self._atom = atom
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return hash(self._atom.eval(vars))

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
