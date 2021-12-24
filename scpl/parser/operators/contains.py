from typing import Dict, Optional
from .common import ParseBinaryOperator
from ..operands import (ParseAtom, ParseBool, ParseCIDR, ParseCIDRv4, ParseCIDRv6,
    ParseIP, ParseIPv4, ParseIPv6)

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
    if isinstance(left, ParseIPv4):
        if isinstance(right, ParseCIDRv4):
            return ParseBinaryContainsIPCIDR(left, right)
        else:
            return None
    if isinstance(left, ParseIPv6):
        if isinstance(right, ParseCIDRv6):
            return ParseBinaryContainsIPCIDR(left, right)
        else:
            return None
    else:
        return None
