import string
from typing   import Optional
from ..common import *

CHARS_SPACE    = set(" ")
CHARS_DIGIT    = set(string.digits)
CHARS_WORD     = set(string.ascii_uppercase + string.ascii_lowercase + "_")
CHARS_HEX      = set(string.hexdigits)
OPERATORS_BOTH = set(OPERATORS_BINARY) | set(OPERATORS_UNARY)
CHARS_OPERATOR = set(op[0] for op in OPERATORS_BOTH)

DELIMS_STRING = {
    '"': '"',
    "'": "'",
    "“": "”"
}

class Token:
    def __init__(self,
            index: int,
            last:  Optional["Token"]):
        self.index    = index
        self.last     = last
        self.text     = ""
        self.complete = False
    def __repr__(self) -> str:
        name = self.__class__.__name__.replace("Token", "", 1)
        return f"{name}({self.text})"
    def push(self, next: str) -> Optional[str]:
        return None

class TokenTransparent(Token):
    pass
class TokenSpace(TokenTransparent):
    def push(self, next: str) -> Optional[str]:
        if next in CHARS_SPACE:
            self.text    += next
            self.complete = True
            return None
        else:
            return "not a space"

class TokenParenthesis(Token):
    def push(self, next: str) -> Optional[str]:
        if self.text:
            return "already finished"
        elif next in {"(", ")"}:
            self.text    += next
            self.complete = True
            return None
        else:
            return "not a parenthesis"

class TokenWord(Token):
    def push(self, next: str) -> Optional[str]:
        if (next in CHARS_WORD or
                (next in CHARS_DIGIT and len(self.text) > 0)):
            self.text    += next
            self.complete = True
            return None
        else:
            return "invalid word character"

class TokenOperator(Token):
    def push(self, next: str) -> Optional[str]:
        if self.text:
            if (op := self.text + next) in OPERATORS_BOTH:
                self.text     = op
                self.complete = True
                return None
            else:
                return "invalid operator"
        elif next in CHARS_OPERATOR:
            self.text     = next
            self.complete = next in OPERATORS_BOTH
            return None
        else:
            return "not an operator"

class TokenNumber(Token):
    def __init__(self,
            index: int,
            last:  Optional[Token]):
        super().__init__(index, last)
        self._point = False

    def push(self, next: str) -> Optional[str]:
        if next in CHARS_DIGIT:
            self.text    += next
            self.complete = True
            return None
        elif next == ".":
            self.complete = False
            if not self._point:
                self.text  += next
                self._point = True
                return None
            else:
                return "too many points"
        else:
            if next in CHARS_WORD:
                self.complete = False
            return "invalid number character"

class TokenHex(Token):
    def push(self, next: str) -> Optional[str]:
        if not self.text:
            if next == "0":
                self.text += next
                return None
            else:
                return "not a hex literal"
        elif self.text == "0":
            if next == "x":
                self.text += next
                return None
            else:
                return "not a hex literal"
        elif len(self.text) > 1:
            if next in CHARS_HEX:
                self.text += next
                self.complete = True
                return None
            else:
                if next in CHARS_WORD:
                    self.complete = False
                return "not a hex digit"
        else:
            return "not a hex literal"

class TokenString(Token):
    def __init__(self,
            index: int,
            last:  Optional[Token]):
        super().__init__(index, last)
        self._delim  = ""
        self._escape = False

    def push(self, next: str) -> Optional[str]:
        if self.complete:
            return "string already completed"
        elif self.text:
            self.text += next
            if not self._escape:
                if next == DELIMS_STRING[self._delim]:
                    self.complete = True
                elif next == "\\":
                    self._escape = True
            else:
                self._escape = False
            return None
        elif next in DELIMS_STRING:
            self._delim = next
            self.text  += next
            return None
        else:
            return "invalid string delimiter"

class TokenRegex(Token):
    def __init__(self,
            index: int,
            last:  Optional[Token]):
        super().__init__(index, last)
        self._delim  = ""
        self._escape = False

    def push(self, next: str) -> Optional[str]:
        if self.complete:
            if next in CHARS_WORD:
                self.text += next
                return None
            else:
                return "invalid flag character"
        elif self.text:
            self.text += next
            if not self._escape:
                if next == self._delim:
                    self.complete = True
                elif next == "\\":
                    self._escape = True
            else:
                self._escape = False
            return None
        elif next in CHARS_WORD | CHARS_DIGIT | CHARS_SPACE | set("\\()"):
            return "invalid regex delimiter"
        elif next in OPERATORS_UNARY:
            return "invalid regex delimiter"
        elif (next in CHARS_OPERATOR
                and self.last is not None
                and not isinstance(self.last, TokenOperator)):
            return "invalid regex delimiter"
        else:
            self.text  += next
            self._delim = next
            return None

class TokenIPv4(Token):
    def __init__(self,
            index: int,
            last:  Optional[Token]):
        super().__init__(index, last)
        self._octet  = ""
        self._octets = 0
        self._cidr   = False

    def push(self, next: str) -> Optional[str]:
        if next == ".":
            if self._octets == 3:
                return "too many octets"
            elif not self._octet:
                return "empty octet"
            else:
                self.text    += next
                self._octets += 1
                self._octet   = ""
                self.complete = False
                return None
        elif next == "/":
            if self._cidr:
                return "excess cidr delimiter"
            elif not self.complete:
                return "invalid position for cidr delimiter"
            else:
                self.complete = False
                self.text += next
                self._cidr = True
                return None
        elif next in CHARS_DIGIT:
            self._octet += next
            if self._cidr:
                self.text += next
                self.complete = True
                return None
            elif 0 <= int(self._octet) <= 255:
                self.text    += next
                self.complete = self._octets == 3
                return None
            else:
                self.complete = False
                return "octet must be between 0 and 255"
        else:
            return "invalid IPv4 character"

class TokenIPv6(Token):
    def __init__(self,
            index: int,
            last:  Optional[Token]):
        super().__init__(index, last)
        self._trunc   = False
        self._hextet  = ""
        self._hextets = 0
        self._cidr    = False

    def push(self, next: str) -> Optional[str]:
        if next == ":":
            if not self.text:
                self.text += next
                return None
            elif self._hextets == 7:
                return "too many hextets"
            elif self.text[-1] == ":":
                if self._trunc:
                    self.complete = False
                    return "double truncation"
                elif self._hextets == 6:
                    self.complete = False
                    return "insufficient truncation"
                else:
                    self.text     += next
                    self._trunc    = True
                    self._hextets += 2
                    self.complete  = True
                    return None
            else:
                self.text     += next
                self._hextet   = ""
                self._hextets += 1
                if not self.complete:
                    self.complete = self._hextets == 7
                return None
        elif next == "/":
            if self._cidr:
                return "excess cidr delimiter"
            elif not self.complete:
                return "invalid position for cidr delimiter"
            else:
                self.complete = False
                self.text += next
                self._cidr = True
                return None
        elif self._cidr:
            if next in CHARS_DIGIT:
                self.text += next
                self.complete = True
                return None
            else:
                return "invalid cidr character"
        elif next in CHARS_HEX:
            self._hextet += next
            if 0 <= int(self._hextet, 16) <= 0xffff:
                self.text += next
                return None
            else:
                self.complete = False
                return "hextet must be between 0 and ffff"
        else:
            if next in CHARS_WORD:
                self.complete = False
            return "invalid IPv6 character"

class TokenDuration(Token):
    def __init__(self,
            index: int,
            last:  Optional[Token]):
        super().__init__(index, last)
        self._on_unit = False

    def push(self, next: str) -> Optional[str]:
        if next.isdigit():
            self._on_unit = False;
            self.complete = False
            self.text += next
            return None
        elif not self.text:
            return "not a duration string"
        elif next in CHARS_WORD:
            if next in set("wdhms"):
                if self._on_unit:
                    self.complete = False
                    return "consecutive unit chars"
                else:
                    self._on_unit = True;
                    self.text += next
                    self.complete = True
                    return None
            else:
                self.complete = False
                return "invalid unit character"
        else:
            return "invalid duration chracter"
