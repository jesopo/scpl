from ..operands import *

class ParseBinaryDivideFloatFloat(ParseFloat):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Divide({self._left!r}, {self._right!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        return ParseFloat(self._left.value / self._right.value)
class ParseBinaryDivideIntegerInteger(ParseBinaryDivideFloatFloat):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(ParseFloat(float(left.value)), ParseFloat(float(right.value)))

class ParseBinaryDivideIPv4Integer(ParseCIDRv4):
    def __init__(self, left: ParseIPv4, right: ParseInteger):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Divide({self._left!r}, {self._right!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        return ParseCIDRv4(self._left.integer, self._right.value)
class ParseBinaryDivideIPv6Integer(ParseCIDRv6):
    def __init__(self, left: ParseIPv6, right: ParseInteger):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Divide({self._left!r}, {self._right!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        return ParseCIDRv6(self._left.integer, self._right.value)

def find_binary_divide(left: ParseAtom, right: ParseAtom):
    if isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryDivideFloatFloat(left, right)
        else:
            return None
    elif isinstance(left, ParseInteger):
        if isinstance(right, ParseInteger):
            return ParseBinaryDivideIntegerInteger(left, right)
        else:
            return None
    elif isinstance(left, ParseIPv4):
        if isinstance(right, ParseInteger):
            return ParseBinaryDivideIPv4Integer(left, right)
        else:
            return None
    elif isinstance(left, ParseIPv6):
        if isinstance(right, ParseInteger):
            return ParseBinaryDivideIPv6Integer(left, right)
        else:
            return None
    else:
        return None
