import sys, traceback
from collections import deque
from time        import monotonic
from typing      import Dict

from ..lexer           import tokenise
from ..parser          import parse, ParseAtom
from ..parser.__main__ import main_parser

def main_eval(
        line: str,
        vars: Dict[str, str]
        ):

    var_atoms: Dict[str, ParseAtom] = {}
    for key, value in vars.items():
        var_tokens     = deque(tokenise(value))
        var_atoms[key] = parse(var_tokens, {})[0]

    ast   = main_parser(line, {k: type(v) for k, v in var_atoms.items()})
    start = monotonic()
    try:
        out = ast.eval(var_atoms)
    except Exception as e:
        print(f"eval error: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
    else:
        end = monotonic()
        print(f"vars    : {var_atoms!r}")
        print(f"eval    : {out!r}")
        print(f"duration: {(end-start)*1_000_000:.2f}μs")

if __name__ == "__main__":
    vars: Dict[str, str] = {}
    if sys.argv[2:]:
        import json
        vars = json.loads(sys.argv[2])

    main_eval(sys.argv[1], vars)
