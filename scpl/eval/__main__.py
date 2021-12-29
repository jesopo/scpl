import json, sys, traceback
from collections import deque
from time        import monotonic
from typing      import Dict

from ..lexer import tokenise
from ..parser import parse
from ..parser.operands import ParseAtom
from ..parser.operators.common import ParseOperator
from ..parser.__main__ import main_parser

def main_eval(line: str, vars: Dict[str, ParseAtom]):
    ast = main_parser(line, vars)
    if not isinstance(ast, ParseOperator):
        print(f"nothing to do")
        sys.exit(1)

    start = monotonic()
    try:
        out = ast.eval(vars)
    except Exception as e:
        print(f"eval error: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
    else:
        end = monotonic()
        print(f"vars    : {vars!r}")
        print(f"eval    : {out!r}")
        print(f"duration: {(end-start)*1_000_000:.2f}μs")

if __name__ == "__main__":
    vars: Dict[str, ParseAtom] = {}
    if len(sys.argv) > 2:
        import json
        for key, value in json.loads(sys.argv[2]).items():
            tokens = deque(tokenise(value))
            atoms, deps = parse(tokens, {})
            vars[key] = atoms[0]

    main_eval(sys.argv[1], vars)
