import string
from collections import deque
from typing import Deque, Dict, List, Sequence, Tuple

RANGES: Tuple[str, str, str] = (
    string.ascii_uppercase,
    string.ascii_lowercase,
    string.digits
)

def _find_unescaped(chars: Sequence[str], findchar: int) -> int:
    i = 0
    while chars[i]:
        char = chars[i]
        if chars[i] == "\\":
            i += 1
        elif ord(char) == findchar:
            return i
        i += 1
    return -1

class RegexLexerError(Exception):
    pass

class RegexToken:
    def __init__(self, text: str):
        self.text = text
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.text!r})"
class RegexTokenScope(RegexToken):
    pass
class RegexTokenClass(RegexToken):
    pass
class RegexTokenRepeat(RegexToken):
    pass
class RegexTokenOperator(RegexToken):
    pass
class RegexTokenOpaque(RegexToken):
    pass
class RegexTokenLiteral(RegexToken):
    pass

def tokenise_class(chars: Deque[str]) -> List[RegexToken]:
    out: List[RegexToken] = []
    if chars[0] == "^":
        out.append(RegexTokenOperator(chars.popleft()))
    if chars[0] == "]":
        out.append(RegexTokenLiteral(chars.popleft()))

    chars.append("") # end of expression
    while chars[0]:
        char = chars.popleft()
        if char == "]":
            # this means the parent scope can know we closed our class correctly
            chars.appendleft(char)
            break
        elif char.isalpha() and chars[0] == "-" and chars[0]:
            range_c = char + chars.popleft()
            for range in RANGES:
                if ((r_start := range.find(char)) > -1
                        and (r_end := range.find(chars[0])) > -1
                        and r_end >= r_start):
                    out.append(RegexTokenLiteral(range[r_start:r_end]))
                    break
            else:
                raise RegexLexerError("invalid range")
        else:
            out.append(RegexTokenLiteral(char))

    return out

def tokenise_expression(chars: Deque[str]) -> List[RegexToken]:
    out: List[RegexToken] = []

    while chars[0]:
        char = chars.popleft()
        if char == ")":
            # this means a maybe-existent parent scope can know we closed our scope successfully
            chars.appendleft(char)
            break
        elif char == "(":
            scope = char
            if chars[0] == "?":
                while chars[0] and not chars[0] == ")":
                    scope_next = chars.popleft()
                    scope += scope_next
                    if scope_next == ":":
                        break

            subexpression = tokenise_expression(chars)
            if not chars[0] == ")":
                raise RegexLexerError("no end")
            else:
                out.append(RegexTokenScope(scope))
                out.extend(subexpression)
                out.append(RegexTokenScope(chars.popleft()))
        elif char == "[":
            reclass = tokenise_class(chars)
            if not chars[0] == "]":
                raise RegexLexerError("no end")
            else:
                out.append(RegexTokenClass(char))
                out.extend(reclass)
                out.append(RegexTokenClass(chars.popleft()))
        elif char == "{":
            repeat = ""
            repeat_end = _find_unescaped(chars, ord("}"))
            if repeat_end == -1:
                raise RegexLexerError("no end")
            else:
                for i in range(repeat_end):
                    repeat += chars.popleft()
                out.append(RegexTokenRepeat(char))
                out.append(RegexTokenOpaque(repeat))
                out.append(RegexTokenRepeat(chars.popleft()))
        elif char == "\\":
            if not chars[0]:
                raise RegexLexerError("empty escape")
            else:
                out.append(RegexTokenOpaque(char + chars.popleft()))
        elif char in set("^.+*?$|"):
            out.append(RegexTokenOperator(char))
        else:
            out.append(RegexTokenLiteral(char))

    return out

def tokenise(regex: str):
    chars = deque(regex)
    chars.append("") # end of expression
    out = tokenise_expression(chars)
    if chars[0] == "":
        return out
    else:
        raise RegexLexerError("unexpected token")

if __name__ == "__main__":
    import sys
    out = tokenise(sys.argv[1])
    print(out)
