from typing import Optional

from .add import find_binary_add
from ..operands import ParseAtom
from ...lexer import Token

from .common import ParseOperator

# binary
from .add import find_binary_add
from .subtract import find_binary_subtract
from .divide import find_binary_divide
from .bools import find_binary_and, find_binary_or, find_unary_not
from .match import find_binary_match

# unary
from .negative import find_unary_negative
from .positive import find_unary_positive

# ✨ special
from .variable import find_variable

def find_binary_operator(
        token: Token, left: ParseAtom, right: ParseAtom
        ) -> Optional[ParseAtom]:

    if token.text == "+":
        return find_binary_add(left, right)
    elif token.text == "-":
        return find_binary_subtract(left, right)
    elif token.text == "/":
        return find_binary_divide(left, right)
    elif token.text == "&&":
        return find_binary_and(left, right)
    elif token.text == "||":
        return find_binary_and(left, right)
    elif token.text == "=~":
        return find_binary_match(left, right)
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
    else:
        return None
