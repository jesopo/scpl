import unittest
from scpl.lexer import LexerError, tokenise
from scpl.lexer import (TokenOperator, TokenNumber, TokenRegex, TokenSpace,
    TokenString, TokenWord)
from scpl.common import OPERATORS_BINARY, OPERATORS_UNARY

class LexerTestString(unittest.TestCase):
    def test_doublequote(self):
        token = tokenise('"asd"')[0]
        self.assertEqual(token.__class__, TokenString)
        self.assertEqual(token.text, '"asd"')

    def test_apostrophe(self):
        token = tokenise("'asd'")[0]
        self.assertEqual(token.__class__, TokenString)
        self.assertEqual(token.text, "'asd'")

    def test_curvedquote(self):
        token = tokenise("“asd”")[0]
        self.assertEqual(token.__class__, TokenString)
        self.assertEqual(token.text, "“asd”")

    def test_space(self):
        token = tokenise('"asd asd"')[0]
        self.assertEqual(token.__class__, TokenString)
        self.assertEqual(token.text, '"asd asd"')

    def test_unfinished(self):
        self.assertRaises(LexerError, lambda: tokenise("'asd"))

class LexerTestNumber(unittest.TestCase):
    def test_int(self):
        token = tokenise('123')[0]
        self.assertEqual(token.__class__, TokenNumber)
        self.assertEqual(token.text, '123')

    def test_float(self):
        token = tokenise('1.23')[0]
        self.assertEqual(token.__class__, TokenNumber)
        self.assertEqual(token.text, '1.23')

    def test_float_dotprefix(self):
        token = tokenise('.23')[0]
        self.assertEqual(token.__class__, TokenNumber)
        self.assertEqual(token.text, '.23')

    def test_unfinished(self):
        self.assertRaises(LexerError, lambda: tokenise("1."))

    def test_invalid(self):
        self.assertRaises(LexerError, lambda: tokenise("1.2.3"))
        self.assertRaises(LexerError, lambda: tokenise("1.."))
        self.assertRaises(LexerError, lambda: tokenise("1.a"))

class LexerTestOperators(unittest.TestCase):
    def test_binary(self):
        for operator in OPERATORS_BINARY:
            token = tokenise(operator)[0]
            self.assertEqual(token.__class__, TokenOperator)
            self.assertEqual(token.text, operator)

    def test_unary(self):
        for operator in OPERATORS_UNARY:
            token = tokenise(operator)[0]
            self.assertEqual(token.__class__, TokenOperator)
            self.assertEqual(token.text, operator)

class LexerTestRegex(unittest.TestCase):
    def test_not_operator(self):
        tokens = tokenise(",asd,")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, TokenRegex)
        self.assertEqual(tokens[0].text, ",asd,")

    def test_nonunary_as_unary(self):
        # should be a regex because / isn't a valid unary operator but is used
        # where we'd expect a unary operator
        tokens = tokenise("/asd/")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, TokenRegex)

    def test_binary(self):
        # shouldn't be a regex because it's a binary operator where we'd
        # expect a binary operator
        tokens = tokenise("1 /asd/")
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0].__class__, TokenNumber)
        self.assertEqual(tokens[1].__class__, TokenSpace)
        self.assertEqual(tokens[2].__class__, TokenOperator)
        self.assertEqual(tokens[3].__class__, TokenWord)
        self.assertEqual(tokens[4].__class__, TokenOperator)

    def test_unfinished(self):
        self.assertRaises(LexerError, lambda: tokenise("/asd"))
