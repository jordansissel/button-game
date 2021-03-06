import mock
from gpio_switch import GPIOSwitch
from circuit import Circuit
import pytest

O = Circuit.open
C = Circuit.closed

@pytest.fixture
def gpio():
	gpio = mock.Mock()
	gpio.setup = mock.Mock()
	return gpio

def assertStates(gpio, input, output, **kwargs):
	gpio.input = mock.Mock(side_effect=input)
	switch = GPIOSwitch(0, gpio, **kwargs)

	# initial state is read during __init__ of GPIOSwitch
	assert switch.peek() == input[0]

	results = [switch.check(i) for i in range(len(input) - 1)]
	assert results == output

def testCheckReturnsCircuitChanges(gpio):
	assertStates(gpio, [O, O, O, C, C, O], [None, None, C, None, O], debounce_period=0)

def testCheckDebouncing(gpio):
	assertStates(gpio, [O, C, O, C, O], [C, None, None, O], debounce_period=2)
