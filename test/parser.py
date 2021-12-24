import unittest
from re        import compile as re_compile
from ipaddress import ip_address

from scpl.lexer import tokenise
from scpl.parser import operators, parse
from scpl.parser import (ParseInteger, ParseIPv4, ParseIPv6, ParseFloat, ParseRegex,
    ParseString)

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

    def test_not(self):
        atom = parse(tokenise("!'a'"), {})[0]
        self.assertIsInstance(atom, operators.bools.ParseUnaryNot)

class ParseTestRegex(unittest.TestCase):
    def test_lone(self):
        atom = parse(tokenise("/a/"), {})[0]
        self.assertIsInstance(atom, ParseRegex)
        self.assertEqual(atom.pattern, "a")
        self.assertEqual(atom.delimiter, "/")
        self.assertEqual(atom.compiled, re_compile("a"))
        self.assertEqual(atom.flags, set())

    def test_addregex(self):
        atom = parse(tokenise('/asd/ + /asd/'), {})[0]
        self.assertIsInstance(atom, operators.add.ParseBinaryAddRegexRegex)

    def test_addstring(self):
        atom = parse(tokenise('/asd/ + "asd"'), {})[0]
        self.assertIsInstance(atom, operators.add.ParseBinaryAddRegexString)

    def test_not(self):
        atom = parse(tokenise("!/a/"), {})[0]
        self.assertIsInstance(atom, operators.bools.ParseUnaryNot)

class ParseTestRegexset(unittest.TestCase):
    def test_complement(self):
        atom = parse(tokenise("~/a/"), {})[0]
        self.assertIsInstance(atom, operators.complement.ParseUnaryComplementRegex)

class ParserTestInteger(unittest.TestCase):
    def test_lone(self):
        atom = parse(tokenise("123"), {})[0]
        self.assertEqual(atom.__class__, ParseInteger)
        self.assertEqual(atom.value, 123)

    def test_addinteger(self):
        atom = parse(tokenise("1 + 1"), {})[0]
        self.assertEqual(atom.__class__, operators.add.ParseBinaryAddIntegerInteger)
    def test_addinteger_negative(self):
        atom = parse(tokenise("1 + -1"), {})[0]
        self.assertEqual(atom.__class__, operators.add.ParseBinaryAddIntegerInteger)

    def test_addfloat(self):
        atom = parse(tokenise("1 + 1.0"), {})[0]
        self.assertEqual(atom.__class__, operators.add.ParseBinaryAddIntegerFloat)
    def test_addfloat_negative(self):
        atom = parse(tokenise("1 + -1.0"), {})[0]
        self.assertEqual(atom.__class__, operators.add.ParseBinaryAddIntegerFloat)

    def test_negative(self):
        atom = parse(tokenise("-1"), {})[0]
        self.assertIsInstance(atom, operators.negative.ParseUnaryNegativeInteger)

    def test_complement(self):
        atom = parse(tokenise("~1"), {})[0]
        self.assertIsInstance(atom, operators.complement.ParseUnaryComplementInteger)

    def test_not(self):
        atom = parse(tokenise("!1"), {})[0]
        self.assertIsInstance(atom, operators.bools.ParseUnaryNot)

class ParserTestFloat(unittest.TestCase):
    def test_lone(self):
        atom = parse(tokenise("123.0"), {})[0]
        self.assertEqual(atom.__class__, ParseFloat)
        self.assertEqual(atom.value, 123.0)

    def test_addfloat(self):
        atom = parse(tokenise("1.0 + 1.0"), {})[0]
        self.assertEqual(atom.__class__, operators.add.ParseBinaryAddFloatFloat)

    def test_addinteger(self):
        atom = parse(tokenise("1.0 + 1"), {})[0]
        self.assertEqual(atom.__class__, operators.add.ParseBinaryAddFloatInteger)

    def test_negative(self):
        atom = parse(tokenise("-1.0"), {})[0]
        self.assertIsInstance(atom, operators.negative.ParseUnaryNegativeFloat)

    def test_not(self):
        atom = parse(tokenise("!1.0"), {})[0]
        self.assertIsInstance(atom, operators.bools.ParseUnaryNot)

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

class ParserTestBinaryOperator(unittest.TestCase):
    def test_precedence_0(self):
        atom = parse(tokenise("1 && 1 || 1"), {})[0]
        self.assertIsInstance(atom, operators.bools.ParseBinaryEither)

    def test_precedence_1(self):
        atom = parse(tokenise("true == true && true"), {})[0]
        self.assertIsInstance(atom, operators.bools.ParseBinaryBoth)

    def test_precedence_3(self):
        # missing: unequal, contains, match
        atom = parse(tokenise("1 - 1 == 2"), {})[0]
        self.assertIsInstance(atom, operators.equal.ParseBinaryEqualIntegerInteger)
        atom = parse(tokenise("1 - 1 < 2"), {})[0]
        self.assertIsInstance(atom, operators.lesser.ParseBinaryLesserIntegerInteger)
        atom = parse(tokenise("1 - 1 < 2"), {})[0]
        self.assertIsInstance(atom, operators.lesser.ParseBinaryLesserIntegerInteger)
        atom = parse(tokenise("1 - 1 < 2"), {})[0]
        self.assertIsInstance(atom, operators.lesser.ParseBinaryLesserIntegerInteger)

    def test_precedence_4(self):
        atom = parse(tokenise("1 ^ 1 | 2"), {})[0]
        self.assertIsInstance(atom, operators.bitwise.ParseBinaryOrIntegerInteger)

    def test_precedence_5(self):
        atom = parse(tokenise("1 & 1 ^ 2"), {})[0]
        self.assertIsInstance(atom, operators.bitwise.ParseBinaryXorIntegerInteger)

    def test_precedence_6(self):
        atom = parse(tokenise("1 + 1 & 2"), {})[0]
        self.assertIsInstance(atom, operators.bitwise.ParseBinaryAndIntegerInteger)

    def test_precedence_7(self):
        atom = parse(tokenise("1 / 1 + 2"), {})[0]
        self.assertIsInstance(atom, operators.add.ParseBinaryAddFloatInteger)
        atom = parse(tokenise("1 / 1 - 2"), {})[0]
        self.assertIsInstance(atom, operators.subtract.ParseBinarySubtractFloatInteger)

    # missing: multiply, divide, positive, negative, complement, exponent
