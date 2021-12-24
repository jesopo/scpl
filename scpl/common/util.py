from typing import Iterator, Optional, Sequence

def find_unescaped(
        s: str,
        c: str
        ) -> Iterator[int]:

    i = 0

    while i < len(s):
        c2 = s[i]
        if c2 == "\\":
            i += 1
        elif c2 == c:
            yield i
        i += 1

def find_unused_delimiter(
        s:     str,
        chars: Sequence[str]
        ) -> Optional[str]:

    for char in chars:
        try:
            next(find_unescaped(s, char))
        except StopIteration:
            return char
    else:
        return None

def with_delimiter(
        s:     str,
        chars: Sequence[str]
        ) -> str:

    if unused_delim := find_unused_delimiter(s, chars):
        delim = unused_delim
    else:
        delim  = chars[0]
        found  = find_unescaped(s, delim)
        rdelim = f"\\{delim}"
        for index in reversed(list(found)):
            s = s[:index] + rdelim + s[index+1:]

    return f"{delim}{s}{delim}"
