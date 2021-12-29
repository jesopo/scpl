import re, unittest
from ipaddress import ip_network

from scpl.lexer import tokenise
from scpl.parser import parse
from scpl.parser import (ParseBool, ParseCIDRv4, ParseCIDRv6, ParseInteger, ParseFloat,
    ParseRegex, ParseString)

class EvalTestString(unittest.TestCase):
    def test_add_string(self):
        atoms, deps = parse(tokenise('"asd" + "asd"'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, str)
        self.assertEqual(atom, "asdasd")

    def test_not(self):
        atoms, deps = parse(tokenise('!"asd"'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, bool)
        self.assertEqual(atom, False)

        atoms, deps = parse(tokenise('!""'), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom, True)

    def test_add_regex(self):
        atoms, deps = parse(tokenise('"asd." + /asd/i'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, re.Pattern)
        self.assertEqual(atom.pattern, "asd\.(?i:asd)")

    def test_equal_string(self):
        atoms, deps = parse(tokenise('"asd" == "asd"'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, bool)
        self.assertEqual(atom, True)

        atoms, deps = parse(tokenise('"asd" == "bsd"'), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom, False)
    def test_unequal_string(self):
        atoms, deps = parse(tokenise('"asd" != "asd"'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, bool)
        self.assertEqual(atom, False)

        atoms, deps = parse(tokenise('"asd" != "bsd"'), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom, True)

    def test_contains_string(self):
        atoms, deps = parse(tokenise('"a" in "asd"'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, bool)
        self.assertEqual(atom, True)

        atoms, deps = parse(tokenise('"b" in "asd"'), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom, False)

    def test_match_regex(self):
        atoms, deps = parse(tokenise('"asd" =~ /^asd$/'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, str)
        self.assertEqual(atom, "asd")

        atoms, deps = parse(tokenise('"asd" =~ /^bsd$/'), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom, "")

class EvalTestRegex(unittest.TestCase):
    def test_match(self):
        atoms, deps = parse(tokenise("'asd' =~ /^as/"), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, str)
        self.assertEqual(atom, "as")

        atoms, deps = parse(tokenise("'asd' =~ /^bs/"), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom, "")
