import RPi.GPIO as GPIO
import time
import random
from neopixel import *

GPIO.setmode(GPIO.BCM)

class Circuit:
	open = 1
	closed = 0

class GPIOSwitch:
	DEFAULT_DEBOUNCE_PERIOD = 0.030

	def __init__(self, pin, debounce_period=DEFAULT_DEBOUNCE_PERIOD):
		self.pin = pin
		GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.debounce_period = debounce_period
		self.debounce_until = 0
		self.__previous_value = None
		self.__previous_time = None
		self.__ignore_until = 0
		self.check(time.time())

	def check(self, timestamp):
		value = GPIO.input(self.pin)
		return self.update(value, timestamp)

	def update(self, value, timestamp):
		# Ignore updates during debounce period
		if timestamp <= self.debounce_until:
			return None
		
		if value == self.__previous_value:
			return None

		if value == Circuit.closed:
			self.debounce_until = timestamp + self.debounce_period

		self.__previous_time = timestamp
		self.__previous_value = value
		return value

class Game:
	LED_OFF = Color(0,0,0)

	def __init__(self):
		self.switches = [
			GPIOSwitch(5),
			GPIOSwitch(6),
			GPIOSwitch(13),
			GPIOSwitch(19),
			GPIOSwitch(26)
		]

		self.lights = Adafruit_NeoPixel(5, 18, 800000, 5, False, 50, 0, ws.WS2811_STRIP_GRB)
		self.startup()

	def startup(self):
		self.lights.begin()

		# Startup light sequence.
		for x in range(5):
			self.lights.setPixelColor(4-x, Color(255,0,255))
			self.lights.show()
			time.sleep(0.1)
			self.lights.setPixelColor(4-x, Game.LED_OFF)
			self.lights.show()

		for x in range(5):
			self.lights.setPixelColor(x, Color(255,0,255))
			self.lights.show()
			time.sleep(0.1)
			self.lights.setPixelColor(x, Game.LED_OFF)
			self.lights.show()

		self.__target = None
		self.target(random.randint(0,4))

	def target(self, button):
		self.clear()
		self.__target = button
		self.lights.setPixelColor(4-button, Color(0, 255, 0))
		self.lights.show()

	def clear(self):
		for x in range(5):
			self.lights.setPixelColor(x, Game.LED_OFF)
		self.lights.show()

	def pressed(self, button):
		if button != self.__target:
			self.lights.setPixelColor(4-button, Color(255, 0, 0))
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


Game().loop()
