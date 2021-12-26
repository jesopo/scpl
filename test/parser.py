import unittest
from re        import compile as re_compile
from ipaddress import ip_address, ip_network

from scpl.lexer import tokenise
from scpl.parser import parse
from scpl.parser import (ParseInteger, ParseCIDRv4, ParseCIDRv6, ParseIPv4, ParseIPv6,
    ParseFloat, ParseRegex, ParseString)

class ParserTestString(unittest.TestCase):
    def test(self):
        atoms, deps = parse(tokenise('"asd"'), {})
        self.assertIsInstance(atoms[0], ParseString)
        self.assertEqual(atoms[0].value, "asd")
        self.assertEqual(atoms[0].delimiter, '"')

class ParseTestRegex(unittest.TestCase):
    def test_simple(self):
        atoms, deps = parse(tokenise("/a/"), {})
        self.assertIsInstance(atoms[0], ParseRegex)
        self.assertEqual(atoms[0].pattern, "a")
        self.assertEqual(atoms[0].delimiter, "/")
        self.assertEqual(atoms[0].compiled, re_compile("a"))
        self.assertEqual(atoms[0].flags, set())

    def test_flags(self):
        atoms, deps = parse(tokenise("/a/abc"), {})
        self.assertIsInstance(atoms[0], ParseRegex)
        self.assertEqual(atoms[0].pattern, "a")
        self.assertEqual(atoms[0].delimiter, "/")
        self.assertEqual(atoms[0].compiled, re_compile("a"))
        self.assertEqual(atoms[0].flags, set("abc"))

class ParserTestInteger(unittest.TestCase):
    def test(self):
        atoms, deps = parse(tokenise("123"), {})
        self.assertIsInstance(atoms[0], ParseInteger)
        self.assertEqual(atoms[0].value, 123)

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
