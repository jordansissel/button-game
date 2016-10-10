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
