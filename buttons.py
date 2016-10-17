from board import Board

class Buttons:
	def __init__(self, board):
		self.board = board
		self.tick_interval = 0.005
		self.board.registerCallback(Board.SwitchPressed, self.pressed)

	def target(self, button):
		self.clear()
		self.__target = button
		self.board.setPixelColorRGB(4-button, 0, 255, 0)
		self.board.render()

	def clear(self):
		for x in range(5):
			self.board.setPixelColorRGB(x, 0, 0, 0)
		self.board.show()

	def pressed(self, button, timestamp):
		if button != self.__target:
			self.missed(button, timestamp)
		else:
			self.hit(button, timestamp)

	def missed(self, button, timestamp):
		self.board.setPixelColorRGB(4-button, 255, 0, 0)
		self.board.show()
		self.wins = []

	def hit(self, button, timestamp):
		self.wins = self.wins + [timestamp]
		if len(self.wins) >= 3 and (timestamp - self.wins[0]) < 3:
			colorutils.rainbowCycle(self.board, self.Color)
			self.wins = []
		self.target(random.randint(0,4))

if __name__ == "__main__":
	from neopixel import Color, Adafruit_NeoPixel
	from neopixel import *
	import RPi.GPIO as GPIO
	GPIO.setmode(gpio.BCM)

	switches = [
		GPIOSwitch(5, GPIO),
		GPIOSwitch(6, GPIO),
		GPIOSwitch(13, GPIO),
		GPIOSwitch(19, GPIO),
		GPIOSwitch(26, GPIO)
	]

	lights = Adafruit_Neopixel(len(self.switches), 18, 800000, 5, False, 50, 0, ws.WS2811_STRIP_GRB)
	lights.begin()

	board = Board(lights, switches)
	buttons = Buttons(board)
	buttons.run()
