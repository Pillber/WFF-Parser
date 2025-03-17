import re
from tokenizer import Operator


def default_disjunction(left, right):
    return left or right


def default_conjunction(left, right):
    return left and right


def default_conditional(left, right):
    return not left or right


def default_biconditional(left, right):
    return left == right


def default_negation(main_component):
    return not main_component


class Operation:
    function_map = {
        Operator.DISJUNCTION: default_disjunction,
        Operator.CONJUNCTION: default_conjunction,
        Operator.CONDITIONAL: default_conditional,
        Operator.BICONDITIONAL: default_biconditional,
        Operator.NEGATION: default_negation,
    }

    def __init__(self, operator):
        self.operator = operator
        self.truth_value = None


class SentenceLetter(Operation):
    def __init__(self, token):
        self.name = token.value
        self.valid()
        super().__init__('SL')

    def valid(self):
        pattern = r"([A-Z]_\d+)|(^[A-Z]$)"
        match = re.match(pattern, self.name)
        if not match:
            raise ValueError

    def solve(self):
        return self.truth_value

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, SentenceLetter):
            return self.name == other.name
        return False


class UnaryOperation(Operation):
    def __init__(self, operator, main_component):
        super().__init__(operator)
        self.main_component = main_component

    def solve(self):
        mc = self.main_component.solve()
        self.truth_value = Operation.function_map[self.operator](mc)
        return self.truth_value

    def __repr__(self):
        return self.operator + " (" + str(self.main_component) + ")"


class BinaryOperation(Operation):
    def __init__(self, operator, left, right):
        super().__init__(operator)
        self.left = left
        self.right = right

    def solve(self):
        l = self.left.solve()
        r = self.right.solve()
        self.truth_value = Operation.function_map[self.operator](l, r)
        return self.truth_value

    def __repr__(self):
        return self.operator + " (" + str(self.left) + ", " + str(self.right) + ")"
