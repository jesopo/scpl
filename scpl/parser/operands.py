from collections import deque
from dataclasses import dataclass
from re          import compile as re_compile
from re          import escape as re_escape
from socket      import inet_ntop, inet_pton, AF_INET, AF_INET6
from struct      import pack, unpack
from typing      import Any, Deque, Dict, List, Set, Type

from ..common    import *
from ..lexer     import *

# used for pretty printing when we don't have a delim already.
# it'll pick whichever doesn't already exist in the string, or pick [0] and
# escape all instances in the string
STRING_DELIMS = ['"', "'"]
REGEX_DELIMS  = ["/", ",", ";", ":"]

class ParseBadOperandError(Exception):
    pass

class ParseAtom:
    token: Optional[Token] = None

    @staticmethod
    def from_token(token: Token) -> "ParseAtom":
        raise NotImplementedError()

    def is_constant(self) -> bool:
        return True

    def eval(self, variables: Dict[str, "ParseAtom"]) -> "ParseAtom":
        return self

    def precompile(self):
        if self.is_constant():
            return self.eval({})
        else:
            return self

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

class ParseVariable(ParseAtom):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self) -> str:
        return f"Variable({self.name})"

    @staticmethod
    def from_token(token: Token) -> "ParseVariable":
        atom = ParseVariable(token.text)
        atom.token = token
        return atom

    def is_constant(self) -> bool:
        return False

    def eval(self, variables: Dict[str, ParseAtom]) -> ParseAtom:
        if self.name in variables:
            return variables[self.name]
        else:
            raise NameError(self.name)

class ParseInteger(ParseAtom):
    def __init__(self, value: int):
        self.value = value
    def __repr__(self) -> str:
        return f"Int({self.value})"

    @staticmethod
    def from_token(token: Token) -> "ParseInteger":
        atom = ParseInteger(int(token.text))
        atom.token = token
        return atom

class ParseFloat(ParseAtom):
    def __init__(self, value: float):
        self.value = value
    def __repr__(self) -> str:
        return f"Float({self.value})"

    @staticmethod
    def from_token(token: Token) -> "ParseFloat":
        atom = ParseFloat(float(token.text))
        atom.token = token
        return atom

class ParseString(ParseAtom):
    def __init__(self,
            delim: Optional[str],
            value: str):

        self.delimiter = delim
        self.value = value

    def __repr__(self) -> str:
        if self.delimiter is not None:
            return f"{self.delimiter}{self.value}{self.delimiter}"
        else:
            return with_delimiter(self.value, STRING_DELIMS)

    @staticmethod
    def from_token(token: Token) -> "ParseString":
        atom = ParseString(token.text[0], token.text[1:-1])
        atom.token = token
        return atom

class ParseRegex(ParseAtom):
    def __init__(self,
            delimiter: Optional[str],
            pattern: str,
            flags: Set[str]):

        self.delimiter = delimiter
        self.flags = flags
        self.compiled = re_compile(pattern)
        self.pattern = pattern

    def __repr__(self) -> str:
        if self.delimiter is not None:
            regex = f"{self.delimiter}{self.pattern}{self.delimiter}"
        else:
            regex = with_delimiter(self.pattern, REGEX_DELIMS)

        flags = ''.join(self.flags)
        return f"Regex({regex}{flags})"

    @staticmethod
    def from_token(token: Token) -> "ParseRegex":
        delim, r = token.text[0], token.text[1:]
        r, flags = r.rsplit(delim, 1)

        atom = ParseRegex(delim, r, set(flags))
        atom.token = token
        return atom

class ParseCIDR(ParseAtom):
    def __init__(self,
            network: int,
            prefix:  int,
            maxbits: int):

        self.prefix  = prefix
        # /8 becomes 0xFF000000
        self.mask    = 0xFF << (maxbits-prefix)
        # & here to remove any host bits
        self.integer = network & self.mask

class ParseCIDRv4(ParseCIDR):
    def __init__(self,
            network: int,
            prefix:  int):

        super().__init__(network, prefix, 32)

    def __repr__(self) -> str:
        bytes = pack("!L", self.integer)
        ntop  = inet_ntop(AF_INET, bytes)
        return f"CIDR({ntop}/{self.prefix})"

class ParseCIDRv6(ParseCIDR):
    def __init__(self,
            network: int,
            prefix:  int):

        super().__init__(network, prefix, 128)

    def __repr__(self) -> str:
        high = self.integer >> 64
        low = self.integer & ((1 << 64) - 1)
        bytes = pack("!2Q", high, low)
        ntop  = inet_ntop(AF_INET6, bytes)
        return f"CIDR({ntop}/{self.prefix})"

class ParseIPv4(ParseAtom):
    def __init__(self, ip: int):
        self.integer = ip
    def __repr__(self) -> str:
        bytes = pack("!L", self.integer)
        ntop  = inet_ntop(AF_INET, bytes)
        return f"IPv4({ntop})"

    @staticmethod
    def from_token(token: Token) -> "ParseIPv4":
        ip, *_ = unpack("!L", inet_pton(AF_INET, token.text))
        atom   = ParseIPv4(ip)
        atom.token = token
        return atom

class ParseIPv6(ParseAtom):
    def __init__(self, ip: int):
        self.integer = ip
    def __repr__(self) -> str:
        high = self.integer >> 64
        low = self.integer & ((1 << 64) - 1)
        bytes = pack("!2Q", high, low)
        ntop  = inet_ntop(AF_INET6, bytes)
        return f"IPv6({ntop})"

    @staticmethod
    def from_token(token: Token) -> "ParseIPv6":
        high, low = unpack('!2Q', inet_pton(AF_INET6, token.text))
        integer = (high << 64) | low
        atom = ParseIPv6(integer)
        atom.token = token
        return atom

KEYWORDS: Dict[str, Type[ParseAtom]] = {
    "true":  ParseBool,
    "false": ParseBool
}
