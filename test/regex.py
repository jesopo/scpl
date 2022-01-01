import re, unittest
from ipaddress import ip_network

from scpl.regex import lexer

class RegexTestLexer(unittest.TestCase):
    def test_literal(self):
        tokens = lexer.tokenise("abc")
        self.assertEqual(len(tokens), 3)
        self.assertIsInstance(tokens[0], lexer.RegexTokenLiteral)
        self.assertEqual(tokens[0].text, "a")
        self.assertIsInstance(tokens[1], lexer.RegexTokenLiteral)
        self.assertEqual(tokens[1].text, "b")
        self.assertIsInstance(tokens[2], lexer.RegexTokenLiteral)
        self.assertEqual(tokens[2].text, "c")

    def test_repeats(self):
        tokens = lexer.tokenise("a+a*")
        self.assertEqual(len(tokens), 4)
        self.assertIsInstance(tokens[0], lexer.RegexTokenLiteral)
        self.assertEqual(tokens[0].text, "a")
        self.assertIsInstance(tokens[1], lexer.RegexTokenOperator)
        self.assertEqual(tokens[1].text, "+")
        self.assertIsInstance(tokens[2], lexer.RegexTokenLiteral)
        self.assertEqual(tokens[2].text, "a")
        self.assertIsInstance(tokens[3], lexer.RegexTokenOperator)
        self.assertEqual(tokens[3].text, "*")

    def test_group(self):
        tokens = lexer.tokenise("(a)")
        self.assertEqual(len(tokens), 3)
        self.assertIsInstance(tokens[0], lexer.RegexTokenScope)
        self.assertEqual(tokens[0].text, "(")
        self.assertIsInstance(tokens[1], lexer.RegexTokenLiteral)
        self.assertEqual(tokens[1].text, "a")
        self.assertIsInstance(tokens[2], lexer.RegexTokenScope)
        self.assertEqual(tokens[2].text, ")")

    def test_group_nested(self):
        tokens = lexer.tokenise("((a))")
        self.assertEqual(len(tokens), 5)
        self.assertIsInstance(tokens[0], lexer.RegexTokenScope)
        self.assertEqual(tokens[0].text, "(")
        self.assertIsInstance(tokens[1], lexer.RegexTokenScope)
        self.assertEqual(tokens[1].text, "(")
        self.assertIsInstance(tokens[2], lexer.RegexTokenLiteral)
        self.assertEqual(tokens[2].text, "a")
        self.assertIsInstance(tokens[3], lexer.RegexTokenScope)
        self.assertEqual(tokens[3].text, ")")
        self.assertIsInstance(tokens[4], lexer.RegexTokenScope)
        self.assertEqual(tokens[4].text, ")")

    def test_group_flags(self):
        tokens = lexer.tokenise("(?i:a)")
        self.assertEqual(len(tokens), 3)
        self.assertIsInstance(tokens[0], lexer.RegexTokenScope)
        self.assertEqual(tokens[0].text, "(?i:")
        self.assertIsInstance(tokens[1], lexer.RegexTokenLiteral)
        self.assertEqual(tokens[1].text, "a")
        self.assertIsInstance(tokens[2], lexer.RegexTokenScope)
        self.assertEqual(tokens[2].text, ")")
