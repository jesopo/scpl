import unittest
from scpl.lexer import tokenise
from scpl.parser import parse
from scpl.parser import ParseInteger, ParseFloat, ParseRegex, ParseString

class ParserTestString(unittest.TestCase):
    def test_addstring(self):
        atom = parse(tokenise('"asd" + "asd"'), {})[0].eval({})
        self.assertIsInstance(atom, ParseString)
        self.assertEqual(atom.value, "asdasd")
        self.assertEqual(atom.delimiter, '"')

    def test_addregex(self):
        atom = parse(tokenise('"asd." + /asd/i'), {})[0].eval({})
        self.assertIsInstance(atom, ParseRegex)
        self.assertEqual(atom.pattern, "asd\.(?i:asd)")
        self.assertEqual(atom.delimiter, None)
        self.assertEqual(atom.flags, set())
