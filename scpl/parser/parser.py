from collections import deque
from dataclasses import dataclass
from typing      import Deque, Generic, List, TypeVar

from .operators  import *
from .operands   import *

from ..common    import *
from ..lexer     import *

class PreparseOperator:
    def __init__(self, token: Token):
        self.token = token
    def __repr__(self) -> str:
        return self.operator().name
    def weight(self):
        return self.operator().weight
    def operator(self) -> Operator:
        raise NotImplementedError()
class PreparseBinaryOperator(PreparseOperator):
    def operator(self) -> Operator:
        return OPERATORS_BINARY[self.token.text]
class PreparseUnaryOperator(PreparseOperator):
    def operator(self) -> Operator:
        return OPERATORS_UNARY[self.token.text]
class PreparseParenthesis(PreparseOperator):
    def weight(self):
        return 0

class ParserError(Exception):
    def __init__(self,
            token: Token,
            error: str):
        self.token = token
        super().__init__(error)

def parse(tokens: Deque[Token]):
    operands:  Deque[ParseAtom]        = deque()
    operators: Deque[PreparseOperator] = deque()

    def _pop_op() -> PreparseOperator:
        op_head = operators.pop()

        if isinstance(op_head, PreparseUnaryOperator):
            if not operands:
                raise ParserError(op_head.token, "missing unary operand")
            right = operands.pop()
            atom  = ParseUnaryOperator(op_head.token, right)
        else:
            if not len(operands) > 1:
                raise ParserError(op_head.token, "missing operand")
            right = operands.pop()
            left  = operands.pop()
            atom  = ParseBinaryOperator(op_head.token, left, right)

        operands.append(atom)
        return op_head

    last_is_operator = False
    while tokens:
        token = tokens.popleft()

        if isinstance(token, TokenTransparent):
            pass

        elif isinstance(token, TokenParenthesis):
            if token.text == "(":
                operators.append(PreparseParenthesis(token))
            else:
                while (operators and
                        not isinstance(operators[-1], PreparseParenthesis)):
                    _pop_op()

                if operators:
                    operators.pop()
                else:
                    raise ParserError(token, "unexpected closing parenthesis")

        elif isinstance(token, TokenOperator):
            if last_is_operator or not operands:
                if token.text in OPERATORS_UNARY:
                    operator = PreparseUnaryOperator(token)
                else:
                    raise ParserError(token, "invalid unary operator")
            else:
                if token.text in OPERATORS_BINARY:
                    operator = PreparseBinaryOperator(token)
                else:
                    raise ParserError(token, "invalid binary operator")

            # shunting yard
            while operators and operators[-1].weight() >= operator.weight():
                _pop_op()
            operators.append(operator)
            last_is_operator = True

        elif last_is_operator or not operands:
            last_is_operator = False
            if isinstance(token, TokenWord):
                if token.text in KEYWORDS:
                    keyword_type = KEYWORDS[token.text]
                    operands.append(keyword_type.from_token(token))
                else:
                    operands.append(ParseVariable.from_token(token))
            elif isinstance(token, TokenNumber):
                if "." in token.text:
                    operands.append(ParseFloat.from_token(token))
                else:
                    operands.append(ParseInteger.from_token(token))
            elif isinstance(token, TokenString):
                operands.append(ParseString.from_token(token))
            elif isinstance(token, TokenRegex):
                operands.append(ParseRegex.from_token(token))
            elif isinstance(token, TokenIPv4):
                operands.append(ParseIPv4.from_token(token))
        else:
            raise ParserError(token, "missing operator")

    while operators:
        if isinstance(operators[-1], PreparseParenthesis):
            raise ParserError(operators[-1].token, "unclosed parenthesis")
        else:
            _pop_op()

    return list(operands)
