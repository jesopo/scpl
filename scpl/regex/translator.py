from typing import Dict, Sequence
from .lexer import (tokenise, RegexToken, RegexTokenClass, RegexTokenLiteral,
    RegexTokenOpaque, RegexTokenRange)
from .ranges import get_range

def translate(tokens: Sequence[RegexToken], table: Dict[int, str]):
    out = list(tokens)
    in_class = False

    for i, token in enumerate(out):
        if isinstance(token, RegexTokenClass):
            in_class = token.text == "["
        elif isinstance(token, RegexTokenRange):
            range_c = get_range(ord(token.text[0]), ord(token.text[2]))
            if not (range_t := range_c.translate(table)) == range_c:
                # /[a-c]/ becomes /[abc]/ and if 'a' is translated in to 'b' we end up
                # with /[bbc]/ so the set stuff is to remove duplicates
                range_s = "".join(sorted(set(range_t)))
                out[i] = RegexTokenOpaque(range_s)
        elif isinstance(token, RegexTokenLiteral):
            literal = ""
            for char in token.text:
                if (char_ord := ord(char)) in table:
                    piece = table[char_ord]

                    if in_class or len(piece) == 1:
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

