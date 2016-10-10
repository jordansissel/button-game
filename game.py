import time
import random

from circuit import Circuit
from gpio_switch import GPIOSwitch

class Game:
	def __init__(self, color, neopixel, gpio, ws):
		gpio.setmode(gpio.BCM)
		self.Color = color
		self.Neopixel = neopixel
		self.LED_OFF = self.Color(0,0,0)
		self.tick_interval = 0.005

		self.switches = [
			GPIOSwitch(5, gpio),
			GPIOSwitch(6, gpio),
			GPIOSwitch(13, gpio),
			GPIOSwitch(19, gpio),
			GPIOSwitch(26, gpio)
		]

		self.lights = self.Neopixel(5, 18, 800000, 5, False, 50, 0, ws.WS2811_STRIP_GRB)
		self.startup()

	def startup(self):
		self.lights.begin()

		# Startup light sequence.
		for x in range(5):
			self.lights.setPixelColor(4-x, self.Color(255,0,255))
			self.lights.show()
			time.sleep(0.1)
			self.lights.setPixelColor(4-x, self.LED_OFF)
			self.lights.show()

		for x in range(5):
			self.lights.setPixelColor(x, self.Color(255,0,255))
			self.lights.show()
			time.sleep(0.1)
			self.lights.setPixelColor(x, self.LED_OFF)
			self.lights.show()

		self.__target = None
		self.target(random.randint(0,4))

	def target(self, button):
		self.clear()
		self.__target = button
		self.lights.setPixelColor(4-button, self.Color(0, 255, 0))
		self.lights.show()

	def clear(self):
		for x in range(5):
			self.lights.setPixelColor(x, self.LED_OFF)
		self.lights.show()

	def pressed(self, button):
		if button != self.__target:
			self.lights.setPixelColor(4-button, self.Color(255, 0, 0))
			self.lights.show()
		else:
			self.target(random.randint(0,4))

	def loop(self):
		while True:
			timestamp = time.time()
			self.tick(timestamp);
			duration = time.time() - timestamp
			if duration < self.tick_interval:
				time.sleep(self.tick_interval - duration)

	def tick(self, timestamp):
		states = [switch.check(timestamp) for switch in self.switches]
		for i, state in enumerate(states):
			if state == Circuit.open:
				print "%f: Button %d: release" % (timestamp, i)
			elif state == Circuit.closed:
				print "%f: Button %d: pressed" % (timestamp, i)
				self.pressed(i)
