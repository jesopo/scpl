import unittest

from scpl.lexer import tokenise
from scpl.parser import operators, parse
from scpl.parser import (ParseInteger, ParseIPv4, ParseIPv6, ParseBool, ParseFloat,
    ParseRegex, ParseString)

class ParseOperatorTestAdd(unittest.TestCase):
    def test_string_string(self):
        atoms, deps = parse(tokenise('"a" + "a"'), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddStringString)
    def test_string_regex(self):
        atoms, deps = parse(tokenise('"a" + /a/'), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddStringRegex)

    def test_regex_regex(self):
        atoms, deps = parse(tokenise("/a/ + /a/"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddRegexRegex)
    def test_regex_string(self):
        atoms, deps = parse(tokenise('"a" + /a/'), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddStringRegex)

    def test_integer_integer(self):
        atoms, deps = parse(tokenise("1 + 1"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddIntegerInteger)
    def test_integer_float(self):
        atoms, deps = parse(tokenise("1 + 1.0"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddIntegerFloat)

    def test_float_float(self):
        atoms, deps = parse(tokenise("1.0 + 1.0"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddFloatFloat)
    def test_float_integer(self):
        atoms, deps = parse(tokenise("1.0 + 1"), {})
        self.assertIsInstance(atoms[0], operators.add.ParseBinaryAddFloatInteger)

class ParseOperatorTestSubtract(unittest.TestCase):
    def test_integer_integer(self):
        atoms, deps = parse(tokenise("1 - 1"), {})
        self.assertIsInstance(atoms[0], operators.subtract.ParseBinarySubtractIntegerInteger)
    def test_integer_float(self):
        atoms, deps = parse(tokenise("1 - 1.0"), {})
        self.assertIsInstance(atoms[0], operators.subtract.ParseBinarySubtractIntegerFloat)

    def test_float_float(self):
        atoms, deps = parse(tokenise("1.0 - 1.0"), {})
        self.assertIsInstance(atoms[0], operators.subtract.ParseBinarySubtractFloatFloat)
    def test_float_integer(self):
        atoms, deps = parse(tokenise("1.0 - 1"), {})
        self.assertIsInstance(atoms[0], operators.subtract.ParseBinarySubtractFloatInteger)

class ParseOperatorTestDivide(unittest.TestCase):
    def test_integer_integer(self):
        atoms, deps = parse(tokenise("1 / 1"), {})
        self.assertIsInstance(atoms[0], operators.divide.ParseBinaryDivideIntegerInteger)
    def test_integer_float(self):
        atoms, deps = parse(tokenise("1 / 1.0"), {})
        self.assertIsInstance(atoms[0], operators.divide.ParseBinaryDivideIntegerFloat)

    def test_float_float(self):
        atoms, deps = parse(tokenise("1.0 / 1.0"), {})
        self.assertIsInstance(atoms[0], operators.divide.ParseBinaryDivideFloatFloat)
    def test_float_integer(self):
        atoms, deps = parse(tokenise("1.0 / 1"), {})
        self.assertIsInstance(atoms[0], operators.divide.ParseBinaryDivideFloatInteger)

class ParseOperatorTestMultiply(unittest.TestCase):
    def test_integer_integer(self):
        atoms, deps = parse(tokenise("1 * 1"), {})
        self.assertIsInstance(atoms[0], operators.multiply.ParseBinaryMultiplyIntegerInteger)
    def test_integer_float(self):
        atoms, deps = parse(tokenise("1 * 1.0"), {})
        self.assertIsInstance(atoms[0], operators.multiply.ParseBinaryMultiplyIntegerFloat)

    def test_float_float(self):
        atoms, deps = parse(tokenise("1.0 * 1.0"), {})
        self.assertIsInstance(atoms[0], operators.multiply.ParseBinaryMultiplyFloatFloat)
    def test_float_integer(self):
        atoms, deps = parse(tokenise("1.0 * 1"), {})
        self.assertIsInstance(atoms[0], operators.multiply.ParseBinaryMultiplyFloatInteger)

class ParseOperatorTestExponent(unittest.TestCase):
    def test_integer_integer(self):
        atoms, deps = parse(tokenise("1 ** 1"), {})
        self.assertIsInstance(atoms[0], operators.exponent.ParseBinaryExponentIntegerInteger)
    def test_integer_negative(self):
        atoms, deps = parse(tokenise("1 ** -1"), {})
        self.assertIsInstance(atoms[0], operators.exponent.ParseBinaryExponentIntegerNegative)
    def test_integer_float(self):
        atoms, deps = parse(tokenise("1 ** 1.0"), {})
        self.assertIsInstance(atoms[0], operators.exponent.ParseBinaryExponentIntegerFloat)

    def test_float_float(self):
        atoms, deps = parse(tokenise("1.0 ** 1.0"), {})
        self.assertIsInstance(atoms[0], operators.exponent.ParseBinaryExponentFloatFloat)
    def test_float_integer(self):
        atoms, deps = parse(tokenise("1.0 ** 1"), {})
        self.assertIsInstance(atoms[0], operators.exponent.ParseBinaryExponentFloatInteger)

class ParseOperatorTestComplement(unittest.TestCase):
    def test_integer(self):
        atoms, deps = parse(tokenise("~1"), {})
        self.assertIsInstance(atoms[0], operators.complement.ParseUnaryComplementInteger)

    def test_regex(self):
        atoms, deps = parse(tokenise("~/a/"), {})
        self.assertIsInstance(atoms[0], operators.complement.ParseUnaryComplementRegex)
    def test_regex_double(self):
        # flatten a double complement in to an uncomplemented regex
        atoms, deps = parse(tokenise("~~/a/"), {})
        self.assertIsInstance(atoms[0], ParseRegex)

class ParseOperatorTestAnd(unittest.TestCase):
    def test_and_integer_integer(self):
        atoms, deps = parse(tokenise("1 & 1"), {})
        self.assertIsInstance(atoms[0], operators.bitwise.ParseBinaryAndIntegerInteger)

class ParseOperatorTestXor(unittest.TestCase):
    def test_and_integer_integer(self):
        atoms, deps = parse(tokenise("1 ^ 1"), {})
        self.assertIsInstance(atoms[0], operators.bitwise.ParseBinaryXorIntegerInteger)

class ParseOperatorTestOr(unittest.TestCase):
    def test_and_integer_integer(self):
        atoms, deps = parse(tokenise("1 | 1"), {})
        self.assertIsInstance(atoms[0], operators.bitwise.ParseBinaryOrIntegerInteger)

class ParseOperatorTestGreater(unittest.TestCase):
    def test_integer_integer(self):
        atoms, deps = parse(tokenise("1 > 1"), {})
        self.assertIsInstance(atoms[0], operators.greater.ParseBinaryGreaterIntegerInteger)
    def test_integer_float(self):
        atoms, deps = parse(tokenise("1 > 1.0"), {})
        self.assertIsInstance(atoms[0], operators.greater.ParseBinaryGreaterIntegerFloat)

    def test_float_float(self):
        atoms, deps = parse(tokenise("1.0 > 1.0"), {})
        self.assertIsInstance(atoms[0], operators.greater.ParseBinaryGreaterFloatFloat)
    def test_float_integer(self):
        atoms, deps = parse(tokenise("1.0 > 1"), {})
        self.assertIsInstance(atoms[0], operators.greater.ParseBinaryGreaterFloatInteger)

class ParseOperatorTestLesser(unittest.TestCase):
    def test_integer_integer(self):
        atoms, deps = parse(tokenise("1 < 1"), {})
        self.assertIsInstance(atoms[0], operators.lesser.ParseBinaryLesserIntegerInteger)
    def test_integer_float(self):
        atoms, deps = parse(tokenise("1 < 1.0"), {})
        self.assertIsInstance(atoms[0], operators.lesser.ParseBinaryLesserIntegerFloat)

    def test_float_float(self):
        atoms, deps = parse(tokenise("1.0 < 1.0"), {})
        self.assertIsInstance(atoms[0], operators.lesser.ParseBinaryLesserFloatFloat)
    def test_float_integer(self):
        atoms, deps = parse(tokenise("1.0 < 1"), {})
        self.assertIsInstance(atoms[0], operators.lesser.ParseBinaryLesserFloatInteger)

class ParseOperatorTestContains(unittest.TestCase):
    def test_string_string(self):
        atoms, deps = parse(tokenise('"a" in "asd"'), {})
        self.assertIsInstance(atoms[0], operators.contains.ParseBinaryContainsStringString)

    def test_ipv4_cidrv4(self):
        atoms, deps = parse(tokenise("10.84.1.1 in 10.84.0.0/16"), {})
        self.assertIsInstance(atoms[0], operators.contains.ParseBinaryContainsIPCIDR)

    def test_ipv6_cidrv6(self):
        atoms, deps = parse(tokenise("fd84:9d71:8b8:1::1 in fd84:9d71:8b8::/48"), {})
        self.assertIsInstance(atoms[0], operators.contains.ParseBinaryContainsIPCIDR)

class ParseOperatorTestMatch(unittest.TestCase):
    def test_string_regex(self):
        atoms, deps = parse(tokenise('"asd" =~ /^a/'), {})
        self.assertIsInstance(atoms[0], operators.match.ParseBinaryMatchStringRegex)

class ParseOperatorTestNot(unittest.TestCase):
    def test_string(self):
        atoms, deps = parse(tokenise('!"asd"'), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseUnaryNot)

    def test_regex(self):
        atoms, deps = parse(tokenise("!/a/"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseUnaryNot)

    def test_integer(self):
        atoms, deps = parse(tokenise("!1"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseUnaryNot)

    def test_float(self):
        atoms, deps = parse(tokenise("!1.0"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseUnaryNot)

    def test_bool(self):
        atoms, deps = parse(tokenise("!true"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseUnaryNot)

class ParseOperatorTestPositive(unittest.TestCase):
    def test_integer(self):
        atoms, deps = parse(tokenise("+1"), {})
        self.assertIsInstance(atoms[0], operators.positive.ParseUnaryPositiveInteger)

    def test_float(self):
        atoms, deps = parse(tokenise("+1.0"), {})
        self.assertIsInstance(atoms[0], operators.positive.ParseUnaryPositiveFloat)

class ParseOperatorTestNegative(unittest.TestCase):
    def test_integer(self):
        atoms, deps = parse(tokenise("-1"), {})
        self.assertIsInstance(atoms[0], operators.negative.ParseUnaryNegativeInteger)

    def test_float(self):
        atoms, deps = parse(tokenise("-1.0"), {})
        self.assertIsInstance(atoms[0], operators.negative.ParseUnaryNegativeFloat)

class ParseOperatorTestBoth(unittest.TestCase):
    def test_bool_bool(self):
        atoms, deps = parse(tokenise("true && true"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseBinaryBoth)

    def test_integer_integer(self):
        atoms, deps = parse(tokenise("1 && 1"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseBinaryBoth)

    def test_float_float(self):
        atoms, deps = parse(tokenise("1.0 && 1.0"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseBinaryBoth)

    def test_string_string(self):
        atoms, deps = parse(tokenise('"asd" && "asd"'), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseBinaryBoth)

    def test_regex_regex(self):
        atoms, deps = parse(tokenise("/a/ && /a/"), {})
        self.assertIsInstance(atoms[0], operators.bools.ParseBinaryBoth)

class ParseOperatorTestVariable(unittest.TestCase):
    def test_integer(self):
        atoms, deps = parse(tokenise("a"), {"a": ParseInteger})
        self.assertIsInstance(atoms[0], operators.variable.ParseVariableInteger)

    def test_float(self):
        atoms, deps = parse(tokenise("a"), {"a": ParseFloat})
        self.assertIsInstance(atoms[0], operators.variable.ParseVariableFloat)

    def test_string(self):
        atoms, deps = parse(tokenise("a"), {"a": ParseString})
        self.assertIsInstance(atoms[0], operators.variable.ParseVariableString)

    def test_regex(self):
        atoms, deps = parse(tokenise("a"), {"a": ParseRegex})
        self.assertIsInstance(atoms[0], operators.variable.ParseVariableRegex)

    def test_bool(self):
        atoms, deps = parse(tokenise("a"), {"a": ParseBool})
        self.assertIsInstance(atoms[0], operators.variable.ParseVariableBool)

    def test_ipv4(self):
        atoms, deps = parse(tokenise("a"), {"a": ParseIPv4})
        self.assertIsInstance(atoms[0], operators.variable.ParseVariableIPv4)

    def test_ipv6(self):
        atoms, deps = parse(tokenise("a"), {"a": ParseIPv6})
        self.assertIsInstance(atoms[0], operators.variable.ParseVariableIPv6)

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
