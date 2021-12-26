from typing import cast, Dict, Optional, Sequence, Set
from ..operands import (ParseAtom, ParseFloat, ParseInteger, ParseIPv4, ParseIPv6,
    ParseString)

class ParseSet(ParseAtom):
    def __init__(self, atoms: Sequence[ParseAtom]):
        self._base_atoms = atoms
    def __repr__(self) -> str:
        return f"Set({', '.join(repr(a) for a in self._base_atoms)})"

class ParseSetInteger(ParseSet):
    def __init__(self, atoms: Sequence[ParseInteger]):
        super().__init__(atoms)
        self._atoms = atoms
    def eval(self, vars: Dict[str, ParseAtom]) -> Set[ParseInteger]:
        return set(atom.eval(vars) for atom in self._atoms)

class ParseSetFloat(ParseSet):
    def __init__(self, atoms: Sequence[ParseFloat]):
        super().__init__(atoms)
        self._atoms = atoms
    def eval(self, vars: Dict[str, ParseAtom]) -> Set[ParseFloat]:
        return set(atom.eval(vars) for atom in self._atoms)

class ParseSetString(ParseSet):
    def __init__(self, atoms: Sequence[ParseString]):
        super().__init__(atoms)
        self._atoms = atoms
    def eval(self, vars: Dict[str, ParseAtom]) -> Set[ParseString]:
        return set(atom.eval(vars) for atom in self._atoms)

class ParseSetIPv4(ParseSet):
    def __init__(self, atoms: Sequence[ParseIPv4]):
        super().__init__(atoms)
        self._atoms = atoms
    def eval(self, vars: Dict[str, ParseAtom]) -> Set[ParseIPv4]:
        return set(atom.eval(vars) for atom in self._atoms)
class ParseSetIPv6(ParseSet):
    def __init__(self, atoms: Sequence[ParseIPv6]):
        super().__init__(atoms)
        self._atoms = atoms
    def eval(self, vars: Dict[str, ParseAtom]) -> Set[ParseIPv6]:
        return set(atom.eval(vars) for atom in self._atoms)

def _all_isinstance(atoms: Sequence[ParseAtom], atype: type) -> bool:
    for atom in atoms:
        if not isinstance(atom, atype):
            return False
    return True

def find_set(atoms: Sequence[ParseAtom]) -> Optional[ParseAtom]:
    if _all_isinstance(atoms, ParseInteger):
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
