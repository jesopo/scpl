from enum        import Enum
from dataclasses import dataclass
from typing      import Iterator, List, Optional, Sequence

class Associativity(Enum):
    LEFT = 0
    RIGHT = 1

@dataclass
class Operator:
    weight: int
    name: str
    associativity: Associativity = Associativity.LEFT

OPERATORS_BINARY = {
    "&&": Operator(1, "And"),
    "||": Operator(1, "Or"),
    "in": Operator(1, "SubsetOf"),
    "<":  Operator(2, "LesserThanb"),
    ">":  Operator(2, "GreaterThan"),
    "==": Operator(2, "Equal"),
    "!=": Operator(2, "Unequal"),
    "=~": Operator(2, "MatchOf"),

    "&":  Operator(1, "BitwiseAnd"),
    "|":  Operator(1, "BitwiseOr"),
    "+":  Operator(3, "Add"),
    "-":  Operator(3, "Subtract"),
    "/":  Operator(3, "Divide"),
    "*":  Operator(3, "Multiply"),
}

OPERATORS_UNARY = {
    "!":  Operator(4, "Not", Associativity.RIGHT),
    "+":  Operator(4, "Pos", Associativity.RIGHT),
    "-":  Operator(4, "Neg", Associativity.RIGHT)
}

def find_unescaped(
        s: str,
        c: str
        ) -> Iterator[int]:

    i = 0

    while i < len(s):
        c2 = s[i]
        if c2 == "\\":
            i += 1
        elif c2 == c:
            yield i
        i += 1

def find_unused_delimiter(
        s:     str,
        chars: Sequence[str]
        ) -> Optional[str]:

    for char in chars:
        try:
            next(find_unescaped(s, char))
        except StopIteration:
            return char
    else:
        return None

def with_delimiter(
        s:     str,
        chars: Sequence[str]
        ) -> str:

    if unused_delim := find_unused_delimiter(s, chars):
        delim = unused_delim
    else:
        delim  = chars[0]
        found  = find_unescaped(s, delim)
        rdelim = f"\\{delim}"
        for index in reversed(list(found)):
            s = s[:index] + rdelim + s[index+1:]

    return f"{delim}{s}{delim}"
