from parser import Parser, ParseException
from tokenizer import TokenizerException
from pytest import raises
import pytest

# TODO (Definitions/stretch): custom operators???


class TestSLParse:
    def test_correct(self):
        p = Parser()
        assert p.parse("A").__repr__() == "A"

    def test_correct_indexed(self):
        p = Parser()
        assert p.parse("A_1").__repr__() == "A_1"

    def test_incorrect_token(self):
        p = Parser()
        with raises(TokenizerException):
            p.parse("a")

    def test_no_index_number(self):
        p = Parser()
        with raises(ParseException):
            p.parse("A_")

    def test_bad_parens(self):
        p = Parser()
        with raises(ParseException):
            p.parse("(A)")


@pytest.mark.parametrize(
    'token,wrong_token,string_val',
    [
        ('v', '||', 'OR'),
        ('&', '*', 'AND'),
        ('->', '@', 'IF'),
        ('<->', '^', 'IFF'),
    ],
    ids=[
        "disjunction",
        "conjunction",
        "conditional",
        "biconditional",
    ]
)
class TestBinaryOperatorParse:
    @pytest.mark.parametrize('definition', ['informal', 'formal'])
    def test_simple(self, token, wrong_token, string_val, definition):
        p = Parser(definition)
        assert p.parse(f'(A {token} B)').__repr__() == f'{string_val} (A, B)'

    def test_wrong_token(self, token, wrong_token, string_val):
        p = Parser()
        with raises(TokenizerException):
            p.parse(f'(A {wrong_token} B)')
     
    def test_no_outer_parens_formal(self, token, wrong_token, string_val):
        p = Parser('formal')
        with raises(ParseException):
            p.parse(f'A {token} B')

    def test_no_outer_parens_informal(self, token, wrong_token, string_val):
        p = Parser()
        assert p.parse(f'A {token} B').__repr__() == f'{string_val} (A, B)'

    @pytest.mark.parametrize('definition', ['informal', 'formal'])
    def test_missing_first_operand(self, token, wrong_token, string_val, definition):
        p = Parser(definition)
        with raises(ParseException):
            p.parse(f'( {token} B)')

    @pytest.mark.parametrize('definition', ['informal', 'formal'])
    def test_missing_second_operand(self, token, wrong_token, string_val, definition):
        p = Parser()
        with raises(ParseException):
            p.parse(f'(A {token} )')


class TestNegationParse:
    @pytest.mark.parametrize('definition', ['informal', 'formal'])
    def test_simple(self, definition):
        p = Parser(definition)
        assert p.parse('~A').__repr__() == 'NOT (A)'

    @pytest.mark.parametrize('definition', ['informal', 'formal'])
    def test_outer_parens(self, definition):
        p = Parser(definition)
        with raises(ParseException):
            p.parse('(~A)')

    @pytest.mark.parametrize('definition', ['informal', 'formal'])
    def test_missing_operand(self, definition):
        p = Parser(definition)
        with raises(ParseException):
            p.parse('~ v B')


class TestComplex:
    def test_multi_definitions_correct(self):
        p = Parser('informal')
        assert p.parse('(A . B)').__repr__() == 'AND (A, B)'

    def test_nested(self):
        p = Parser()
        assert p.parse('(C -> (F & ~X))').__repr__() == 'IF (C, AND (F, NOT (X)))'

    def test_multi_definitions_incorrect(self):
        p = Parser('informal')
        with raises(ParseException):
            p.parse('(A . B) v (C & D)')

    def test_informal_brackets(self):
        p = Parser('informal')
        assert p.parse('[A v B]').__repr__() == 'OR (A, B)'

    def test_bracket_match(self):
        p = Parser()
        with raises(TokenizerException):
            p.parse('[A v B)')

    def test_nested_deep(self):
        p = Parser()
        assert p.parse('(([A . B] v B) <-> (C -> (F . ~X)))').__repr__() == 'IFF (OR (AND (A, B), B), IF (C, AND (F, NOT (X))))'
