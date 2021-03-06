import string
from collections import deque
from typing import Deque, Dict, List, Sequence, Tuple
from .ranges import RANGE_CHARS

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
    def __init__(self, index: int, error: str):
        super().__init__(error)
        self.index = index

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
class RegexTokenRange(RegexToken):
    pass

def tokenise_class(chars: Deque[str], offset: int) -> List[RegexToken]:
    startlen = len(chars)

    out: List[RegexToken] = []
    if chars[0] == "]":
        out.append(RegexTokenLiteral(chars.popleft()))

    chars.append("") # end of expression
    while chars[0]:
        index = offset + (startlen - len(chars))
        char = chars.popleft()
        if char == "]":
            # this means the parent scope can know we closed our class correctly
            chars.appendleft(char)
            break
        elif ((r_start := ord(char)) in RANGE_CHARS
                and chars[0] == "-" and chars[0]):
            range_c = char + chars.popleft()
            if (r_start in RANGE_CHARS
                    and (r_end := ord(chars[0])) in RANGE_CHARS
                    and RANGE_CHARS[r_start] == RANGE_CHARS[r_end]):
                out.append(RegexTokenRange(range_c + chars.popleft()))
            else:
                raise RegexLexerError(1, "invalid range")
        elif char == "\\":
            if not chars[0]:
                raise RegexLexerError(index, "empty escape")
            else:
                out.append(RegexTokenOpaque(char + chars.popleft()))
        else:
            out.append(RegexTokenLiteral(char))

    return out

def tokenise_expression(chars: Deque[str], offset: int) -> List[RegexToken]:
    startlen = len(chars)
    out: List[RegexToken] = []

    while chars[0]:
        index = offset + (startlen - len(chars))
        char = chars.popleft()
        if char == ")":
            # this means a maybe-existent parent scope can know we closed our scope successfully
            chars.appendleft(char)
            break
        elif char == "(":
            group_start = char
            if chars[0] == "?":
                while chars[0] and not chars[0] == ")":
                    group_next = chars.popleft()
                    group_start += group_next
                    if group_next == ":":
                        break

            group_tokens = tokenise_expression(chars, index+1)
            if not chars[0] == ")":
                raise RegexLexerError(index, "unterminated group")
            else:
                out.append(RegexTokenScope(group_start))
                out.extend(group_tokens)
                out.append(RegexTokenScope(chars.popleft()))
        elif char == "[":
            class_start = char
            if chars[0] == "^":
                class_start += chars.popleft()

            class_tokens = tokenise_class(chars, index+1)
            if not chars[0] == "]":
                raise RegexLexerError(index, "unterminated class")
            else:
                out.append(RegexTokenClass(class_start))
                out.extend(class_tokens)
                out.append(RegexTokenClass(chars.popleft()))
        elif char == "{":
            repeat = ""
            repeat_end = _find_unescaped(chars, ord("}"))
            if repeat_end == -1:
                raise RegexLexerError(index, "unterminated range")
            else:
                for i in range(repeat_end):
                    repeat += chars.popleft()
                out.append(RegexTokenRepeat(char))
                out.append(RegexTokenOpaque(repeat))
                out.append(RegexTokenRepeat(chars.popleft()))
        elif char == "\\":
            if not chars[0]:
                raise RegexLexerError(index, "empty escape")
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
    out = tokenise_expression(chars, 0)
    if chars[0] == "":
        return out
    else:
        raise RegexLexerError(len(regex)-len(chars)+1, "unexpected token")

if __name__ == "__main__":
    import sys
    regex = sys.argv[1]
    try:
        out = tokenise(regex)
    except RegexLexerError as e:
        print(regex)
        print(" "*e.index + "^")
        print()
        print(str(e))
        sys.exit(1)
    else:
        print(out)
