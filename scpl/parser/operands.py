import re
from collections import deque, OrderedDict
from dataclasses import dataclass
from socket      import inet_ntop, inet_pton, AF_INET, AF_INET6
from struct      import pack, unpack
from typing      import Any, Deque, Dict, List, Optional, Pattern, Set, Tuple, Type
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

    def is_constant(self) -> bool:
        return True

class ParseBool(ParseAtom):
    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        raise NotImplementedError()
class ParseConstBool(ParseBool):
    def __init__(self, value: bool):
        self.value = value
    def __repr__(self) -> str:
        tostr = {True: "true", False: "false"}[self.value]
        return f"Bool({tostr})"

    @staticmethod
    def from_text(text: str) -> "ParseBool":
        return ParseConstBool({"true": True, "false": False}[text])

    def eval(self, vars: Dict[str, ParseAtom]) -> bool:
        return self.value

class ParseInteger(ParseAtom):
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        raise NotImplementedError()
class ParseConstInteger(ParseInteger):
    def __init__(self, value: int):
        self.value = value
    def __repr__(self) -> str:
        return f"Integer({self.value})"
    def __hash__(self) -> int:
        return hash(self.value)

    @staticmethod
    def from_text(text: str) -> "ParseInteger":
        return ParseConstInteger(int(text))

    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return self.value

# sneaky little trick. convert hex to integer
class ParseHex(ParseInteger):
    @staticmethod
    def from_text(text: str) -> ParseInteger:
        return ParseConstInteger(int(text[2:], 16))

DURATION_UNITS: TOrderedDict[str, int] = OrderedDict(reversed([
    ("s", 1),
    ("m", SECONDS_M := 60),
    ("h", SECONDS_H := SECONDS_M * 60),
    ("d", SECONDS_D := SECONDS_H * 24),
    ("w", SECONDS_W := SECONDS_D * 7)
]))
RE_DURATION = re.compile("^(\d+w)?(\d+d)?(\d+h)?(\d+m)?(\d+s)?$")

class ParseDuration(ParseInteger):
    @staticmethod
    def from_text(text: str) -> "ParseInteger":
        seconds = 0
        if (match := RE_DURATION.search(text)) is not None:
            for group in match.groups():
                if group is not None:
                    value_s, unit = group[:-1], group[-1]
                    scale = DURATION_UNITS[unit]
                    seconds += int(value_s) * scale

        return ParseConstInteger(seconds)

class ParseFloat(ParseAtom):
    def eval(self, vars: Dict[str, ParseAtom]) -> float:
        raise NotImplementedError()
class ParseConstFloat(ParseFloat):
    def __init__(self, value: float):
        self.value = value
    def __repr__(self) -> str:
        return f"Float({self.value})"
    def __hash__(self) -> int:
        return hash(self.value)

    @staticmethod
    def from_text(text: str) -> "ParseFloat":
        return ParseConstFloat(float(text))

    def eval(self, vars: Dict[str, ParseAtom]) -> float:
        return self.value

class ParseString(ParseAtom):
    def __init__(self, casemap: Optional[Dict[int, str]] = None):
        self.casemap = casemap
    def eval(self, vars: Dict[str, ParseAtom]) -> str:
        raise NotImplementedError()
class ParseConstString(ParseString):
    def __init__(self, delim: Optional[str], value: str):
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
        return ParseConstString(text[0], text[1:-1])

    def eval(self, vars: Dict[str, ParseAtom]) -> str:
        return self.value

class ParseRegex(ParseAtom):
    def eval(self, vars: Dict[str, ParseAtom]) -> Pattern:
        raise NotImplementedError()
class ParseConstRegex(ParseRegex):
    def __init__(self,
            delimiter: Optional[str],
            pattern: str,
            flags: Set[str]):

        self.delimiter = delimiter
        self.pattern = pattern
        self.flags = flags

    def __str__(self) -> str:
        if self.delimiter is not None:
            regex = f"{self.delimiter}{self.pattern}{self.delimiter}"
        else:
            regex = with_delimiter(self.pattern, REGEX_DELIMS)
        flags = ''.join(self.flags)
        return f"{regex}{flags}"

    def __repr__(self) -> str:
        return f"Regex({str(self)})"
    def __hash__(self) -> int:
        return hash((self.pattern, self.flags))

    @staticmethod
    def from_text(text: str) -> "ParseRegex":
        delim, r = text[0], text[1:]
        r, flags = r.rsplit(delim, 1)

        return ParseConstRegex(delim, r, set(flags))

    def eval(self, vars: Dict[str, ParseAtom]) -> Pattern:
        flags = 0
        if "i" in self.flags:
            flags |= re.I
        return re.compile(self.pattern, flags)

class ParseIP(ParseAtom):
    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        raise NotImplementedError()
class ParseConstIP(ParseIP):
    def __init__(self, ip: int):
        self.integer = ip
    def __hash__(self) -> int:
        return hash(self.integer)

    def eval(self, vars: Dict[str, ParseAtom]) -> int:
        return self.integer

class ParseIPv4(ParseIP):
    pass
class ParseConstIPv4(ParseIPv4, ParseConstIP):
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
        return ParseConstIPv4(ParseConstIPv4.to_int(text))

class ParseIPv6(ParseIP):
    pass
class ParseConstIPv6(ParseIPv6, ParseConstIP):
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
        return ParseConstIPv6(ParseConstIPv6.to_int(text))

class ParseCIDR(ParseAtom):
    def eval(self, vars: Dict[str, ParseAtom]) -> Tuple[int, int]:
        raise NotImplementedError()
class ParseConstCIDR(ParseCIDR):
    def __init__(self, integer: int, prefix: int, maxbits: int):
        if prefix < 0 or prefix > maxbits:
            raise ValueError(f"invalid prefix length {prefix} (min 0 max {maxbits})")

        self.prefix  = prefix
        # /8 becomes 0xFF000000
        self.mask    = ((1 << prefix) - 1) << (maxbits - prefix)
        # & here to remove any host bits
        self.integer = integer & self.mask

        self._hash = hash((self.prefix, self.integer))

    def __hash__(self) -> int:
        return self._hash

    def eval(self, vars: Dict[str, ParseAtom]) -> Tuple[int, int]:
        return (self.integer, self.mask)

class ParseCIDRv4(ParseCIDR):
    pass
class ParseConstCIDRv4(ParseCIDRv4, ParseConstCIDR):
    def __init__(self, network: int, prefix: int):
        super().__init__(network, prefix, 32)

    def __repr__(self) -> str:
        bytes = pack("!L", self.integer)
        ntop  = inet_ntop(AF_INET, bytes)
        return f"CIDRv4({ntop}/{self.prefix})"

    @staticmethod
    def from_text(text: str) -> "ParseCIDRv4":
        address, cidr = text.split("/")
        return ParseConstCIDRv4(ParseConstIPv4.to_int(address), int(cidr))

class ParseCIDRv6(ParseCIDR):
    pass
class ParseConstCIDRv6(ParseCIDRv6, ParseConstCIDR):
    def __init__(self, network: int, prefix: int):
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
        return ParseConstCIDRv6(ParseConstIPv6.to_int(address), int(cidr))

KEYWORDS: Dict[str, ParseAtom] = {
    "true":  ParseConstBool(True),
    "false": ParseConstBool(False)
}
