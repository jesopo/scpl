from typing import Dict
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseBool, ParseRegex, ParseRegexset, ParseString

class ParseBinaryMatchStringRegex(ParseBinaryOperator, ParseString):
    def __init__(self, left: ParseString, right: ParseRegex):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Match({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseString:
        reference = self._left.eval(vars).value
        match = self._right.eval(vars).compiled.search(reference)
        if match is not None:
            return ParseString(None, match.group(0))
        else:
            return ParseString(None, "")

class ParseBinaryMatchStringRegexset(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseString, right: ParseRegexset):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Match({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        reference = self._left.eval(vars).value
        regexes = self._right.eval(vars).regexes
        for invert, regex in regexes:
            match = bool(regex.compiled.search(reference))
            if match == invert:
                return ParseBool(False)
        return ParseBool(True)

def find_binary_match(left: ParseAtom, right: ParseAtom):
    if isinstance(left, ParseString):
        if isinstance(right, ParseRegex):
            return ParseBinaryMatchStringRegex(left, right)
        elif isinstance(right, ParseRegexset):
            return ParseBinaryMatchStringRegexset(left, right)
        else:
            return None
    else:
        return None
