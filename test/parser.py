import unittest
from ipaddress import ip_address

from scpl.lexer import tokenise
from scpl.parser import operators, parse
from scpl.parser import ParseInteger, ParseIPv4, ParseIPv6, ParseFloat, ParseString

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

class ParserTestIPv4(unittest.TestCase):
    def test_lone(self):
        addr = "10.84.1.1"
        atom = parse(tokenise(addr), {})[0]
        self.assertIsInstance(atom, ParseIPv4)
        self.assertEqual(atom.integer, int(ip_address(addr)))

class ParserTestIPv6(unittest.TestCase):
    def test_lone(self):
        addr = "fd84:9d71:8b8:1::1"
        atom = parse(tokenise(addr), {})[0]
        self.assertIsInstance(atom, ParseIPv6)
        self.assertEqual(atom.integer, int(ip_address(addr)))
