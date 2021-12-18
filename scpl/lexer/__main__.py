import sys
from typing import Deque

from .lexer  import tokenise, LexerError
from .tokens import Token

def main_lexer(line: str) -> Deque[Token]:
    try:
        tokens = tokenise(line)
    except LexerError as e:
        print(line)
        print(' '*e.index + "^")
        print(str(e))
        sys.exit(1)
    else:
        print(f"tokens  : {list(tokens)!r}")
        return tokens

if __name__ == "__main__":
    main_lexer(sys.argv[1])
