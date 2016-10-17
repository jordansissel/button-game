import mock
import pytest
from gpio_switch import GPIOSwitch
from board import Board

@pytest.fixture(scope="module")
def time():
	time = mock.Mock()
	time.time = mock.Mock(side_effect=range(1000))
	time.sleep = mock.Mock()
	return time

@pytest.fixture
def button(gpio=mock.Mock()):
	return GPIOSwitch(0, gpio, 1)

@pytest.fixture
def board(button, time):
	return Board(mock.Mock(), [button], time)


