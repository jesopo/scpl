import unittest
from ipaddress import ip_address, ip_network

from scpl.lexer import tokenise
from scpl.parser import operators, parse, ParserError, ParserTypeError
from scpl.parser import (ParseInteger, ParseCIDRv4, ParseCIDRv6, ParseIPv4, ParseIPv6,
    ParseFloat, ParseRegex, ParseString)

class ParserTestString(unittest.TestCase):
    def test(self):
        atoms, deps = parse(tokenise('"asd"'), {})
        self.assertIsInstance(atoms[0], ParseString)
        self.assertEqual(atoms[0].value, "asd")
        self.assertEqual(atoms[0].delimiter, '"')

class ParserTestRegex(unittest.TestCase):
    def test_simple(self):
        atoms, deps = parse(tokenise("/a/"), {})
        self.assertIsInstance(atoms[0], ParseRegex)
        self.assertEqual(atoms[0].pattern, "a")
        self.assertEqual(atoms[0].delimiter, "/")
        self.assertEqual(atoms[0].flags, set())

    def test_flags(self):
        atoms, deps = parse(tokenise("/a/abc"), {})
        self.assertIsInstance(atoms[0], ParseRegex)
        self.assertEqual(atoms[0].pattern, "a")
        self.assertEqual(atoms[0].delimiter, "/")
        self.assertEqual(atoms[0].flags, set("abc"))

class ParserTestInteger(unittest.TestCase):
    def test(self):
        atoms, deps = parse(tokenise("123"), {})
        self.assertIsInstance(atoms[0], ParseInteger)
        self.assertEqual(atoms[0].value, 123)

class ParserTestHex(unittest.TestCase):
    def test(self):
        atoms, deps = parse(tokenise("0xff"), {})
        self.assertIsInstance(atoms[0], ParseInteger)
        self.assertEqual(atoms[0].value, 255)

class ParserTestDuration(unittest.TestCase):
    def test(self):
        atoms, deps = parse(tokenise("1w2d3h4m5s"), {})
        self.assertIsInstance(atoms[0], ParseInteger)
        self.assertEqual(atoms[0].value, 788645)

class ParserTestFloat(unittest.TestCase):
    def test(self):
        atoms, deps = parse(tokenise("123.0"), {})
        self.assertIsInstance(atoms[0], ParseFloat)
        self.assertEqual(atoms[0].value, 123.0)

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

class ParserTestParenthesis(unittest.TestCase):
    def test_unwrap(self):
        atoms, deps = parse(tokenise("(1)"), {})
        self.assertIsInstance(atoms[0], ParseInteger)

    def test_nested(self):
        atoms, deps = parse(tokenise("((1))"), {})
        self.assertIsInstance(atoms[0], ParseInteger)

    def test_unfinished(self):
        with self.assertRaises(ParserError):
            atoms, deps = parse(tokenise("(1"), {})

class ParserTestSet(unittest.TestCase):
    def test_empty(self):
        atoms, deps = parse(tokenise("{}"), {})
        self.assertIsInstance(atoms[0], operators.set.ParseSet)

    def test_integer(self):
        atoms, deps = parse(tokenise("{1, 2}"), {})
        self.assertIsInstance(atoms[0], operators.set.ParseSetInteger)

    def test_float(self):
        atoms, deps = parse(tokenise("{1.0, 2.0}"), {})
        self.assertIsInstance(atoms[0], operators.set.ParseSetFloat)

    def test_string(self):
        atoms, deps = parse(tokenise('{"a", "b"}'), {})
        self.assertIsInstance(atoms[0], operators.set.ParseSetString)

    def test_ipv4(self):
        atoms, deps = parse(tokenise("{10.84.1.1, 10.84.1.2}"), {})
        self.assertIsInstance(atoms[0], operators.set.ParseSetIPv4)

    def test_ipv6(self):
        atoms, deps = parse(tokenise("{fd84:9d71:8b8:1::1, fd84:9d71:8b8:1::2}"), {})
        self.assertIsInstance(atoms[0], operators.set.ParseSetIPv6)

    def test_invalid_mixed(self):
        tokens = tokenise("{1, 1.0}")
        with self.assertRaises(ParserTypeError) as cm:
            parse(tokens.copy(), {})
        self.assertEqual(tokens[4], cm.exception.token)
