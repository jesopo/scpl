from collections import deque
from dataclasses import dataclass
from re          import compile as re_compile
from re          import escape as re_escape
from socket      import inet_ntop, inet_pton, AF_INET
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

    def _equal(self, other: "ParseAtom") -> "ParseBool":
        raise NotImplementedError()
    def _and(self, other: "ParseAtom") -> "ParseBool":
        return ParseBool(self._bool().value and other._bool().value)
    def _or(self, other: "ParseAtom") -> "ParseBool":
        return ParseBool(self._bool().value or other._bool().value)

    def _add(self, other: "ParseAtom") -> "ParseAtom":
        raise NotImplementedError()
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
    def _equal(self, other: ParseAtom) -> "ParseBool":
        return ParseBool(isinstance(other, ParseBool)
            and self.value == other.value)

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

    def _bool(self) -> ParseBool:
        return ParseBool(self.value != 0)

    def _equal(self, other: ParseAtom) -> ParseBool:
        return ParseBool(isinstance(other, ParseInteger)
            and self.value == other.value)

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

    def _equal(self, other: ParseAtom) -> ParseBool:
        return ParseBool(isinstance(other, ParseFloat)
            and self.value == other.value)

class ParseString(ParseAtom):
    def __init__(self,
            delim: Optional[str],
            value: str):

        self._delim = delim
        self.value  = value

    def __repr__(self) -> str:
        if self._delim is not None:
            return f"{self._delim}{self.value}{self._delim}"
        else:
            return with_delimiter(self.value, STRING_DELIMS)

    @staticmethod
    def from_token(token: Token) -> "ParseString":
        atom = ParseString(token.text[0], token.text[1:-1])
        atom.token = token
        return atom

    def _bool(self) -> bool:
        return ParseBool(len(self.value) > 0)

    def _equal(self, other: ParseAtom) -> ParseBool:
        return ParseBool(isinstance(other, ParseString)
            and self.value == other.value)

    def _add(self, other: ParseAtom) -> ParseAtom:
        if isinstance(other, ParseString):
            delim: Optional[str] = None
            if self._delim and self._delim == other._delim:
                delim = self._delim
            return ParseString(delim, self.value + other.value)
        elif isinstance(other, ParseRegex):
            cast_self = ParseRegex(None, re_escape(self.value), set())
            return cast_self._add(other)
        else:
            raise ParseBadOperandError()

    def _subset_of(self, other: ParseAtom) -> ParseAtom:
        if isinstance(other, ParseString):
            return ParseBool(self.value in other.value)
        else:
            raise ParseBadOperandError()

    def _match_of(self, other: ParseAtom) -> ParseAtom:
        if isinstance(other, ParseRegex):
            match = other.regex.search(self.value)
            value = match.group(0) if match else ""
            return ParseString(None, value)
        else:
            raise ParseBadOperandError()

class ParseRegex(ParseAtom):
    def __init__(self,
            delim: Optional[str],
            regex: str,
            flags: Set[str]):

        self._delim = delim
        self.flags  = flags
        self.regex  = re_compile(regex)
        self._regex = regex

    def __repr__(self) -> str:
        if self._delim is not None:
            regex = f"{self._delim}{self._regex}{self._delim}"
        else:
            regex = with_delimiter(self._regex, REGEX_DELIMS)

        flags = ''.join(self.flags)
        return f"Regex({regex}{flags})"

    @staticmethod
    def from_token(token: Token) -> "ParseRegex":
        delim, r = token.text[0], token.text[1:]
        r, flags = r.rsplit(delim, 1)

        atom = ParseRegex(delim, r, set(flags))
        atom.token = token
        return atom

    def _equal(self, other: ParseAtom) -> ParseBool:
        return ParseBool(isinstance(other, ParseRegex) and
            self.flags == other.flags and
            self._regex == other.regex)

    def _add(self, other: ParseAtom) -> ParseAtom:
        if isinstance(other, ParseRegex):
            common_flags = self.flags & other.flags
            regex_1      = self._regex
            regex_2      = other._regex

            if uncommon := self.flags - common_flags:
                regex_1 = f"(?{''.join(uncommon)}:{regex_1})"
            if uncommon := other.flags - common_flags:
                regex_2 = f"(?{''.join(uncommon)}:{regex_2})"

            delim: Optional[str] = None
            if (self._delim is not None
                    and self._delim == other._delim):
                delim = self._delim

            return ParseRegex(delim, regex_1 + regex_2, common_flags)
        else:
            raise ParseBadOperandError()

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

    def _equal(self, other: ParseAtom) -> ParseBool:
        return ParseBool(isinstance(other, ParseCIDRv4)
            and self._prefix  == other._prefix
            and self._network == other._network)

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

    def _equal(self, other: ParseAtom) -> "ParseBool":
        return (isinstance(other, ParseCIDRv4)
            and self._ip == other._ip)

    def _div(self, other: ParseAtom) -> ParseAtom:
        if isinstance(other, ParseInteger):
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
