import mock
from board import Board
import pytest

from circuit import Circuit
O = Circuit.open
C = Circuit.closed

@pytest.fixture
def gpio():
	gpio = mock.Mock()
	gpio.setup = mock.Mock()
	gpio.input = mock.Mock(side_effect=[O,C,O,C,C])
	return gpio

def test_events(time, board):
	x = mock.Mock()
	board.bindEvent(Board.SwitchPressed, x)
	board.tick(time.time())
	assert x.called_once
