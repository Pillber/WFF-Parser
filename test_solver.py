from solver import Solver
import pytest


def test_set_conclusions():
    s = Solver()
    s.set_conclusion('A')
    with pytest.raises(Exception):
        s.set_conclusion('B')


def test_modus_ponens():
    s = Solver()
    s.add_premise('A -> B')
    s.add_premise('A')
    s.set_conclusion('B')

    assert s.solve()


def test_modus_tolens():
    s = Solver()
    s.add_premise('A -> B')
    s.add_premise('~B')
    s.set_conclusion('~A')

    assert s.solve()


def test_conditional_exchange():
    s = Solver()
    s.add_premise('A -> B')
    s.set_conclusion('~A v B')

    assert s.solve()


def test_de_morgans_and():
    s = Solver()
    s.add_premise('~(A & B)')
    s.set_conclusion('~A v ~B')

    assert s.solve()


def test_de_morgans_or():
    s = Solver()
    s.add_premise('~(A v B)')
    s.set_conclusion('~A & ~B')

    assert s.solve()


def test_bad_modus_tolens():
    s = Solver()
    s.add_premise('A -> B')
    s.add_premise('~A')
    s.set_conclusion('~B')

    assert not s.solve()


tests = [
    (('P <-> Q', 'Q'), 'P', True),
    (('P <-> ~Q', 'Q v P'), '~Q v ~P', True),
    (('P <-> Q', 'Q'), 'P', True),
    (('P -> (~Q & ~R)', '~R <-> Q'), 'R v ~P', True),
    (('P <-> ~Q', 'Q v P'), '~Q v ~P', True),
    (('(P v Q) -> (R v S)', 'P <-> ~(R & S)', 'Q <-> ~(P & R)'), '(S & P) -> ~(P v Q)', False),
    (('P -> Q', 'P v ~Q'), 'P <-> Q', True),
    (('(P v Q) -> R', '(R v S) -> ~T'), 'P -> ~T', True),
    (('P -> (Q -> ~P)', 'P <-> Q'), '~P & ~Q', True),
    (('~(P & Q) -> ~(R v S)', '~(P <-> (T v W))', '(R & W) <-> Z'), 'Z -> ~S', True),
]


@pytest.mark.parametrize("premises,conclusion,valid", tests)
def test_hw_problems(premises, conclusion, valid):
    s = Solver()
    for premise in premises:
        s.add_premise(premise)
    s.set_conclusion(conclusion)

    assert s.solve() == valid


s = Solver()
s.add_premise('P <-> Q')
s.add_premise('~Q')
