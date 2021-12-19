from ..operands import *

class ParseBinaryAddIntegerInteger(ParseInteger):
    def __init__(self, left: ParseInteger, right: ParseInteger):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        return ParseInteger(self._left.value + self._right.value)

class ParseBinaryAddFloatFloat(ParseFloat):
    def __init__(self, left: ParseFloat, right: ParseFloat):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        return ParseFloat(self._left.value + self._right.value)

class ParseBinaryAddStringString(ParseString):
    def __init__(self, left: ParseString, right: ParseString):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        return ParseString(None, self._left.value + self._right.value)

class ParseBinaryAddRegexRegex(ParseRegex):
    def __init__(self, left: ParseRegex, right: ParseRegex):
        self._left = left
        self._right = right
    def __repr__(self) -> str:
        return f"Add({self._left!r}, {self._right!r})"
    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        common_flags = self._left.flags & self._right.flags
        regex_1      = self._left.pattern
        regex_2      = self._right.pattern

        if uncommon := self._left.flags - common_flags:
            regex_1 = f"(?{''.join(uncommon)}:{regex_1})"
        if uncommon := self._right.flags - common_flags:
            regex_2 = f"(?{''.join(uncommon)}:{regex_2})"

        delim: Optional[str] = None
        if (self._left.delimiter is not None
                and self._left.delimiter == self._right.delimiter):
            delim = self._left.delimiter

        return ParseRegex(delim, regex_1 + regex_2, common_flags)
class ParseBinaryAddRegexString(ParseBinaryAddRegexRegex):
    def __init__(self, left: ParseRegex, right: ParseString):
        super().__init__(left, ParseRegex(None, re_escape(right.value), set()))
class ParseBinaryAddStringRegex(ParseBinaryAddRegexRegex):
    def __init__(self, left: ParseString, right: ParseRegex):
        super().__init__(ParseRegex(None, re_escape(left.value), set()), right)

def find_binary_add(left: ParseAtom, right: ParseAtom) -> Optional[ParseAtom]:
    if isinstance(left, ParseInteger):
        if isinstance(right, ParseInteger):
            return ParseBinaryAddIntegerInteger(left, right)
        else:
            return None
    elif isinstance(left, ParseFloat):
        if isinstance(right, ParseFloat):
            return ParseBinaryAddFloatFloat(left, right)
        else:
            return None
    elif isinstance(left, ParseString):
        if isinstance(right, ParseString):
            return ParseBinaryAddStringString(left, right)
        elif isinstance(right, ParseRegex):
            return ParseBinaryAddStringRegex(left, right)
        else:
            return None
    elif isinstance(left, ParseRegex):
        if isinstance(right, ParseRegex):
            return ParseBinaryAddRegexRegex(left, right)
        elif isinstance(right, ParseString):
            return ParseBinaryAddRegexString(left, right)
        else:
            return None
    else:
        return None
