import unittest
from ipaddress import ip_network

from scpl.lexer import tokenise
from scpl.parser import parse
from scpl.parser import (ParseBool, ParseCIDRv4, ParseCIDRv6, ParseInteger, ParseFloat,
    ParseRegex, ParseString)

class EvalTestString(unittest.TestCase):
    def test_add_string(self):
        atoms, deps = parse(tokenise('"asd" + "asd"'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, ParseString)
        self.assertEqual(atom.value, "asdasd")
        self.assertEqual(atom.delimiter, '"')

    def test_not(self):
        atoms, deps = parse(tokenise('!"asd"'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, ParseBool)
        self.assertEqual(atom.value, False)

        atoms, deps = parse(tokenise('!""'), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom.value, True)

    def test_add_regex(self):
        atoms, deps = parse(tokenise('"asd." + /asd/i'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, ParseRegex)
        self.assertEqual(atom.pattern, "asd\.(?i:asd)")
        self.assertEqual(atom.delimiter, None)
        self.assertEqual(atom.flags, set())

    def test_equal_string(self):
        atoms, deps = parse(tokenise('"asd" == "asd"'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, ParseBool)
        self.assertEqual(atom.value, True)

        atoms, deps = parse(tokenise('"asd" == "bsd"'), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom.value, False)
    def test_unequal_string(self):
        atoms, deps = parse(tokenise('"asd" != "asd"'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, ParseBool)
        self.assertEqual(atom.value, False)

        atoms, deps = parse(tokenise('"asd" != "bsd"'), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom.value, True)

    def test_contains_string(self):
        atoms, deps = parse(tokenise('"a" in "asd"'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, ParseBool)
        self.assertEqual(atom.value, True)

        atoms, deps = parse(tokenise('"b" in "asd"'), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom.value, False)

    def test_match_regex(self):
        atoms, deps = parse(tokenise('"asd" =~ /^asd$/'), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, ParseString)
        self.assertEqual(atom.value, "asd")

        atoms, deps = parse(tokenise('"asd" =~ /^bsd$/'), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom.value, "")

class EvalTestRegex(unittest.TestCase):
    def test_match(self):
        atoms, deps = parse(tokenise("'asd' =~ /^as/"), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, ParseString)
        self.assertEqual(atom.value, "as")

        atoms, deps = parse(tokenise("'asd' =~ /^bs/"), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom.value, "")

    def test_complement_match(self):
        atoms, deps = parse(tokenise("'asd' =~ ~/^as/"), {})
        atom = atoms[0].eval({})
        self.assertIsInstance(atom, ParseBool)
        self.assertEqual(atom.value, False)

        atoms, deps = parse(tokenise("'asd' =~ ~/^bd/"), {})
        atom = atoms[0].eval({})
        self.assertEqual(atom.value, True)
