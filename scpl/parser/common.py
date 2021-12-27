from ..lexer import Token

class ParserError(Exception):
    def __init__(self, token: Token, error: str):
        self.token = token
        super().__init__(error)

class ParserErrorWithIndex(Exception):
    def __init__(self, index: int, error: str):
        self.index = index
        super().__init__(error)

class ParserTypeError(ParserError):
    def __init__(self,
            token: Token,
            error: str):
        super().__init__(token, error)
