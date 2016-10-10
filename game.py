import time
import random

class Game:
	def __init__(self, color_, neopixel_):
		self.Color = color_
		self.Neopixel = neopixel_
		self.LED_OFF = self.Color(0,0,0)
		self.switches = [
			GPIOSwitch(5),
			GPIOSwitch(6),
			GPIOSwitch(13),
			GPIOSwitch(19),
			GPIOSwitch(26)
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
			self.lights.setPixelColor(4-x, Game.LED_OFF)
			self.lights.show()

		for x in range(5):
			self.lights.setPixelColor(x, self.Color(255,0,255))
			self.lights.show()
			time.sleep(0.1)
			self.lights.setPixelColor(x, Game.LED_OFF)
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
			self.lights.setPixelColor(x, Game.LED_OFF)
		self.lights.show()

	def pressed(self, button):
		if button != self.__target:
			self.lights.setPixelColor(4-button, self.Color(255, 0, 0))
			self.lights.show()
		else:
			self.target(random.randint(0,4))

	def loop(self):
		while True:
			self.tick();

	def tick(self):
		t = time.time()
		states = [switch.check(t) for switch in self.switches]
		for i, state in enumerate(states):
			if state == Circuit.open:
				print "%f: Button %d: release" % (t, i)
			elif state == Circuit.closed:
				print "%f: Button %d: pressed" % (t, i)
				self.pressed(i)
