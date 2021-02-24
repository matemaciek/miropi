import adafruit_ssd1306
import board
import busio
import abc
import sys
import PIL.Image
import PIL.ImageDraw
from enum import Enum

from interface.buttons import Command

class ScreenCommand(Enum):
    SHOW = 0
    BACK = 1
    PREV = 2
    NEXT = 3

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
        if command == Command.BACK:
            return (ScreenCommand.BACK, None)
        if command == Command.LEFT:
            return (ScreenCommand.PREV, None)
        if command == Command.RIGHT:
            return (ScreenCommand.NEXT, None)
        return NotImplemented

class ScreenManager:
    def __init__(self, model, start_screens):
        self._model = model
        self._i2c = busio.I2C(board.SCL, board.SDA)
        self._display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, self._i2c)
        self._image = PIL.Image.new("1", (self._display.width, self._display.height))
        self._draw = PIL.ImageDraw.Draw(self._image)
        self._screens = []
        self._indexes = []
        self._show(start_screens)

    def _show(self, screens):
        self._screens.append(screens)
        self._indexes.append(0)
        self._show_screen()

    def _back(self):
        self._screens.pop()
        self._indexes.pop()
        if len(self._screens) == 0:
            self._exit()
        else:
            self._show_screen() # thought: keep screen object, not only class? Both here and in left/right (needs new screen method for redraw)

    def _prev(self):
        self._move_screen(-1)

    def _next(self):
        self._move_screen(1)

    def _move_screen(self, delta):
        self._indexes[-1] = (self._indexes[-1] + delta) % len(self._screens[-1])
        self._show_screen()

    def _show_screen(self):
        screen = self._screens[-1][self._indexes[-1]]
        self._draw.rectangle((0, 0, WIDTH, HEIGHT), fill=0)
        self._screen = screen(self._model, self._image, self._draw)
        self._refresh()

    def _refresh(self):
        self._display.image(self._image)
        self._display.show()

    def click(self, action):
        click_result = self._screen.click(action)
        if click_result is not None:
            (command, args) = click_result
            if command == ScreenCommand.SHOW:
                return self._show(args)
            if command == ScreenCommand.BACK:
                return self._back()
            if command == ScreenCommand.PREV:
                return self._prev()
            if command == ScreenCommand.NEXT:
                return self._next()
        else:
            self._refresh()

    def _exit(self):
        self._draw.text((100, 50), "Bye!", fill=1)
        self._refresh()
        sys.exit(0)
