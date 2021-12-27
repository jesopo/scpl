from typing import cast, Dict, Optional, Sequence, Set
from .cast import (ParseCastHash, ParseCastHashFloat, ParseCastHashInteger,
    ParseCastHashIPv4, ParseCastHashIPv6, ParseCastHashString)
from ..common import ParserErrorWithIndex
from ..operands import (ParseAtom, ParseFloat, ParseInteger, ParseIPv4, ParseIPv6,
    ParseString)

class ParseSet(ParseAtom):
    def __init__(self, atoms: Sequence[ParseCastHash]):
        self._atoms = atoms
        self._precompile: Set[int] = set()
    def __repr__(self) -> str:
        return f"Set({', '.join(repr(a.atom) for a in self._atoms)})"
    def eval(self, vars: Dict[str, ParseAtom]) -> Set[int]:
        nonconst = set(a.eval(vars).value for a in self._atoms)
        return self._precompile | nonconst

class ParseSetInteger(ParseSet):
    def __init__(self, atoms: Sequence[ParseInteger]):
        super().__init__([ParseCastHashInteger(a) for a in atoms])
class ParseSetFloat(ParseSet):
    def __init__(self, atoms: Sequence[ParseFloat]):
        super().__init__([ParseCastHashFloat(a) for a in atoms])
class ParseSetString(ParseSet):
    def __init__(self, atoms: Sequence[ParseString]):
        super().__init__([ParseCastHashString(a) for a in atoms])
class ParseSetIPv4(ParseSet):
    def __init__(self, atoms: Sequence[ParseIPv4]):
        super().__init__([ParseCastHashIPv4(a) for a in atoms])
class ParseSetIPv6(ParseSet):
    def __init__(self, atoms: Sequence[ParseIPv6]):
        super().__init__([ParseCastHashIPv6(a) for a in atoms])

def _all_isinstance(atoms: Sequence[ParseAtom], atype: type) -> bool:
    for i, atom in enumerate(atoms):
        if not isinstance(atom, atype):
            if i > 0:
                raise ParserErrorWithIndex(
                    i, f"{type(atom).__name__} in {atype.__name__} set"
                )
            else:
                return False
    return True

def find_set(atoms: Sequence[ParseAtom]) -> Optional[ParseAtom]:
    if len(atoms) == 0:
        return ParseSet([])
    elif _all_isinstance(atoms, ParseInteger):
        return ParseSetInteger(cast(Sequence[ParseInteger], atoms))
    elif _all_isinstance(atoms, ParseFloat):
        return ParseSetFloat(cast(Sequence[ParseFloat], atoms))
    elif _all_isinstance(atoms, ParseString):
        return ParseSetString(cast(Sequence[ParseString], atoms))
    elif _all_isinstance(atoms, ParseIPv4):
        return ParseSetIPv4(cast(Sequence[ParseIPv4], atoms))
    elif _all_isinstance(atoms, ParseIPv6):
        return ParseSetIPv6(cast(Sequence[ParseIPv6], atoms))
    else:
        return None
