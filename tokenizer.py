from enum import StrEnum, Enum
import re

# TODO (Tokenizer/Parser): token error printing with input string and token that messed up
# example:
# ((A & B) -> c)
#             ^


class Operator(StrEnum):
    DISJUNCTION = 'OR'
    CONJUNCTION = 'AND'
    CONDITIONAL = 'IF'
    BICONDITIONAL = 'IFF'
    NEGATION = 'NOT'
    OPENING_GROUPING = '('
    CLOSING_GROUPING = ')'


class Token:
    class Type(Enum):
        OPERATOR = 0
        SENTENCE_LETTER = 1

    def __init__(self, token_type, value, actual):
        self.token_type = token_type    # Operator/SL
        self.value = value              # OperatorEnum/Sentence Letter Name
        self.actual = actual            # String value from input

    def __repr__(self):
        return f"'{self.value}'"


class TokenizerException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class Tokenizer:
    def __init__(self, definition):
        self.definition = definition

    def tokenize_operation(self) -> (bool, Operator, str):
        for operation in Operator:
            for definition in self.definition['tokens'][operation]:
                if self.formula[self.index:self.index + len(definition)] == definition:
                    self.index += len(definition)
                    return (True, operation, definition)
        return (False, None, None)

    def add_sentence_letter(self) -> None:
        if self.current_sentence_letter:
            t = Token(Token.Type.SENTENCE_LETTER, self.current_sentence_letter, self.current_sentence_letter)
            self.tokens.append(t)
            self.current_sentence_letter = ""

    def add_to_sentence_letter(self):
        char = self.formula[self.index]
        if not re.match(r"[A-Z]|_|\d", char):
            raise TokenizerException(f"Invalid character found while tokenizing using {self.definition['name']} definition: '{char}' at index: {self.index}")
        self.current_sentence_letter += char
        self.index += 1

    def check_grouping(self, operation, definition):
        if operation == Operator.OPENING_GROUPING:
            # append the definition to match with closing
            self.grouping_stack.append(definition)
            
        elif operation == Operator.CLOSING_GROUPING:
            # if stack is empty, parens mismatch
            if len(self.grouping_stack) == 0:
                raise TokenizerException("Too many closing grouping operators.")
            top = self.grouping_stack.pop()
            # match open and close, use index from definition list?
            opening_index = self.definition['tokens'][Operator.OPENING_GROUPING].index(top)
            closing_index = self.definition['tokens'][Operator.CLOSING_GROUPING].index(definition)
            if opening_index != closing_index:
                raise TokenizerException("Parens mismatch!")

    def tokenize(self, formula) -> None:
        self.formula = formula.replace(' ', '')
        self.current_sentence_letter = ""
        self.index = 0
        self.tokens = []

        self.grouping_stack = []
        self.has_outer_parens = True
        while self.index < len(self.formula):
            success, operation, definition = self.tokenize_operation()
            if success:
                # if we found an operation, add whatever sentence letter
                # we've been constructing, then the operator
                self.add_sentence_letter()
                t = Token(Token.Type.OPERATOR, operation, definition)
                self.tokens.append(t)

                self.check_grouping(operation, definition)
            else:
                self.add_to_sentence_letter()
        self.add_sentence_letter()

        # if stack still has anything in it, parens mismatch
        if len(self.grouping_stack) != 0:
            raise TokenizerException("Too many opening grouping operators.")

        return self.tokens
