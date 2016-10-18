import time
import random

from reactor import Reactor
from circuit import Circuit
from gpio_switch import GPIOSwitch
import colorutils

class PixelProblem(Exception):
	pass

# A board for the game.
#
# The board is a sequence of pairs of buttons and RGB LEDs.
class Board:
	SwitchPress = Reactor.event()
	SwitchRelease = Reactor.event()

	def __init__(self, lights, switches, reactor, time=time):
		self.time = time
		self.lights = lights
		self.reactor = reactor
		self.switches = switches
		self.startup()
		self.tick_interval = 0.01

	def switch_count(self):
		return len(self.switches)

	def pixel(self, button):
		# The pixel addresses are in reverse order.
		# Zero is the end of the LED strip.
		return (self.switch_count() - button - 1)

	def startup(self):
		colorutils.scan(self)

	def setPixelColorRGB(self, index, red, green, blue):
		#print("setPixelColorRGB(%d, %d, %d, %d)"  % (index, red, green, blue))
		if index < 0:
			raise PixelProblem("Pixel %d is invalid" % index)
		self.lights.setPixelColorRGB(index, red, green, blue)

	def render(self):
		self.lights.show()
	def loop(self):
		while True:
			timestamp = self.time.time()
			self.tick(timestamp);
			duration = self.time.time() - timestamp
			if duration < self.tick_interval:
				self.time.sleep(self.tick_interval - duration)

	def tick(self, timestamp):
		states = [switch.check(timestamp) for switch in self.switches]
		for i, state in enumerate(states):
			if state == Circuit.open:
				self.reactor.call(Board.SwitchRelease, i, timestamp)
			elif state == Circuit.closed:
				print "%f: Button %d: pressed" % (timestamp, i)
				self.reactor.call(Board.SwitchPress, i, timestamp)
