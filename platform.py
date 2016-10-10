class Neopixel:
    @staticmethod
    def instance():
        import neopixel
        return neopixel

class GPIO:
    @staticmethod
    def instance():
        import RPi.GPIO as gpio
        return gpio

class Color:
    @staticmethod
    def instance():
        from neopixel import Color as color
        return color
