from typing import Optional

from .add import find_binary_add
from ..operands import ParseAtom
from ...lexer import Token

from .common import ParseOperator

# binary
from .add import find_binary_add
from .subtract import find_binary_subtract
from .multiply import find_binary_multiply
from .divide import find_binary_divide
from .lesser import find_binary_lesser
from .greater import find_binary_greater
from .bools import find_binary_and, find_binary_or, find_unary_not
from .match import find_binary_match
from .contains import find_binary_contains

# unary
from .negative import find_unary_negative
from .positive import find_unary_positive
from .complement import find_unary_complement

# ✨ special
from .variable import find_variable

def find_binary_operator(
        token: Token, left: ParseAtom, right: ParseAtom
        ) -> Optional[ParseAtom]:

    if token.text == "+":
        return find_binary_add(left, right)
    elif token.text == "-":
        return find_binary_subtract(left, right)
    elif token.text == "*":
        return find_binary_multiply(left, right)
    elif token.text == "/":
        return find_binary_divide(left, right)
    elif token.text == "&&":
        return find_binary_and(left, right)
    elif token.text == "||":
        return find_binary_and(left, right)
    elif token.text == "=~":
        return find_binary_match(left, right)
    elif token.text == "in":
        return find_binary_contains(left, right)
    elif token.text == ">":
        return find_binary_greater(left, right)
    elif token.text == "<":
        return find_binary_lesser(left, right)
    else:
        return None

def find_unary_operator(
        token: Token, atom: ParseAtom
        ) -> Optional[ParseAtom]:

    if token.text == "-":
        return find_unary_negative(atom)
    if token.text == "+":
        return find_unary_positive(atom)
    elif token.text == "!":
        return find_unary_not(atom)
    elif token.text == "~":
        return find_unary_complement(atom)
    else:
        return None
