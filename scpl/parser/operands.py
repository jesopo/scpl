from collections import deque
from dataclasses import dataclass
from re          import compile as re_compile
from socket      import inet_ntop, inet_pton, AF_INET
from struct      import pack, unpack
from typing      import Any, Deque, Dict, List, Type

from ..common    import *
from ..lexer     import *

class ParseBadOperandError(Exception):
    pass

class ParseAtom:
    token: Optional[Token] = None

    @staticmethod
    def from_token(token: Token) -> "ParseAtom":
        raise NotImplementedError()

    def is_constant(self) -> bool:
        return self.token is not None

    def eval(self,
            variables: Dict[str, "ParseAtom"]
            ) -> "ParseAtom":
        return self
    def precompile(self) -> "ParseAtom":
        if self.is_constant():
            return self.eval({})
        else:
            return self

    def _bool(self) -> "ParseBool":
        raise NotImplementedError()

    def _and(self, other: "ParseAtom") -> "ParseBool":
        return ParseBool(self._bool().value and other._bool().value)
    def _or(self, other: "ParseAtom") -> "ParseBool":
        return ParseBool(self._bool().value or other._bool().value)

    def _div(self, other: "ParseAtom") -> "ParseAtom":
        raise NotImplementedError()

    def _subset_of(self, other: "ParseAtom") -> bool:
        raise NotImplementedError()
    def _match_of(self, other: "ParseAtom") -> "ParseAtom":
        raise NotImplementedError()

class ParseBool(ParseAtom):
    def __init__(self, value: bool):
        self.value = value
    def __repr__(self) -> str:
        tostr = {True: "true", False: "false"}[self.value]
        return f"Bool({tostr})"

    @staticmethod
    def from_token(token: Token) -> "ParseBool":
        atom = ParseBool({"true": True, "false": False}[token.text])
        atom.token = token
        return atom

    def _bool(self) -> bool:
        return self

class ParseVariable(ParseAtom):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self) -> str:
        return f"Variable({self.token.text})"

    @staticmethod
    def from_token(token: Token) -> "ParseVariable":
        atom = ParseVariable(token.text)
        atom.token = token
        return atom

    def is_constant(self) -> bool:
        return False

    def eval(self,
            variables: Dict[str, "ParseAtom"]
            ) -> "ParseAtom":

        if self.name in variables:
            return variables[self.name]
        else:
            raise NameError(self.name)

class ParseInt(ParseAtom):
    def __init__(self, value: int):
        self.value = value
    def __repr__(self) -> str:
        return f"Int({self.value})"

    @staticmethod
    def from_token(token: Token) -> "ParseInt":
        atom = ParseInt(int(token.text))
        atom.token = token
        return atom

    def _bool(self) -> ParseBool:
        return ParseBool(self.value != 0)

class ParseFloat(ParseAtom):
    def __init__(self, token: Token):
        super().__init__(token)
        self.value = float(token.text)
    def __repr__(self) -> str:
        return f"Float({self.value})"

    @staticmethod
    def from_token(token: Token) -> "ParseFloat":
        atom = ParseFloat(float(token.text))
        atom.token = token
        return atom

class ParseString(ParseAtom):
    def __init__(self, value: str):
        self.value = value
    def __repr__(self) -> str:
        return f"String({self.value})"

    @staticmethod
    def from_token(token: Token) -> "ParseString":
        atom = ParseString(token.text[1:-1])
        atom.token = token
        return atom

    def _bool(self) -> bool:
        return ParseBool(len(self.value) > 0)

    def _subset_of(self, other: ParseAtom) -> ParseAtom:
        if isinstance(other, ParseString):
            return ParseBool(self.value in other.value)
        else:
            raise ParseBadOperandError()

    def _match_of(self, other: ParseAtom) -> ParseAtom:
        if isinstance(other, ParseRegex):
            match = other.regex.search(self.value)
            value = match.group(0) if match else ""
            return ParseString(value)
        else:
            raise ParseBadOperandError()

class ParseRegex(ParseAtom):
    def __init__(self, regex: str):
        delim, r = regex[0], regex[1:]
        r, flags = r.rsplit(delim, 1)

        self.delim = delim
        self.flags = flags
        self.regex = re_compile(r)

    def __repr__(self) -> str:
        return f"Regex({self.token.text})"

    @staticmethod
    def from_token(token: Token) -> "ParseRegex":
        atom = ParseRegex(token.text)
        atom.token = token
        return atom

class ParseCIDRv4(ParseAtom):
    def __init__(self,
            network: int,
            prefix:  int):

        self._prefix  = prefix
        # /8 becomes 0xFF000000
        self._mask    = 0xFF << (32-prefix)
        # & here to remove any host bits
        self._network = network & self._mask

    def __repr__(self) -> str:
        bytes = pack("!L", self._network)
        ntop  = inet_ntop(AF_INET, bytes)
        return f"CIDR({ntop}/{self._prefix})"

    def _bool(self) -> bool:
        return ParseBool(True)

class ParseIPv4(ParseAtom):
    def __init__(self, ip: int):
        self._ip = ip
    def __repr__(self) -> str:
        bytes = pack("!L", self._ip)
        ntop  = inet_ntop(AF_INET, bytes)
        return f"IPv4({ntop})"

    @staticmethod
    def from_token(token: Token) -> "ParseIPv4":
        ip, *_ = unpack("!L", inet_pton(AF_INET, token.text))
        atom   = ParseIPv4(ip)
        atom.token = token
        return atom

    def _bool(self):
        return ParseBool(True)

    def _div(self, other: ParseAtom) -> ParseAtom:
        if isinstance(other, ParseInt):
            return ParseCIDRv4(self._ip, other.value)
        else:
            raise ParseBadOperandError()

    def _subset_of(self, other: ParseAtom) -> ParseAtom:
        if isinstance(other, ParseCIDRv4):
            network = self._ip & other._mask
            return ParseBool(network == other._network)
        else:
            raise ParseBadOperandError()

KEYWORDS: Dict[str, Type[ParseAtom]] = {
    "true":  ParseBool,
    "false": ParseBool
}
