import time
import random

from circuit import Circuit
from gpio_switch import GPIOSwitch
import colorutils

class Board:
	SwitchPressed = 1

	def __init__(self, lights, switches, time=time):
		self.time = time
		self.lights = lights
		self.switches = switches
		self.bindings = dict()
		self.startup()

	def startup(self):
		colorutils.scan(self.lights, self.time.sleep)

	def setPixelColorRGB(self, index, red, gree, blue):
		self.lights.setPixelColorRGB(index, red, green, blue)

	def render(self):
		self.lights.show()

	def bindEvent(self, event, callback):
		bindings = self.bindings.setdefault(event, [])
		bindings.append(callback)

	def unbindEvent(self, event, callback):
		bindings = self.bindings.setdefault(event, [])
		if callback in bindings:
			bindings.remove(callback)

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
				for callback in self.bindings.get(Board.SwitchPressed, []):
					callback(i, timestamp)
