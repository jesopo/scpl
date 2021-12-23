import sys
from time   import monotonic
from typing import Deque

from .lexer  import tokenise, LexerError, LexerUnfinishedError
from .tokens import Token

def main_lexer(line: str) -> Deque[Token]:
    start = monotonic()
    try:
        tokens = tokenise(line)
    except LexerUnfinishedError as e1:
        print(line)
        print(' '*e1.index + "^"*len(e1.token.text))
        print(str(e1))
        sys.exit(1)
    except LexerError as e2:
        print(line)
        print(' '*e2.index + "^")
        print(str(e2))
        sys.exit(2)
    else:
        end = monotonic()
        print(f"lexer   : {list(tokens)!r}")
        print(f"duration: {(end-start)*1_000_000:.2f}μs")
        return tokens

if __name__ == "__main__":
    main_lexer(sys.argv[1])
