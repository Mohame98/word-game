from pytest import fixture
from letter_state import LetterState, WordState


@fixture
def letter_state():
    return LetterState('hello')


@fixture
def word_state():
    return WordState(['hello'], ['hello'])


def test_color_change(letter_state):
    colors = []
    letter_state.color_change([['h', 'e', 'l', 'l', 'o']], colors)
    assert colors == [['green', 'green', 'green', 'green', 'green']]


def test_is_valid_guess(word_state):
    assert word_state.is_valid_guess([['h', 'e', 'l', 'l', 'o']]) == True
    assert word_state.is_valid_guess([['h', 'h', 'h', 'l', 'o']]) == False


def test_is_winning_guess(word_state):
    assert word_state.is_winning_guess([['h', 'o', 'm', 'e', 's']]) == False