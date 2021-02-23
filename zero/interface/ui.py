import adafruit_ssd1306
import board
import busio
import abc
import sys
import PIL.Image
import PIL.ImageDraw

WIDTH  = 128
HEIGHT = 64

class Screen(abc.ABC):
    def __init__(self, model, image, draw):
        self._model = model
        self._image = image
        self._draw = draw
        (self._W, self._H) = self._image.size
        self._start()

    def _draw_image(self, image, coord):
        self._image.paste(image, coord)

    @abc.abstractmethod
    def _start(self):
        return NotImplemented

    @abc.abstractmethod
    def click(self, command):
        return NotImplemented

class ScreenManager:
    def __init__(self, model, start_screen):
        self._model = model
        self._i2c = busio.I2C(board.SCL, board.SDA)
        self._display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, self._i2c)
        self._image = PIL.Image.new("1", (self._display.width, self._display.height))
        self._draw = PIL.ImageDraw.Draw(self._image)
        self._show(start_screen)

    def _show(self, screen):
        self._draw.rectangle((0, 0, WIDTH, HEIGHT), fill=0)
        self._screen = screen(self._model, self._image, self._draw)
        self._refresh()

    def _refresh(self):
        self._display.image(self._image)
        self._display.show()

    def click(self, action):
        new_screen = self._screen.click(action)
        if new_screen == -1:
            self.exit()
        if new_screen is not None:
            self._show(new_screen)
        else:
            self._refresh()

    def exit(self):
        self._draw.text((100, 50), "Bye!", fill=1)
        self._refresh()
        sys.exit(0)
