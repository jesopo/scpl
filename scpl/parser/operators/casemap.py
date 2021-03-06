import re
from typing import Dict, Pattern
from ..operands import ParseAtom, ParseRegex
from ... import regex

class ParseCasemappedRegex(ParseRegex):
    def __init__(self, atom: ParseRegex, casemap: Dict[int, str]):
        self._atom = atom
        self._casemap = casemap
    def __repr__(self) -> str:
        return f"Casemapped({self._atom!r}, {self._casemap!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> Pattern:
        compiled = self._atom.eval(vars)
        if compiled.flags & re.I:
            # because this is about case insensitivity, the replacement for `k` should
            # include `k` - i.e. a casemap of a:A should translate `a` in to `aA`
            casemap = {k: f"{chr(k)}{v}" for k, v in self._casemap.items()}
            tokens = regex.translator.translate(
                regex.lexer.tokenise(compiled.pattern),
                self._casemap
            )
            newregex = "".join(t.text for t in tokens)
            return re.compile(newregex, compiled.flags & ~re.I)
        else:
            return compiled
