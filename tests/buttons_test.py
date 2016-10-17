import mock
import pytest
from board import Board
from buttons import Buttons

BUTTON_COUNT = 5

@pytest.fixture
def switches():
	return [mock.Mock() for x in range(BUTTON_COUNT)]

@pytest.fixture
def board(button, time):
	return Board(mock.Mock(), switches, time)

@pytest.fixture
def game(board):
	return Buttons(board)

def test_game_hitting(game, switches, time):
	game.hit = mock.Mock()
	# press all buttons should fire 'hit' at least once.
	for i in range(len(switches)):
		game.pressed(i, time.time())
	assert game.hit.called

def test_game_clear(game, board, time):
	board.setPixelColorRGB = mock.Mock()
	calls = [mock.call(x, 0, 0, 0) for x in range(BUTTON_COUNT)]
	game.clear()
	board.setPixelColorRGB.assert_has_calls(calls)
