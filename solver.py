from parser import Parser


class Solver:
    def __init__(self, definition='informal'):
        self.conclusion = None
        self.premises = []
        self.parser = Parser(definition) # set definition?

    def add_premise(self, sentence):
        premise = self.parser.parse(sentence)
        self.premises.append(premise)

    def set_conclusion(self, sentence):
        if self.conclusion is not None:
            raise Exception('conclusion already set')
        self.conclusion = self.parser.parse(sentence)

    def solve(self):
        sentence_letters = list(self.parser.sentence_letters)

        # for every sentence letter combination
        for i in range(2 ** len(sentence_letters)):
            for j in range(len(sentence_letters)):
                sentence_letters[j].truth_value = bool(i & (2 ** j))

            if not self.conclusion.solve():
                for premise in self.premises:
                    if not premise.solve():
                        break
                else:
                    # found a counterexample: invalid
                    return False

        # no counterexamples exist: valid
        return True
