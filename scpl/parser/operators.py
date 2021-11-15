from collections import deque
from dataclasses import dataclass
from typing      import Any, Deque, Generic, List, TypeVar

from ..common    import Operator, OPERATORS_BINARY, OPERATORS_UNARY
from ..lexer     import Token
from .operands   import *

class ParseOperator(ParseAtom):
    pass

class ParseBinaryOperator(ParseOperator):
    def __init__(self,
            token: Token,
            left:  ParseAtom,
            right: ParseAtom):
        self.token = token
        self.left  = left
        self.right = right
    def __repr__(self) -> str:
        name = OPERATORS_BINARY[self.token.text].name
        return f"{name}({self.left!r}, {self.right!r})"

    def is_constant(self) -> bool:
        return (self.left.is_constant()
            and self.right.is_constant())

    def precompile(self):
        self.left  = self.left.precompile()
        self.right = self.right.precompile()
        return super().precompile()

    def eval(self, vars: Dict[str, "ParseAtom"]) -> "ParseAtom":
        left  = self.left.eval(vars)
        right = self.right.eval(vars)

        if self.token.text == "==":
            atom = left._equal(right)
        elif self.token.text == "&&":
            atom = left._bool()._and(right)
        elif self.token.text == "||":
            atom = left._bool()._or(right)
        elif self.token.text == "in":
            atom = left._subset_of(right)
        elif self.token.text == "=~":
            atom = left._match_of(right)
        elif self.token.text == "+":
            atom = left._add(right)
        elif self.token.text == "-":
            atom = left._subtract(right)
        elif self.token.text == "/":
            atom = left._div(right)
        else:
            raise NotImplementedError()

        if self.is_constant():
            atom.token = self.token
        return atom

class ParseUnaryOperator(ParseOperator):
    def __init__(self,
            token: Token,
            atom:  ParseAtom):
        self.token = token
        self.atom  = atom
    def __repr__(self) -> str:
        name = OPERATORS_UNARY[self.token.text].name
        return f"{name}({self.atom!r})"

    def is_constant(self) -> bool:
        return self.atom.is_constant()

    def precompile(self) -> ParseAtom:
        self.atom = self.atom.precompile()
        return super().precompile()

    def eval(self, vars: Dict[str, "ParseAtom"]) -> "ParseAtom":
        atom = self.atom.eval(vars)

        if self.token.text == "!":
            atom = ParseBool(not atom._bool())
        else:
            raise NotImplementedError()

        if self.is_constant():
            atom.token = self.token
        return atom
