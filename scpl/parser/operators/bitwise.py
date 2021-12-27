from typing import Dict, Optional
from .common import ParseBinaryOperator
from ..operands import ParseAtom, ParseInteger

class ParseBinaryAndIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"And({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(self._left.eval(vars).value & self._right.eval(vars).value)
def find_binary_and(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger) and isinstance(right, ParseInteger):
        return ParseBinaryAndIntegerInteger(left, right)
    else:
        return None

class ParseBinaryOrIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Or({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(self._left.eval(vars).value | self._right.eval(vars).value)
def find_binary_or(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger) and isinstance(right, ParseInteger):
        return ParseBinaryOrIntegerInteger(left, right)
    else:
        return None

class ParseBinaryXorIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Xor({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(self._left.eval(vars).value ^ self._right.eval(vars).value)
def find_binary_xor(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger) and isinstance(right, ParseInteger):
        return ParseBinaryXorIntegerInteger(left, right)
    else:
        return None

class ParseBinaryLeftIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Left({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(self._left.eval(vars).value << self._right.eval(vars).value)
def find_binary_left(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger) and isinstance(right, ParseInteger):
        return ParseBinaryLeftIntegerInteger(left, right)
    else:
        return None

class ParseBinaryRightIntegerInteger(ParseBinaryOperator, ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        super().__init__(left, right)
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Right({self._left!r}, {self._right!r})"
    def eval(self, vars: Dict[str, ParseAtom]) -> ParseInteger:
        return ParseInteger(self._left.eval(vars).value >> self._right.eval(vars).value)
def find_binary_right(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger) and isinstance(right, ParseInteger):
        return ParseBinaryRightIntegerInteger(left, right)
    else:
        return None
