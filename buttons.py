import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class Circuit(object):
	open = 1
	closed = 1

class GPIOSwitch:
	DEFAULT_DEBOUNCE_PERIOD = 0.010

	def __init__(self, pin, debounce_period=DEFAULT_DEBOUNCE_PERIOD):
		self.pin = pin
		GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.debounce_period = debounce_period
		self.debounce_until = 0
		self.__previous_value = None
		self.__previous_time = None
		self.__ignore_until = 0
		self.check()

	def check(self):
		value = GPIO.input(self.pin)
		return self.update(value, time.time())

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

switches = [
	GPIOSwitch(26),
	GPIOSwitch(19),
	GPIOSwitch(13),
	GPIOSwitch(6),
	GPIOSwitch(5)
]

while True:
	for i, switch in enumerate(switches):
		state = switch.check()
		if state != None:
			print "Button %d: %d" % (i, state)
