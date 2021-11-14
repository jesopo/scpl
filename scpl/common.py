from dataclasses import dataclass

@dataclass
class Operator:
    weight: int
    name:   str

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
    "+":  Operator(1, "Add"),
    "-":  Operator(1, "Subtract"),
    "/":  Operator(2, "Divide"),
    "*":  Operator(2, "Multiply"),
}

OPERATORS_UNARY = {
    "!":  Operator(3, "Not"),
    "+":  Operator(3, "Pos"),
    "-":  Operator(3, "Neg"),
}
