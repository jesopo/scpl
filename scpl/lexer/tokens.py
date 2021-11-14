import string
from typing   import Optional
from ..common import *

CHARS_SPACE    = set(" ")
CHARS_DIGIT    = set(string.digits)
CHARS_WORD     = set(string.ascii_uppercase + string.ascii_lowercase + "_")
CHARS_HEX      = set(string.hexdigits)
OPERATORS_BOTH = set(OPERATORS_BINARY) | set(OPERATORS_UNARY)
CHARS_OPERATOR = set(op[0] for op in OPERATORS_BOTH)

class Token:
    def __init__(self,
            index: int,
            last:  Optional["Token"]):
        self.index    = index
        self.last     = last
        self.text     = ""
        self.complete = False
    def __repr__(self) -> str:
        name = self.__class__.__name__.removeprefix("Token")
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
        else:
            return "not a space"

class TokenParenthesis(Token):
    def push(self, next: str) -> Optional[str]:
        if self.text:
            return "already finished"
        elif next in {"(", ")"}:
            self.text    += next
            self.complete = True
        else:
            return "not a parenthesis"

class TokenWord(Token):
    def push(self, next: str) -> Optional[str]:
        if (next in CHARS_WORD or
                (next in CHARS_DIGIT and len(self.text) > 0)):
            self.text    += next
            self.complete = True
        else:
            return "invalid word character"

class TokenOperator(Token):
    def push(self, next: str) -> Optional[str]:
        if self.text:
            if (op := self.text + next) in OPERATORS_BOTH:
                self.text     = op
                self.complete = True
            else:
                return "invalid operator"
        elif next in CHARS_OPERATOR:
            self.text     = next
            self.complete = next in OPERATORS_BOTH
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
        elif next == ".":
            self.complete = False
            if not self._point:
                self.text  += next
                self._point = True
            else:
                return "too many points"
        else:
            if next in CHARS_WORD:
                self.complete = False
            return "invalid number character"

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
                if next == self._delim:
                    self.complete = True
                elif next == "\\":
                    self._escape = True
            else:
                self._escape = False
        elif next in {'"', "'"}:
            self._delim = next
            self.text  += next
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

class TokenIPv4(Token):
    def __init__(self,
            index: int,
            last:  Optional[Token]):
        super().__init__(index, last)
        self._octet  = ""
        self._octets = 0

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
        elif next in CHARS_DIGIT:
            self._octet += next
            if 0 <= int(self._octet) <= 255:
                self.text    += next
                self.complete = self._octets == 3
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

    def push(self, next: str) -> Optional[str]:
        if next == ":":
            if not self.text:
                self.text += next
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
            else:
                self.text     += next
                self._hextet   = ""
                self._hextets += 1
                if not self.complete:
                    self.complete = self._hextets == 7
        elif next in CHARS_HEX:
            self._hextet += next
            if 0 <= int(self._hextet, 16) <= 0xffff:
                self.text += next
            else:
                return "hextet must be between 0 and ffff"
        else:
            return "invalid IPv6 character"
