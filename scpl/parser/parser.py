from collections import deque
from dataclasses import dataclass
from typing      import Deque, Generic, List, Sequence, Set, TypeVar

from .operators  import find_binary_operator, find_unary_operator, find_variable
from .operands   import *

from ..common.operators import (Associativity, OPERATORS, OPERATORS_BINARY,
    OPERATORS_UNARY, OperatorName)
from ..lexer import (Token, TokenDuration, TokenHex, TokenIPv4, TokenIPv6, TokenNumber,
    TokenOperator, TokenParenthesis, TokenRegex, TokenString, TokenTransparent,
    TokenWord)

class ParserError(Exception):
    def __init__(self,
            token: Token,
            error: str):
        self.token = token
        super().__init__(error)

def parse(
        tokens: Deque[Token],
        types: Dict[str, type]
        ) -> Tuple[Sequence[ParseAtom], Set[str]]:

    operands:  Deque[ParseAtom] = deque()
    operators: Deque[Tuple[OperatorName, Token]] = deque()
    dependencies: Set[str] = set()

    def _pop_op() -> OperatorName:
        op_head_name, op_head_token = operators.pop()
        op_head = OPERATORS[op_head_name]

        if op_head.operands() == 1:
            if not operands:
                raise ParserError(op_head_token, "missing unary operand")
            right = operands.pop()
            atom  = find_unary_operator(op_head_name, right)
        else:
            if not len(operands) > 1:
                raise ParserError(op_head_token, "missing binary operand")
            right = operands.pop()
            left  = operands.pop()
            atom  = find_binary_operator(op_head_name, left, right)

        if atom is not None:
            operands.append(atom)
            return op_head_name
        else:
            raise ParserError(op_head_token, "invalid operands for operator")

    last_is_operator = False
    while tokens:
        token = tokens.popleft()

        if isinstance(token, TokenTransparent):
            pass

        elif isinstance(token, TokenParenthesis):
            if token.text == "(":
                operators.append((OperatorName.PARENTHESIS, token))
            else:
                while operators and not operators[-1] == OperatorName.PARENTHESIS:
                    _pop_op()

                if operators:
                    operators.pop()
                else:
                    raise ParserError(token, "unexpected closing parenthesis")

        elif isinstance(token, TokenOperator):
            if last_is_operator or not operands:
                if token.text in OPERATORS_UNARY:
                    op_new_name = OPERATORS_UNARY[token.text]
                else:
                    raise ParserError(token, "invalid unary operator")
            else:
                if token.text in OPERATORS_BINARY:
                    op_new_name = OPERATORS_BINARY[token.text]
                else:
                    raise ParserError(token, "invalid binary operator")

            op_new = OPERATORS[op_new_name]

            # shunting yard
            while operators:
                op_head_name, _ = operators[-1]
                op_head = OPERATORS[op_head_name]

                if (op_head.associativity == Associativity.LEFT
                        and op_head.weight >= op_new.weight):
                    _pop_op()
                elif (op_head.associativity == Associativity.RIGHT
                        and op_head.weight > op_new.weight):
                    _pop_op()
                else:
                    break

            operators.append((op_new_name, token))
            last_is_operator = True

        elif last_is_operator or not operands:
            last_is_operator = False
            if isinstance(token, TokenWord):
                if token.text in KEYWORDS:
                    keyword_type = KEYWORDS[token.text]
                    operands.append(keyword_type.from_token(token))
                elif (var_type := types.get(token.text)) is None:
                    raise ParserError(token, f"unknown variable {token.text}")
                elif (var := find_variable(token.text, var_type)) is None:
                    # shouldn't happen
                    raise ParserError(token, f"invalid variable type {var_type!r}")
                else:
                    dependencies.add(token.text)
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
        op_head_name, op_head_token = operators[-1]
        if op_head_name == OperatorName.PARENTHESIS:
            raise ParserError(op_head_token, "unclosed parenthesis")
        else:
            _pop_op()

    return list(operands), dependencies
