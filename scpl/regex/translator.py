from typing import Dict, Sequence
from .lexer import (tokenise, RegexToken, RegexTokenClass, RegexTokenOpaque,
    RegexTokenLiteral)

def translate(tokens: Sequence[RegexToken], table: Dict[int, str]):
    out = list(tokens)
    in_class = False

    for i, token in enumerate(out):
        if isinstance(token, RegexTokenClass):
            in_class = token.text == "["
        elif isinstance(token, RegexTokenLiteral):
            literal = ""
            for char in token.text:
                if (char_ord := ord(char)) in table:
                    piece = f"{char}{table[char_ord]}"
                else:
                    piece = char

                if in_class:
                    literal += piece
                else:
                    literal += f"[{piece}]"
            out[i] = RegexTokenOpaque(literal)
    return out

if __name__ == "__main__":
    import json, sys
    tokens = tokenise(sys.argv[1])
    table = str.maketrans(json.loads(sys.argv[2]))
    out = translate(tokens, table)
    print("".join(t.text for t in out))

