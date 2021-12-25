import unittest
from re        import compile as re_compile
from ipaddress import ip_address, ip_network

from scpl.lexer import tokenise
from scpl.parser import operators, parse, ParserError
from scpl.parser import (ParseInteger, ParseCIDRv4, ParseCIDRv6, ParseIPv4, ParseIPv6,
    ParseFloat, ParseRegex, ParseString)

class ParserTestString(unittest.TestCase):
    def test_lone(self):
        atoms, deps = parse(tokenise('"asd"'), {})
        self.assertIsInstance(atoms[0], ParseString)
        self.assertEqual(atoms[0].value, "asd")
        self.assertEqual(atoms[0].delimiter, '"')

    def test_addstring(self):
        atoms, deps = parse(tokenise('"asd" + "asd"'), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddStringString)

    def test_addregex(self):
        atoms, deps = parse(tokenise('"asd" + /asd/'), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddStringRegex)

    def test_not(self):
        atoms, deps = parse(tokenise("!'a'"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseUnaryNot)

class ParseTestRegex(unittest.TestCase):
    def test_lone(self):
        atoms, deps = parse(tokenise("/a/"), {})
        self.assertIsInstance(atoms[0], ParseRegex)
        self.assertEqual(atoms[0].pattern, "a")
        self.assertEqual(atoms[0].delimiter, "/")
        self.assertEqual(atoms[0].compiled, re_compile("a"))
        self.assertEqual(atoms[0].flags, set())

    def test_addregex(self):
        atoms, deps = parse(tokenise('/asd/ + /asd/'), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddRegexRegex)

    def test_addstring(self):
        atoms, deps = parse(tokenise('/asd/ + "asd"'), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddRegexString)

    def test_not(self):
        atoms, deps = parse(tokenise("!/a/"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseUnaryNot)

    def test_complement(self):
        atoms, deps = parse(tokenise("~/a/"), {})
        self.assertIsInstance(atoms[0], operators.complement.ParseUnaryComplementRegex)

class ParseTestRegexset(unittest.TestCase):
    def test_complement(self):
        atoms, deps = parse(tokenise("~/a/"), {})
        self.assertIsInstance(atoms[0], operators.complement.ParseUnaryComplementRegex)

class ParserTestInteger(unittest.TestCase):
    def test_lone(self):
        atoms, deps = parse(tokenise("123"), {})
        self.assertIsInstance(atoms[0], ParseInteger)
        self.assertEqual(atoms[0].value, 123)

    def test_addinteger(self):
        atoms, deps = parse(tokenise("1 + 1"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddIntegerInteger)
    def test_addinteger_negative(self):
        atoms, deps = parse(tokenise("1 + -1"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddIntegerInteger)

    def test_addfloat(self):
        atoms, deps = parse(tokenise("1 + 1.0"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddIntegerFloat)
    def test_addfloat_negative(self):
        atoms, deps = parse(tokenise("1 + -1.0"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddIntegerFloat)

    def test_negative(self):
        atoms, deps = parse(tokenise("-1"), {})
        self.assertIsInstance(atoms[0], operators.negative.ParseUnaryNegativeInteger)

    def test_complement(self):
        atoms, deps = parse(tokenise("~1"), {})
        self.assertIsInstance(atoms[0], operators.complement.ParseUnaryComplementInteger)

    def test_not(self):
        atoms, deps = parse(tokenise("!1"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseUnaryNot)

class ParserTestFloat(unittest.TestCase):
    def test_lone(self):
        atoms, deps = parse(tokenise("123.0"), {})
        self.assertIsInstance(atoms[0], ParseFloat)
        self.assertEqual(atoms[0].value, 123.0)

    def test_addfloat(self):
        atoms, deps = parse(tokenise("1.0 + 1.0"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddFloatFloat)

    def test_addinteger(self):
        atoms, deps = parse(tokenise("1.0 + 1"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddFloatInteger)

    def test_negative(self):
        atoms, deps = parse(tokenise("-1.0"), {})
        self.assertIsInstance(atoms[0], operators.negative.ParseUnaryNegativeFloat)

    def test_not(self):
        atoms, deps = parse(tokenise("!1.0"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseUnaryNot)

class ParserTestIPv4(unittest.TestCase):
    def test(self):
        addr = "10.84.1.1"
        atoms, deps = parse(tokenise(addr), {})
        self.assertIsInstance(atoms[0], ParseIPv4)
        self.assertEqual(atoms[0].integer, int(ip_address(addr)))

class ParserTestCIDRv4(unittest.TestCase):
    def test(self):
        addr = "10.84.1.1/16"
        atoms, deps = parse(tokenise(addr), {})
        self.assertIsInstance(atoms[0], ParseCIDRv4)
        self.assertEqual(atoms[0].integer, int(ip_network(addr, strict=False).network_address))
        self.assertEqual(atoms[0].prefix, 16)

    def test_invalid(self):
        self.assertRaises(ValueError, lambda: parse(tokenise("10.84.1.1/33"), {}))

class ParserTestIPv6(unittest.TestCase):
    def test(self):
        addr = "fd84:9d71:8b8:1::1"
        atoms, deps = parse(tokenise(addr), {})
        self.assertIsInstance(atoms[0], ParseIPv6)
        self.assertEqual(atoms[0].integer, int(ip_address(addr)))

class ParserTestCIDRv6(unittest.TestCase):
    def test(self):
        addr = "fd84:9d71:8b8:1::1/48"
        atoms, deps = parse(tokenise(addr), {})
        self.assertIsInstance(atoms[0], ParseCIDRv6)
        self.assertEqual(atoms[0].integer, int(ip_network(addr, strict=False).network_address))
        self.assertEqual(atoms[0].prefix, 48)

    def test_invalid(self):
        self.assertRaises(ValueError, lambda: parse(tokenise("fd84:9d71:8b8:1::1/129"), {}))

class ParserTestBinaryOperator(unittest.TestCase):
    def test_precedence_0(self):
        atoms, deps = parse(tokenise("1 && 1 || 1"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseBinaryEither)

    def test_precedence_1(self):
        atoms, deps = parse(tokenise("true == true && true"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseBinaryBoth)

    def test_precedence_3(self):
        # missing: contains, match
        atoms, deps = parse(tokenise("1 - 1 == 2"), {})
        self.assertIsInstance(atoms[0], operators.equal.ParseBinaryEqualIntegerInteger)
        atoms, deps = parse(tokenise("1 - 1 != 2"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseUnaryNot)
        atoms, deps = parse(tokenise("1 - 1 < 2"), {})
        self.assertIsInstance(atoms[0], operators.lesser.ParseBinaryLesserIntegerInteger)
        atoms, deps = parse(tokenise("1 - 1 > 2"), {})
        self.assertIsInstance(atoms[0], operators.greater.ParseBinaryGreaterIntegerInteger)

    def test_precedence_4(self):
        atoms, deps = parse(tokenise("1 ^ 1 | 2"), {})
        self.assertIsInstance(atoms[0], operators.bitwise.ParseBinaryOrIntegerInteger)

    def test_precedence_5(self):
        atoms, deps = parse(tokenise("1 & 1 ^ 2"), {})
        self.assertIsInstance(atoms[0], operators.bitwise.ParseBinaryXorIntegerInteger)

    def test_precedence_6(self):
        atoms, deps = parse(tokenise("1 + 1 & 2"), {})
        self.assertIsInstance(atoms[0], operators.bitwise.ParseBinaryAndIntegerInteger)

    def test_precedence_7(self):
        atoms, deps = parse(tokenise("1 / 1 + 2"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddFloatInteger)
        atoms, deps = parse(tokenise("1 / 1 - 2"), {})
        self.assertIsInstance(atoms[0], operators.subtract.ParseBinarySubtractFloatInteger)

    def test_precedence_8(self):
        atoms, deps = parse(tokenise("1 ** 1 * 2"), {})
        self.assertIsInstance(atoms[0], operators.multiply.ParseBinaryMultiplyIntegerInteger)
        atoms, deps = parse(tokenise("1 ** 1 / 2"), {})
        self.assertIsInstance(atoms[0], operators.divide.ParseBinaryDivideIntegerInteger)

    # missing: 9 (positive, negative)
    # missing: 10 (complement)
    # missing: 11 (exponent)
