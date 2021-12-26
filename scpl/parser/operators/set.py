from typing import cast, Dict, Optional, Sequence, Set
from .cast import find_cast_hash, ParseCastHash
from ..operands import (ParseAtom, ParseFloat, ParseInteger, ParseIPv4, ParseIPv6,
    ParseString)

class ParseSet(ParseAtom):
    def __init__(self, atoms: Sequence[ParseCastHash]):
        self._atoms = atoms
    def __repr__(self) -> str:
        return f"Set({', '.join(repr(a.atom) for a in self._atoms)})"
    def eval(self, vars: Dict[str, ParseAtom]) -> Set[int]:
        return set(a.eval(vars).value for a in self._atoms)

def _all_isinstance(atoms: Sequence[ParseAtom], atype: type) -> bool:
    for atom in atoms:
        if not isinstance(atom, atype):
            return False
    return True

def find_set(atoms: Sequence[ParseAtom]) -> Optional[ParseAtom]:
    if len(atoms) == 0:
        return ParseSet([])
    elif (_all_isinstance(atoms, ParseInteger)
            or _all_isinstance(atoms, ParseFloat)
            or _all_isinstance(atoms, ParseString)
            or _all_isinstance(atoms, ParseIPv4)
            or _all_isinstance(atoms, ParseIPv6)):

        if all(casts := [find_cast_hash(a) for a in atoms]):
            return ParseSet(cast(Sequence[ParseCastHash], casts))
        else:
            return None
    else:
        return None
