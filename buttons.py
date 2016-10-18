import colorutils
import random
from board import Board

class Buttons:
	Miss = 1000
	Hit  = 1001

	def __init__(self, board):
		self.board = board
		self.time = self.board.time
		self.tick_interval = 0.005
		self.board.hook(Board.SwitchPressed, self.pressed)
		self.target(random.randint(0, self.board.switch_count() - 1))
		self.wins = []
		self.setup()

	def setup(self):
		ThreeWins(self.board)

	def target(self, button):
		assert button >= 0
		assert button < self.board.switch_count()
		self.clear()
		self.__target = button
		self.board.setPixelColorRGB(self.board.pixel(button), 0, 255, 0)
		self.board.render()

	def clear(self):
		for x in range(self.board.switch_count()):
			self.board.setPixelColorRGB(x, 0, 0, 0)
		self.board.render()

	def pressed(self, button, timestamp):
		assert button >= 0
		assert button < self.board.switch_count()
		if button != self.__target:
			self.missed(button, timestamp)
		else:
			self.hit(button, timestamp)

	def missed(self, button, timestamp):
		assert button >= 0
		assert button < self.board.switch_count()
		self.board.callhook(Buttons.Miss, button, timestamp)

		self.board.setPixelColorRGB(self.board.pixel(button), 255, 0, 0)
		self.board.render()

	def hit(self, button, timestamp):
		assert button >= 0
		assert button < self.board.switch_count()
		self.board.callhook(Buttons.Hit, button, timestamp)

		self.target(random.randint(0, self.board.switch_count() - 1))

class ThreeWins:
	def __init__(self, board):
		board.hook(Buttons.Hit, self.hit)
		board.hook(Buttons.Miss, self.miss)
		self.reset()
		self.board = board
	
	def hit(self, button, timestamp):
		self.hits.append(timestamp)
		if len(self.misses) == self.board.switch_count() - 1:
			colorutils.scan(self.board, random.randint(50,255), random.randint(50,255), random.randint(50,255))
			colorutils.scan(self.board, random.randint(50,255), random.randint(50,255), random.randint(50,255))

			self.reset()
		if len(self.hits) >= 3 and (timestamp - self.hits[0]) < 3:
			colorutils.rainbowCycle(self.board)
			self.reset()

	def reset(self):
		self.hits = []
		self.misses = dict()

	def miss(self, button, timestamp):
		self.misses[button] = timestamp

if __name__ == "__main__":
	from neopixel import Adafruit_NeoPixel, ws
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	from gpio_switch import GPIOSwitch

	switches = [
		GPIOSwitch(5, GPIO),
		GPIOSwitch(6, GPIO),
		GPIOSwitch(13, GPIO),
		GPIOSwitch(19, GPIO),
		GPIOSwitch(26, GPIO)
	]

	lights = Adafruit_NeoPixel(len(switches), 18, 800000, 5, False, 50, 0, ws.WS2811_STRIP_GRB)
	lights.begin()

	board = Board(lights, switches)
	buttons = Buttons(board)
	board.loop()
