import sys
from time   import monotonic
from typing import Deque

from .lexer  import tokenise, LexerError
from .tokens import Token

def main_lexer(line: str) -> Deque[Token]:
    start = monotonic()
    try:
        tokens = tokenise(line)
    except LexerError as e:
        print(line)
        print(' '*e.index + "^")
        print(str(e))
        sys.exit(1)
    else:
        end = monotonic()
        print(f"lexer   : {list(tokens)!r}")
        print(f"duration: {(end-start)*1_000_000:.2f}μs")
        return tokens

if __name__ == "__main__":
    main_lexer(sys.argv[1])
