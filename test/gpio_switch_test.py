import unittest
from mock import Mock
from gpio_switch import GPIOSwitch
from circuit import Circuit

O = Circuit.open
C = Circuit.closed

class TestGPIOSwitch(unittest.TestCase):
	def setUp(self):
		self.mock_gpio = Mock()

	def assertStates(self, input, output, **kwargs):
		self.mock_gpio.input = Mock(side_effect = input)
		switch = GPIOSwitch(0, self.mock_gpio, **kwargs)
		self.assertEqual(switch.peek(), input[0])
		results = [switch.check(i) for i in range(len(input) - 1)]
		self.assertEqual(results, output)


	def testCheckReturnsCircuitChanges(self):
		self.assertStates([O, O, O, C, C, O], [None, None, C, None, O], debounce_period=0)

	def testCheckDebouncing(self):
		self.assertStates([O, C, O, C, O], [C, None, None, O], debounce_period=2)
