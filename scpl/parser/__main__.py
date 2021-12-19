import sys
from collections import deque
from typing      import Dict, List

from .parser     import parse, ParserError
from .operands   import ParseAtom

from ..lexer          import tokenise, LexerError
from ..lexer.__main__ import main_lexer

def main_parser(line: str, types: Dict[str, type]) -> ParseAtom:
    tokens = main_lexer(line)
    try:
        ast = parse(tokens, types)[0]
    except ParserError as e:
        print()
        print(line)
        print(" "*e.token.index + "^")
        print(f"parse error: {str(e)}")
        sys.exit(2)
    else:
        print(f"ast     : {ast!r}")
        print(f"constant: {ast.is_constant()!r}")

        ast = ast.precompile()
        print(f"precomp : {ast!r}")
        return ast

if __name__ == "__main__":
    main_parser(sys.argv[1], {})
