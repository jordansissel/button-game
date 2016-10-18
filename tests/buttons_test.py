import mock
import pytest
from board import Board
from buttons import Buttons

import random

# Randomize number of buttons.
# The real game board has 5... for now...
BUTTON_COUNT = random.randint(1,30)

@pytest.fixture
def switches():
	return [mock.Mock() for x in range(BUTTON_COUNT)]

@pytest.fixture
def board(lights, switches, time):
	return Board(lights, switches, time)

@pytest.fixture
def lights():
	lights = mock.Mock()
	lights.numPixels = mock.Mock(return_value=BUTTON_COUNT)
	return lights

@pytest.fixture
def game(board):
	return Buttons(board)

def test_game_hitting(game, switches, time):
	game.hit = mock.Mock()
	# press all buttons should fire 'hit' at least once.
	for i in range(len(switches)):
		game.press(i, time.time())
	game.hit.assert_called()

def test_game_missing(game, switches, time):
	game.target(0)
	# Skip first button which is the current target.
	for i in range(1,len(switches)):
		game.board.setPixelColorRGB = mock.Mock()
		game.press(i, time.time())

		# I wired the LEDs backwards. Oops.
		game.board.setPixelColorRGB.assert_called_with(game.board.pixel(i), 255, 0, 0)

def test_game_clear(game, board, time):
	board.setPixelColorRGB = mock.Mock()
	calls = [mock.call(x, 0, 0, 0) for x in range(BUTTON_COUNT)]
	game.clear()
	board.setPixelColorRGB.assert_has_calls(calls)

# Test that 3 quick hits will result in a rainbow splash
def test_game_3hit(game, board, time):
	game.target(0)
	game.press(0, time.time())

	game.target(0)
	game.press(0, time.time())

	board.setPixelColorRGB = mock.Mock()
	game.target(0)
	game.press(0, time.time())

	# Rainbow will set the pixel color lots and lots of times.
	assert len(board.setPixelColorRGB.mock_calls) > board.switch_count()*120

# Test that 3 hits not within the 3-second time frame
# will not result in a rainbow.
def test_game_3hit_timedout(game, board, time):
	game.target(0)
	game.hit(0, time.time())
	game.hit(0, time.time())
	board.setPixelColorRGB = mock.Mock()
	time.time() # skip a tick.
	game.hit(0, time.time())

	assert len(board.setPixelColorRGB.mock_calls) < board.switch_count()*2 
