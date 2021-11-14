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
    "+":  Operator(3, "Add"),
    "-":  Operator(3, "Subtract"),
    "/":  Operator(3, "Divide"),
    "*":  Operator(3, "Multiply"),
}

OPERATORS_UNARY = {
    "!":  Operator(3, "Not"),
    "+":  Operator(3, "Pos"),
    "-":  Operator(3, "Neg"),
}
