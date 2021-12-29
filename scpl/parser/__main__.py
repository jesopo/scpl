import json, sys
from collections import deque
from time        import monotonic
from typing      import Dict, List

from .parser     import parse, ParserError
from .operands   import ParseAtom

from ..lexer          import tokenise, LexerError
from ..lexer.__main__ import main_lexer

def main_parser(line: str, vars: Dict[str, ParseAtom]) -> ParseAtom:
    tokens = main_lexer(line)
    start = monotonic()
    try:
        ast, deps = parse(tokens, vars)
    except ParserError as e:
        print()
        print(line)
        print(" "*e.token.index + "^")
        print(f"parse error: {str(e)}")
        sys.exit(2)
    else:
        end = monotonic()
        print(f"parser  : {ast!r}")
        print(f"deps    : {sorted(deps)}")
        print(f"duration: {(end-start)*1_000_000:.2f}μs")

        #ast = ast.precompile()
        #print(f"precomp : {ast!r}")
        return ast[0]

if __name__ == "__main__":
    vars: Dict[str, ParseAtom] = {}
    if len(sys.argv) > 2:
        for key, value in json.loads(sys.argv[2]).items():
            tokens = deque(tokenise(value))
            atoms, deps = parse(tokens, {})
            vars[key] = atoms[0]

    main_parser(sys.argv[1], vars)
