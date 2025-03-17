import yaml
from tokenizer import Operator, Token, Tokenizer
from operation import SentenceLetter, UnaryOperation, BinaryOperation


class ParseException(Exception):
    def __init__(self, message, informal_error=False):
        self.message = message
        self.informal_error = informal_error
        super().__init__(message)


class Parser:
    def __init__(self, definition='informal'):
        with open('definitions.yaml', 'r') as f:
            all_definitions = yaml.load(f, Loader=yaml.SafeLoader)
            for d in all_definitions:
                if d['name'] == definition:
                    self.definition = d
                    break
            else:  # i love for/else 🤪
                raise ParseException(f"'{definition}' definition does not exists. Check definitions.yaml for available definitions.")

        self.tokenizer = Tokenizer(self.definition)

        self.sentence_letters = set()
        self.used_actuals = {}  # OperatorEnum:actual

    def advance(self):
        try:
            token = self.tokens[self.current_index]
        except IndexError:
            raise ParseException("End of expression reached before expected. Check parenthesis.")
        self.current_index += 1
        return token

    def parse_sentence_letter(self, start):
        self.current_index = start
        token = self.advance()
        try:
            sl = SentenceLetter(token)
            for set_sl in self.sentence_letters:
                if sl == set_sl:
                    return set_sl
            else:
                self.sentence_letters.add(sl)
                return sl
        except ValueError:
            raise ParseException("Invalid Sentence Letter: " + token.actual, True)

    def is_open_parens(self):
        token = self.advance()
        return token.token_type == Token.Type.OPERATOR and token.value == Operator.OPENING_GROUPING

    def is_close_parens(self):
        token = self.advance()
        return token.token_type == Token.Type.OPERATOR and token.value == Operator.CLOSING_GROUPING

    def parse_operator(self, operator):
        token = self.advance()

        if token.token_type != Token.Type.OPERATOR:
            return False

        actual = self.used_actuals.get(token.value)
        if not actual:
            self.used_actuals[token.value] = token.actual
        elif actual != token.actual:
            raise ParseException(f"Invalid use of multiple definitions of an operator.\n{token.actual} != {actual}", True)

        return token.value == operator

    def parse_binary_operator(self, operator, start):
        self.current_index = start
        if not self.is_open_parens():
            return None
        lhs = self.parse_wff(self.current_index)
        if not self.parse_operator(operator):
            return None
        rhs = self.parse_wff(self.current_index)
        if not self.is_close_parens():
            return None
        return BinaryOperation(operator, lhs, rhs)

    def parse_unary_operator(self, operator, start):
        self.current_index = start
        if not self.parse_operator(operator):
            return None
        main_component = self.parse_wff(self.current_index)
        return UnaryOperation(Operator.NEGATION, main_component)

    def parse_wff(self, start=0):
        if b := self.parse_binary_operator(Operator.BICONDITIONAL, start):
            return b
        if c := self.parse_binary_operator(Operator.CONJUNCTION, start):
            return c
        if d := self.parse_binary_operator(Operator.DISJUNCTION, start):
            return d
        if c := self.parse_binary_operator(Operator.CONDITIONAL, start):
            return c
        if n := self.parse_unary_operator(Operator.NEGATION, start):
            return n
        if sl := self.parse_sentence_letter(start):
            return sl

    def parse_binary_operator_no_parens(self, operator, start):
        self.current_index = start
        lhs = self.parse_wff(self.current_index)
        if not self.parse_operator(operator):
            return None
        rhs = self.parse_wff(self.current_index)
        return BinaryOperation(operator, lhs, rhs)

    def parse_informal_wff(self):
        if b := self.parse_binary_operator_no_parens(Operator.BICONDITIONAL, 0):
            return b
        if c := self.parse_binary_operator_no_parens(Operator.CONJUNCTION, 0):
            return c
        if d := self.parse_binary_operator_no_parens(Operator.DISJUNCTION, 0):
            return d
        if c := self.parse_binary_operator_no_parens(Operator.CONDITIONAL, 0):
            return c
        if n := self.parse_unary_operator(Operator.NEGATION, 0):
            return n
        if sl := self.parse_sentence_letter(0):
            return sl

    def parse(self, input_str):
        self.tokens = self.tokenizer.tokenize(input_str)

        if self.definition['allow_drop_outer_grouping']:
            try:
                self.current_index = 0
                result = self.parse_informal_wff()
                return result
            except ParseException as pe:
                # not all parse exceptions are equal and can be ignored...
                if pe.informal_error:
                    raise pe
        self.current_index = 0
        result = self.parse_wff()

        if self.current_index != len(self.tokens):
            raise ParseException(f"Parse stopped before end of expression using '{self.definition['name']}' definition. Check outermost parenthesis")
        return result
