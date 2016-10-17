# A debouncing switch.
#
# RPi.GPIO.add_event_detect exists, so why write this?
# I wasn't able to find a way to have RPi.GPIO provide me with edge-triggered
# events for both rising and falling. There's GPIO.add_event_detect(channel,
# GPIO.BOTH, ...) But the callback isn't given the value of the change, so you
# have to do the read yourself and figure out the edge direction (open/close).
# (But, it does support debouncing, which is nice!)
#
# Example use:
#
#       import RPi.GPIO as GPIO
#       import time
#
#       switch = GPIOSwitch(5, GPIO)
#
#       while true:
#           state = switch.check(time.time())
#           if state != None:
#               print "Switch 5 state changed: %s" % state
class GPIOSwitch:
	DEFAULT_DEBOUNCE_PERIOD = 0.030

	def __init__(self, pin, gpio_provider, debounce_period=DEFAULT_DEBOUNCE_PERIOD):
		self.pin = pin
		self.GPIO = gpio_provider
		self.debounce_period = debounce_period
		self.__debounce_until = None

		self.GPIO.setup(self.pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
		self.__previous_value = self.GPIO.input(self.pin)

	def peek(self):
		return self.__previous_value

	# Edge-triggered state checking.
	# If moving from closed -> open, returns open
	# If moving from open -> closed, returns closed
	# If debouncing, returns None
	# If no state change, returns None
	#
	# Argument 'timestamp' should represent the current time as a number. It is
	# used to calculate the end time of debouncing.
	def check(self, timestamp):
		value = self.GPIO.input(self.pin)
		return self.update(value, timestamp)

	def update(self, value, timestamp):
		# Ignore updates during debounce period
		if self.__debounce_until and timestamp <= self.__debounce_until:
			return None
		
		if value == self.__previous_value:
			return None

		self.__debounce_until = timestamp + self.debounce_period
		self.__previous_value = value
		return value
