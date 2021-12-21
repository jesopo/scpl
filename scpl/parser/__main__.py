import json, sys
from collections import deque
from time        import monotonic
from typing      import Dict, List

from .parser     import parse, ParserError
from .operands   import ParseAtom

from ..lexer          import tokenise, LexerError
from ..lexer.__main__ import main_lexer

def main_parser(line: str, types: Dict[str, type]) -> ParseAtom:
    tokens = main_lexer(line)
    start = monotonic()
    try:
        ast = parse(tokens, types)[0]
    except ParserError as e:
        print()
        print(line)
        print(" "*e.token.index + "^")
        print(f"parse error: {str(e)}")
        sys.exit(2)
    else:
        end = monotonic()
        print(f"parser  : {ast!r}")
        print(f"duration: {(end-start)*1_000_000:.2f}μs")

        #ast = ast.precompile()
        #print(f"precomp : {ast!r}")
        return ast

if __name__ == "__main__":

    vars: Dict[str, type] = {}
    if len(sys.argv) > 2:
        for key, value in json.loads(sys.argv[2]).items():
            tokens    = deque(tokenise(value))
            vars[key] = type(parse(tokens, {})[0])

    main_parser(sys.argv[1], vars)
