from collections import deque, OrderedDict
from dataclasses import dataclass
from re          import compile as re_compile
from re          import escape as re_escape
from socket      import inet_ntop, inet_pton, AF_INET, AF_INET6
from struct      import pack, unpack
from typing      import Any, Deque, Dict, List, Optional, Set, Tuple, Type
from typing      import OrderedDict as TOrderedDict

from ..common.util import with_delimiter

# used for pretty printing when we don't have a delim already.
# it'll pick whichever doesn't already exist in the string, or pick [0] and
# escape all instances in the string
STRING_DELIMS = ['"', "'"]
REGEX_DELIMS  = ["/", ",", ";", ":"]

class ParseBadOperandError(Exception):
    pass

class ParseAtom:
    def __eq__(self, other: object):
        return (type(self) == type(other)
            and hash(self) == hash(other))

    @staticmethod
    def from_text(text: str) -> "ParseAtom":
        raise NotImplementedError()

    def is_constant(self) -> bool:
        return True

class ParseBool(ParseAtom):
    def __init__(self, value: bool):
        self.value = value
    def __repr__(self) -> str:
        tostr = {True: "true", False: "false"}[self.value]
        return f"Bool({tostr})"

    @staticmethod
    def from_text(text: str) -> "ParseBool":
        return ParseBool({"true": True, "false": False}[text])

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseBool":
        return self

class ParseInteger(ParseAtom):
    def __init__(self, value: int):
        self.value = value
    def __repr__(self) -> str:
        return f"Integer({self.value})"
    def __hash__(self) -> int:
        return hash(self.value)

    @staticmethod
    def from_text(text: str) -> "ParseInteger":
        return ParseInteger(int(text))

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseInteger":
        return self

# sneaky little trick. convert hex to integer
class ParseHex(ParseInteger):
    @staticmethod
    def from_text(text: str) -> ParseInteger:
        return ParseInteger(int(text[2:], 16))

DURATION_UNITS: TOrderedDict[str, int] = OrderedDict(reversed([
    ("s", 1),
    ("m", SECONDS_M := 60),
    ("h", SECONDS_H := SECONDS_M * 60),
    ("d", SECONDS_D := SECONDS_H * 24),
    ("w", SECONDS_W := SECONDS_D * 7)
]))
RE_DURATION = re_compile("^(\d+w)?(\d+d)?(\d+h)?(\d+m)?(\d+s)?$")

class ParseDuration(ParseInteger):
    def __repr__(self) -> str:
        seconds = self.value
        out = ""
        for unit, scale in DURATION_UNITS.items():
            unit_value, seconds = divmod(seconds, scale)
            if unit_value > 0:
                out += f"{unit_value}{unit}"

        return f"Duration({out})"

    @staticmethod
    def from_text(text: str) -> "ParseInteger":
        seconds = 0
        if (match := RE_DURATION.search(text)) is not None:
            for group in match.groups():
                if group is not None:
                    value_s, unit = group[:-1], group[-1]
                    scale = DURATION_UNITS[unit]
                    seconds += int(value_s) * scale

        return ParseInteger(seconds)

class ParseFloat(ParseAtom):
    def __init__(self, value: float):
        self.value = value
    def __repr__(self) -> str:
        return f"Float({self.value})"
    def __hash__(self) -> int:
        return hash(self.value)

    @staticmethod
    def from_text(text: str) -> "ParseFloat":
        return ParseFloat(float(text))

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseFloat":
        return self

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
    def __hash__(self) -> int:
        return hash(self.value)

    @staticmethod
    def from_text(text: str) -> "ParseString":
        return ParseString(text[0], text[1:-1])

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseString":
        return self

class ParseRegex(ParseAtom):
    def __init__(self,
            delimiter: Optional[str],
            pattern: str,
            flags: Set[str],
            expected: bool):

        self.delimiter = delimiter
        self.pattern = pattern
        self.flags = flags
        self.expected = expected
        self.compiled = re_compile(pattern)

    def __str__(self) -> str:
        if self.delimiter is not None:
            regex = f"{self.delimiter}{self.pattern}{self.delimiter}"
        else:
            regex = with_delimiter(self.pattern, REGEX_DELIMS)
        flags = ''.join(self.flags)
        if not self.expected:
            regex = f"~{regex}"
        return f"{regex}{flags}"

    def __repr__(self) -> str:
        return f"Regex({str(self)})"
    def __hash__(self) -> int:
        return hash(self.compiled)

    @staticmethod
    def from_text(text: str) -> "ParseRegex":
        delim, r = text[0], text[1:]
        r, flags = r.rsplit(delim, 1)

        return ParseRegex(delim, r, set(flags), True)

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseRegex":
        return self

class ParseIP(ParseAtom):
    def __init__(self, ip: int):
        self.integer = ip
    def __hash__(self) -> int:
        return hash(self.integer)

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseIP":
        return self

class ParseIPv4(ParseIP):
    def __repr__(self) -> str:
        bytes = pack("!L", self.integer)
        ntop  = inet_ntop(AF_INET, bytes)
        return f"IPv4({ntop})"

    @staticmethod
    def to_int(text: str) -> int:
        ip, *_ = unpack("!L", inet_pton(AF_INET, text))
        return ip

    @staticmethod
    def from_text(text: str) -> "ParseIPv4":
        return ParseIPv4(ParseIPv4.to_int(text))

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseIPv4":
        return self

class ParseIPv6(ParseIP):
    def __repr__(self) -> str:
        high = self.integer >> 64
        low = self.integer & ((1 << 64) - 1)
        bytes = pack("!2Q", high, low)
        ntop  = inet_ntop(AF_INET6, bytes)
        return f"IPv6({ntop})"

    @staticmethod
    def to_int(text: str) -> int:
        high, low = unpack('!2Q', inet_pton(AF_INET6, text))
        return (high << 64) | low

    @staticmethod
    def from_text(text: str) -> "ParseIPv6":
        return ParseIPv6(ParseIPv6.to_int(text))

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseIPv6":
        return self

class ParseCIDR(ParseAtom):
    def __init__(self,
            network: int,
            prefix:  int,
            maxbits: int):

        if prefix < 0 or prefix > maxbits:
            raise ValueError(f"invalid prefix length {prefix} (min 0 max {maxbits})")

        self.prefix  = prefix
        # /8 becomes 0xFF000000
        self.mask    = ((1 << prefix) - 1) << (maxbits - prefix)
        # & here to remove any host bits
        self.integer = network & self.mask

        self._hash = hash((self.prefix, self.integer))

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseCIDR":
        return self
    def __hash__(self) -> int:
        return self._hash

class ParseCIDRv4(ParseCIDR):
    def __init__(self,
            network: int,
            prefix:  int):

        super().__init__(network, prefix, 32)

    def __repr__(self) -> str:
        bytes = pack("!L", self.integer)
        ntop  = inet_ntop(AF_INET, bytes)
        return f"CIDRv4({ntop}/{self.prefix})"

    @staticmethod
    def from_text(text: str) -> "ParseCIDRv4":
        address, cidr = text.split("/")
        return ParseCIDRv4(ParseIPv4.to_int(address), int(cidr))

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseCIDRv4":
        return self

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
        return f"CIDRv6({ntop}/{self.prefix})"

    @staticmethod
    def from_text(text: str) -> "ParseCIDRv6":
        address, cidr = text.split("/")
        return ParseCIDRv6(ParseIPv6.to_int(address), int(cidr))

    def eval(self, variables: Dict[str, ParseAtom]) -> "ParseCIDRv6":
        return self

KEYWORDS: Dict[str, Type[ParseAtom]] = {
    "true":  ParseBool,
    "false": ParseBool
}
