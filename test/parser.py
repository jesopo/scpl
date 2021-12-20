import unittest
from scpl.lexer import tokenise
from scpl.parser import operators, parse
from scpl.parser import ParseInteger, ParseFloat, ParseString

class ParserTestString(unittest.TestCase):
    def test_lone(self):
        atom = parse(tokenise('"asd"'), {})[0]
        self.assertEqual(atom.__class__, ParseString)
        self.assertEqual(atom.value, "asd")
        self.assertEqual(atom.delimiter, '"')

    def test_addstring(self):
        atom = parse(tokenise('"asd" + "asd"'), {})[0]
        self.assertEqual(atom.__class__, operators.add.ParseBinaryAddStringString)

    def test_addregex(self):
        atom = parse(tokenise('"asd" + /asd/'), {})[0]
        self.assertEqual(atom.__class__, operators.add.ParseBinaryAddStringRegex)

class ParserTestInteger(unittest.TestCase):
    def test_lone(self):
        atom = parse(tokenise("123"), {})[0]
        self.assertEqual(atom.__class__, ParseInteger)
        self.assertEqual(atom.value, 123)

    def test_addinteger(self):
        atom = parse(tokenise('1 + 1'), {})[0]
        self.assertEqual(atom.__class__, operators.add.ParseBinaryAddIntegerInteger)

class ParserTestFloat(unittest.TestCase):
    def test_lone(self):
        atom = parse(tokenise("123.0"), {})[0]
        self.assertEqual(atom.__class__, ParseFloat)
        self.assertEqual(atom.value, 123.0)

    def test_addfloat(self):
        atom = parse(tokenise('1.0 + 1.0'), {})[0]
        self.assertEqual(atom.__class__, operators.add.ParseBinaryAddFloatFloat)
