from collections import deque
from typing      import Deque, List, Optional, Tuple

from ..common    import *
from .tokens     import *

class LexerError(Exception):
    def __init__(self,
            index: int,
            error: str):
        self.index = index
        super().__init__(error)
class LexerUnfinishedError(LexerError):
    def __init__(self, index: int):
        super().__init__(index, "unfinished token")

def tokenise(expression: str) -> Deque[Token]:
    char_stream       = deque(expression)
    # empty string used to force all tokens to invalidate/finish at the end of
    # the expression
    char_stream.append("")
    # +1 to account for the above empty string
    expression_length = len(expression)+1

    tokens_finished:   Deque[Token] = deque()
    tokens_unfinished: List[Token] = []
    tokens_broken:     List[Tuple[Token, str]] = []

    token_text = ""
    token_last: Optional[Token] = None

    while char_stream:
        char_index = expression_length - len(char_stream)

        if not tokens_unfinished:
            token_text = ""
            tokens_broken     = []
            tokens_unfinished = [
                TokenRegex(char_index, token_last),
                TokenString(char_index, token_last),
                TokenIPv4(char_index, token_last),
                TokenIPv6(char_index, token_last),
                TokenParenthesis(char_index, token_last),
                TokenWord(char_index, token_last),
                TokenOperator(char_index, token_last),
                TokenSpace(char_index, token_last),
                TokenNumber(char_index, token_last),
            ]

        token_text += char_stream[0]
        for token in list(tokens_unfinished):
            was_complete = token.complete
            error        = token.push(char_stream[0])

            if error is not None or not char_stream[0]:
                tokens_unfinished.remove(token)
                if was_complete and not token.complete:
                    tokens_broken.append((token, error))

                if len(tokens_unfinished) == 0:
                    # no more valid tokens left
                    if token.complete:
                        # the current character failed to be added to the
                        # current token, but it didn't invalidate the token
                        tokens_finished.append(token)
                        if not isinstance(token, TokenTransparent):
                            token_last = token
                    elif tokens_broken:
                        btoken, berror = tokens_broken[0]
                        btoken_index   = btoken.index + len(btoken.text)
                        raise LexerError(btoken_index, berror)
                    elif token_text:
                        raise LexerUnfinishedError(token.index)
                    elif char_stream[0]:
                        # unrecognised single character
                        raise LexerError(char_index, "unknown token")
                    else:
                        # we've reached "" (end of expression)
                        char_stream.popleft()
        else:
            if tokens_unfinished:
                char_stream.popleft()

    return tokens_finished
