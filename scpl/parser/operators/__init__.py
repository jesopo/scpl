from typing import Optional

from .add import find_binary_add
from ..operands import ParseAtom
from ...lexer import Token
from ...common.operators import OperatorName

# binary
from .add import find_binary_add
from .subtract import find_binary_subtract
from .multiply import find_binary_multiply
from .divide import find_binary_divide
from .exponent import find_binary_exponent
from .lesser import find_binary_lesser
from .greater import find_binary_greater
from .bools import find_binary_both, find_binary_either, find_unary_not
from .match import find_binary_match
from .contains import find_binary_contains
from .equal import find_binary_equal
from .bitwise import (find_binary_and, find_binary_or, find_binary_xor,
    find_binary_left, find_binary_right)

# unary
from .negative import find_unary_negative
from .positive import find_unary_positive
from .complement import find_unary_complement

# ✨ special
from .variable import find_variable
from .set import find_set

def find_binary_operator(
        op_name: OperatorName, left: ParseAtom, right: ParseAtom
        ) -> Optional[ParseAtom]:

    if op_name == OperatorName.ADD:
        return find_binary_add(left, right)
    elif op_name == OperatorName.SUBTRACT:
        return find_binary_subtract(left, right)
    elif op_name == OperatorName.MULTIPLY:
        return find_binary_multiply(left, right)
    elif op_name == OperatorName.DIVIDE:
        return find_binary_divide(left, right)
    elif op_name == OperatorName.EXPONENT:
        return find_binary_exponent(left, right)
    elif op_name == OperatorName.BOTH:
        return find_binary_both(left, right)
    elif op_name == OperatorName.EITHER:
        return find_binary_either(left, right)
    elif op_name == OperatorName.MATCH:
        return find_binary_match(left, right)
    elif op_name == OperatorName.CONTAINS:
        return find_binary_contains(left, right)
    elif op_name == OperatorName.GREATER:
        return find_binary_greater(left, right)
    elif op_name == OperatorName.LESSER:
        return find_binary_lesser(left, right)
    elif op_name == OperatorName.EQUAL:
        return find_binary_equal(left, right)
    elif op_name == OperatorName.UNEQUAL:
        # just treat != as !(==)
        if (inner := find_binary_equal(left, right)) is not None:
            return find_unary_not(inner)
        else:
            return None
    elif op_name == OperatorName.AND:
        return find_binary_and(left, right)
    elif op_name == OperatorName.OR:
        return find_binary_or(left, right)
    elif op_name == OperatorName.XOR:
        return find_binary_xor(left, right)
    elif op_name == OperatorName.LEFT:
        return find_binary_left(left, right)
    elif op_name == OperatorName.RIGHT:
        return find_binary_right(left, right)
    else:
        return None

def find_unary_operator(
        op_name: OperatorName, atom: ParseAtom
        ) -> Optional[ParseAtom]:

    if op_name == OperatorName.NEGATIVE:
        return find_unary_negative(atom)
    elif op_name == OperatorName.POSITIVE:
        return find_unary_positive(atom)
    elif op_name == OperatorName.NOT:
        return find_unary_not(atom)
    elif op_name == OperatorName.COMPLEMENT:
        return find_unary_complement(atom)
    else:
        return None
