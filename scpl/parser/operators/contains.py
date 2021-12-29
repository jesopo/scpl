from typing import Dict, Optional
from .common import ParseBinaryOperator
from ..operands import (ParseAtom, ParseBool, ParseCIDR, ParseCIDRv4, ParseCIDRv6,
    ParseFloat, ParseInteger, ParseIP, ParseIPv4, ParseIPv6, ParseString)
from .set import (ParseSet, ParseSetInteger, ParseSetIPv4, ParseSetIPv6, ParseSetFloat,
    ParseSetString)
from .cast import (ParseCastHash, ParseCastHashFloat, ParseCastHashInteger,
    ParseCastHashIPv4, ParseCastHashIPv6, ParseCastHashString)

class ParseBinaryContainsStringString(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseString, right: ParseString):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Contains({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        return self._left.eval(vars) in self._right.eval(vars)

class ParseBinaryContainsIPCIDR(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseIP, right: ParseCIDR):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Contains({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        right = self._right.eval(vars)
        network = self._left.eval(vars).integer & right.mask
        return network == right.integer

class ParseBinaryContainsHashSet(ParseBinaryOperator, ParseBool):
    def __init__(self, left: ParseCastHash, right: ParseSet):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Contains({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        right = self._right.eval(vars)
        return self._left.eval(vars) in right

class ParseBinaryContainsIntegerSet(ParseBinaryContainsHashSet):
    def __init__(self, left: ParseInteger, right: ParseSetInteger):
        super().__init__(ParseCastHashInteger(left), right)
class ParseBinaryContainsFloatSet(ParseBinaryContainsHashSet):
    def __init__(self, left: ParseFloat, right: ParseSetFloat):
        super().__init__(ParseCastHashFloat(left), right)
class ParseBinaryContainsStringSet(ParseBinaryContainsHashSet):
    def __init__(self, left: ParseString, right: ParseSetString):
        super().__init__(ParseCastHashString(left), right)
class ParseBinaryContainsIPv4Set(ParseBinaryContainsHashSet):
    def __init__(self, left: ParseIPv4, right: ParseSetIPv4):
        super().__init__(ParseCastHashIPv4(left), right)
class ParseBinaryContainsIPv6Set(ParseBinaryContainsHashSet):
    def __init__(self, left: ParseIPv6, right: ParseSetIPv6):
        super().__init__(ParseCastHashIPv6(left), right)

def find_binary_contains(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    # check `right` first because if it is a set then we don't care what `left` is
    if isinstance(left, ParseInteger) and isinstance(right, ParseSetInteger):
        return ParseBinaryContainsIntegerSet(left, right)
    elif isinstance(left, ParseFloat) and isinstance(right, ParseSetFloat):
        return ParseBinaryContainsFloatSet(left, right)
    elif isinstance(left, ParseString) and isinstance(right, ParseSetString):
        return ParseBinaryContainsStringSet(left, right)
    elif isinstance(left, ParseIPv4) and isinstance(right, ParseSetIPv4):
        return ParseBinaryContainsIPv4Set(left, right)
    elif isinstance(left, ParseIPv6) and isinstance(right, ParseSetIPv6):
        return ParseBinaryContainsIPv6Set(left, right)
    elif isinstance(left, ParseString) and isinstance(right, ParseString):
        return ParseBinaryContainsStringString(left, right)
    elif isinstance(left, ParseIPv4) and isinstance(right, ParseCIDRv4):
        return ParseBinaryContainsIPCIDR(left, right)
    elif isinstance(left, ParseIPv6) and isinstance(right, ParseCIDRv6):
        return ParseBinaryContainsIPCIDR(left, right)
    else:
        return None
