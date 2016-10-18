# rainbowCycle from https://github.com/jgarff/rpi_ws281x
# small changes made for integration.
def rainbowCycle(board, wait_ms=12, iterations=1):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	pixel_count = board.switch_count()
	sleep = board.time.sleep
	for j in range(256*iterations):
		for i in range(pixel_count):
			#board.setPixelColorRGB(i, *wheel((pixel_count + j + i) & 255))
			board.setPixelColorRGB(i, *wheel(((i * 256 / pixel_count) + j) & 255))

		board.render()
		sleep(wait_ms/1000.0)

# wheel from https://github.com/jgarff/rpi_ws281x
# small changes made for integration.
def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return (pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return (255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return (0, pos * 3, 255 - pos * 3)

def scan(board, red=255, green=0, blue=255):
	sleep = board.time.sleep
	# Startup light sequence.
	for x in range(5):
		board.setPixelColorRGB(4-x,red,green,blue)
		board.render()
		sleep(0.1)
		board.setPixelColorRGB(4-x,0,0,0)
		board.render()

	for x in range(5):
		board.setPixelColorRGB(x,red,green,blue)
		board.render()
		sleep(0.1)
		board.setPixelColorRGB(x,0,0,0) 
		board.render()
