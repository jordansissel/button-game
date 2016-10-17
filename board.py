import time
import random

from circuit import Circuit
from gpio_switch import GPIOSwitch
import colorutils

# A board for the game.
#
# The board is a sequence of pairs of buttons and RGB LEDs.
class Board:
	SwitchPressed = 1

	def __init__(self, lights, switches, time=time):
		self.time = time
		self.lights = lights
		self.switches = switches
		self.hooks = dict()
		self.startup()

	def switch_count(self):
		return len(self.switches)

	def pixel(self, button):
		# The pixel addresses are in reverse order.
		# Zero is the end of the LED strip.
		return (self.switch_count() - button - 1)

	def startup(self):
		colorutils.scan(self.lights, self.time.sleep)

	def setPixelColorRGB(self, index, red, green, blue):
		self.lights.setPixelColorRGB(index, red, green, blue)

	def render(self):
		self.lights.show()

	def hook(self, event, callback):
		hooks = self.hooks.setdefault(event, [])
		hooks.append(callback)

	def unhook(self, event, callback):
		hooks = self.hooks.setdefault(event, [])
		if callback in hooks:
			hooks.remove(callback)

	def callhook(self, event, *args, **kwargs):
		hooks = self.hooks.setdefault(event, [])
		for hook in hooks:
			hook.call(*args, **kwargs)

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
				print "%f: Button %d: release" % (timestamp, i)
			elif state == Circuit.closed:
				print "%f: Button %d: pressed" % (timestamp, i)
				self.callhook(Board.SwitchPressed, i, timestamp)
