if __name__ == "__main__":
	from neopixel import Color, Adafruit_NeoPixel
	from neopixel import *
	import RPi.GPIO as GPIO
	from game import Game
	Game(color=Color, neopixel=Adafruit_NeoPixel, gpio=GPIO, ws=ws).loop()
