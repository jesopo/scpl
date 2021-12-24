from typing import Dict, Optional
from .common import ParseBinaryOperator
from ..operands import (ParseAtom, ParseBool, ParseCIDR, ParseCIDRv4, ParseCIDRv6,
    ParseIP, ParseIPv4, ParseIPv6, ParseString)

class ParseBinaryContainsStringString(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseString, right: ParseString):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Contains({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        return ParseBool(self._left.eval(vars).value in self._right.eval(vars).value)

class ParseBinaryContainsIPCIDR(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseIP, right: ParseCIDR):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Contains({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseBool:
        right = self._right.eval(vars)
        network = self._left.eval(vars).integer & right.mask
        return ParseBool(network == right.integer)

def find_binary_contains(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseString) and isinstance(right, ParseString):
        return ParseBinaryContainsStringString(left, right)
    elif isinstance(left, ParseIPv4) and isinstance(right, ParseCIDRv4):
        return ParseBinaryContainsIPCIDR(left, right)
    elif isinstance(left, ParseIPv6) and isinstance(right, ParseCIDRv6):
        return ParseBinaryContainsIPCIDR(left, right)
    else:
        return None
