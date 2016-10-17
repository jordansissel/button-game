# A way for me to name the states of a GPIO read.
#
# Note: This is only valid for GPIO inputs with a pull-up resistor
# 
# Example, setting up a pin like this:
#
#     import RPi.GPIO as GPIO
#     GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
class Circuit:
	open = 1
	closed = 0
