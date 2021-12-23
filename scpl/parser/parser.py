from collections import deque
from dataclasses import dataclass
from typing      import Deque, Generic, List, TypeVar

from .operators  import find_binary_operator, find_unary_operator, find_variable
from .operands   import *

from ..common    import *
from ..lexer     import *

class PreparseOperator:
    def __init__(self, token: Token):
        self.token = token
    def __repr__(self) -> str:
        return self.operator().name
    def operator(self) -> Operator:
        raise NotImplementedError()
    def weight(self):
        return self.operator().weight
    def is_left(self):
        return self.operator().associativity == Associativity.LEFT
    def is_right(self):
        return self.operator().associativity == Associativity.RIGHT
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

def parse(tokens: Deque[Token], types: Dict[str, type]):
    operands:  Deque[ParseAtom]        = deque()
    operators: Deque[PreparseOperator] = deque()

    def _pop_op() -> PreparseOperator:
        op_head = operators.pop()

        if isinstance(op_head, PreparseUnaryOperator):
            if not operands:
                raise ParserError(op_head.token, "missing unary operand")
            right = operands.pop()
            atom  = find_unary_operator(op_head.token, right)
        else:
            if not len(operands) > 1:
                raise ParserError(op_head.token, "missing binary operand")
            right = operands.pop()
            left  = operands.pop()
            atom  = find_binary_operator(op_head.token, left, right)

        if atom is not None:
            operands.append(atom)
            return op_head
        else:
            raise ParserError(op_head.token, "invalid operands for operator")

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
            operator: PreparseOperator
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

            weight = operator.weight()
            # shunting yard
            while operators:
                head = operators[-1]
                if ((head.is_left() and head.weight() >= weight)
                        or (head.is_right() and head.weight() > weight)):
                    _pop_op()
                else:
                    break

            operators.append(operator)
            last_is_operator = True

        elif last_is_operator or not operands:
            last_is_operator = False
            if isinstance(token, TokenWord):
                if token.text in KEYWORDS:
                    keyword_type = KEYWORDS[token.text]
                    operands.append(keyword_type.from_token(token))
                else:
                    if not token.text in types:
                        raise ParserError(token, f"unknown variable {token.text}")
                    elif (var := find_variable(token.text, types)) is None:
                        # shouldn't happen
                        raise ParserError(token, "invalid variable type")
                    else:
                        operands.append(var)

            elif isinstance(token, TokenNumber):
                if "." in token.text:
                    operands.append(ParseFloat.from_token(token))
                else:
                    operands.append(ParseInteger.from_token(token))
            elif isinstance(token, TokenHex):
                operands.append(ParseHex.from_token(token))
            elif isinstance(token, TokenDuration):
                operands.append(ParseDuration.from_token(token))
            elif isinstance(token, TokenString):
                operands.append(ParseString.from_token(token))
            elif isinstance(token, TokenRegex):
                operands.append(ParseRegex.from_token(token))
            elif isinstance(token, TokenIPv4):
                if "/" in token.text:
                    operands.append(ParseCIDRv4.from_token(token))
                else:
                    operands.append(ParseIPv4.from_token(token))
            elif isinstance(token, TokenIPv6):
                if "/" in token.text:
                    operands.append(ParseCIDRv6.from_token(token))
                else:
                    operands.append(ParseIPv6.from_token(token))
            else:
                raise ParserError(token, "unknown token")
        else:
            raise ParserError(token, "missing operator")

    while operators:
        if isinstance(operators[-1], PreparseParenthesis):
            raise ParserError(operators[-1].token, "unclosed parenthesis")
        else:
            _pop_op()

    return list(operands)
