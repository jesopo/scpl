import unittest
from ipaddress import ip_network

from scpl.lexer import tokenise
from scpl.parser import parse
from scpl.parser import (ParseBool, ParseCIDRv4, ParseCIDRv6, ParseInteger, ParseFloat,
    ParseRegex, ParseString)

class EvalTestString(unittest.TestCase):
    def test_add_string(self):
        atom = parse(tokenise('"asd" + "asd"'), {})[0].eval({})
        self.assertIsInstance(atom, ParseString)
        self.assertEqual(atom.value, "asdasd")
        self.assertEqual(atom.delimiter, '"')

    def test_not(self):
        atom = parse(tokenise('!"asd"'), {})[0].eval({})
        self.assertIsInstance(atom, ParseBool)
        self.assertEqual(atom.value, False)
        atom = parse(tokenise('!""'), {})[0].eval({})
        self.assertEqual(atom.value, True)

    def test_add_regex(self):
        atom = parse(tokenise('"asd." + /asd/i'), {})[0].eval({})
        self.assertIsInstance(atom, ParseRegex)
        self.assertEqual(atom.pattern, "asd\.(?i:asd)")
        self.assertEqual(atom.delimiter, None)
        self.assertEqual(atom.flags, set())

    def test_equal_string(self):
        atom = parse(tokenise('"asd" == "asd"'), {})[0].eval({})
        self.assertIsInstance(atom, ParseBool)
        self.assertEqual(atom.value, True)
        atom = parse(tokenise('"asd" == "bsd"'), {})[0].eval({})
        self.assertEqual(atom.value, False)
    def test_unequal_string(self):
        atom = parse(tokenise('"asd" != "asd"'), {})[0].eval({})
        self.assertIsInstance(atom, ParseBool)
        self.assertEqual(atom.value, False)
        atom = parse(tokenise('"asd" != "bsd"'), {})[0].eval({})
        self.assertEqual(atom.value, True)

    def test_contains_string(self):
        atom = parse(tokenise('"a" in "asd"'), {})[0].eval({})
        self.assertIsInstance(atom, ParseBool)
        self.assertEqual(atom.value, True)
        atom = parse(tokenise('"b" in "asd"'), {})[0].eval({})
        self.assertEqual(atom.value, False)

    def test_match_regex(self):
        atom = parse(tokenise('"asd" =~ /^asd$/'), {})[0].eval({})
        self.assertIsInstance(atom, ParseString)
        self.assertEqual(atom.value, "asd")
        atom = parse(tokenise('"asd" =~ /^bsd$/'), {})[0].eval({})
        self.assertEqual(atom.value, "")
