from enum        import auto, Enum
from dataclasses import dataclass

class Associativity(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2

@dataclass
class Operator:
    weight: int
    left_operands: int
    right_operands: int
    associativity: Associativity

    def operands(self) -> int:
        return self.left_operands + self.right_operands

# done in order of precedence
class OperatorName(Enum):
    # special
    SCOPE = auto()
    COMMA = auto()
    # binary boolean
    BOTH = auto()
    EITHER = auto()
    CONTAINS = auto()
    GREATER = auto()
    LESSER = auto()
    EQUAL = auto()
    UNEQUAL = auto()
    MATCH = auto()
    # binary arithmetic
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    EXPONENT = auto()
    # binary bitwise
    AND = auto()
    OR = auto()
    XOR = auto()
    LEFT = auto()
    RIGHT = auto()
    # unary boolean
    NOT = auto()
    # unary arithmetic
    POSITIVE = auto()
    NEGATIVE = auto()
    # unary bitwise
    COMPLEMENT = auto()

OPERATORS = {
    # SCOPE ([]{}()) is subject to special rules due to associativity
    OperatorName.SCOPE: Operator(0, 0, 0, Associativity.NONE),
    OperatorName.COMMA: Operator(0, 0, 0, Associativity.NONE),
    OperatorName.EITHER: Operator(1, 1, 1, Associativity.LEFT),
    OperatorName.BOTH: Operator(2, 1, 1, Associativity.LEFT),
    OperatorName.EQUAL: Operator(3, 1, 1, Associativity.LEFT),
    OperatorName.UNEQUAL: Operator(3, 1, 1, Associativity.LEFT),
    OperatorName.GREATER: Operator(3, 1, 1, Associativity.LEFT),
    OperatorName.LESSER: Operator(3, 1, 1, Associativity.LEFT),
    OperatorName.CONTAINS: Operator(3, 1, 1, Associativity.LEFT),
    OperatorName.MATCH: Operator(3, 1, 1, Associativity.LEFT),
    OperatorName.OR: Operator(4, 1, 1, Associativity.LEFT),
    OperatorName.XOR: Operator(5, 1, 1, Associativity.LEFT),
    OperatorName.AND: Operator(6, 1, 1, Associativity.LEFT),
    OperatorName.LEFT: Operator(7, 1, 1, Associativity.LEFT),
    OperatorName.RIGHT: Operator(7, 1, 1, Associativity.LEFT),
    OperatorName.ADD: Operator(8, 1, 1, Associativity.LEFT),
    OperatorName.SUBTRACT: Operator(8, 1, 1, Associativity.LEFT),
    OperatorName.MULTIPLY: Operator(9, 1, 1, Associativity.LEFT),
    OperatorName.DIVIDE: Operator(9, 1, 1, Associativity.LEFT),
    OperatorName.MODULO: Operator(9, 1, 1, Associativity.LEFT),
    OperatorName.EXPONENT: Operator(10, 1, 1, Associativity.RIGHT),
    OperatorName.NOT: Operator(11, 0, 1, Associativity.RIGHT),
    OperatorName.POSITIVE: Operator(11, 0, 1, Associativity.RIGHT),
    OperatorName.NEGATIVE: Operator(11, 0, 1, Associativity.RIGHT),
    OperatorName.COMPLEMENT: Operator(12, 0, 1, Associativity.RIGHT),
}

OPERATORS_BINARY = {
    ",":  OperatorName.COMMA,
    "&&": OperatorName.BOTH,
    "||": OperatorName.EITHER,
    "in": OperatorName.CONTAINS,
    "<":  OperatorName.LESSER,
    ">":  OperatorName.GREATER,
    "==": OperatorName.EQUAL,
    "!=": OperatorName.UNEQUAL,
    "=~": OperatorName.MATCH,
    "&":  OperatorName.AND,
    "|":  OperatorName.OR,
    "^":  OperatorName.XOR,
    "<<": OperatorName.LEFT,
    ">>": OperatorName.RIGHT,
    "+":  OperatorName.ADD,
    "-":  OperatorName.SUBTRACT,
    "/":  OperatorName.DIVIDE,
    "*":  OperatorName.MULTIPLY,
    "%":  OperatorName.MODULO,
    "**": OperatorName.EXPONENT,
}

OPERATORS_UNARY = {
    "!": OperatorName.NOT,
    "+": OperatorName.POSITIVE,
    "-": OperatorName.NEGATIVE,
    "~": OperatorName.COMPLEMENT,
}
