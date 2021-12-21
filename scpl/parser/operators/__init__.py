from .add import find_binary_add
from ..operands import *

# binary
from .add import find_binary_add
from .divide import find_binary_divide

# unary
from ._not import find_unary_not
from .negative import find_unary_negative

# ✨ special
from .variable import find_variable

def find_binary_operator(
        token: Token, left: ParseAtom, right: ParseAtom
        ) -> Optional[ParseAtom]:

    if token.text == "+":
        return find_binary_add(left, right)
    elif token.text == "/":
        return find_binary_divide(left, right)
    else:
        return None

def find_unary_operator(
        token: Token, atom: ParseAtom
        ) -> Optional[ParseAtom]:

    if token.text == "-":
        return find_unary_negative(atom)
    elif token.text == "!":
        return find_unary_not(atom)
    else:
        return None
