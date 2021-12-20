import unittest
from ipaddress import ip_network

from scpl.lexer import tokenise
from scpl.parser import parse
from scpl.parser import (ParseCIDRv4, ParseCIDRv6, ParseInteger, ParseFloat,
    ParseRegex, ParseString)

class EvalTestString(unittest.TestCase):
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

class EvalTestIPv4(unittest.TestCase):
    def test_divideinteger(self):
        addr = "10.84.1.1/24"
        atom = parse(tokenise(addr), {})[0].eval({})
        self.assertIsInstance(atom, ParseCIDRv4)
        reference = ip_network(addr, strict=False)
        self.assertEqual(atom.integer, int(reference.network_address))
        self.assertEqual(atom.prefix, 24)

class EvalTestIPv6(unittest.TestCase):
    def test_divideinteger(self):
        addr = "fd84:9d71:8b8:1::1/48"
        atom = parse(tokenise(addr), {})[0].eval({})
        self.assertIsInstance(atom, ParseCIDRv6)
        reference = ip_network(addr, strict=False)
        self.assertEqual(atom.integer, int(reference.network_address))
        self.assertEqual(atom.prefix, 48)
