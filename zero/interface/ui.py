import abc
import sys
import PIL.Image
import PIL.ImageDraw
from enum import Enum
from luma.core.virtual import viewport
from luma.core.sprite_system import framerate_regulator

from interface.buttons import Command

class ScreenCommand(Enum):
    SHOW = 0
    BACK = 1
    PREV = 2
    NEXT = 3

FONT_W = 6
FONT_H = 9

regulator = framerate_regulator(fps=25)

class Screen(abc.ABC):
    def __init__(self, model, mode, size):
        self._model = model
        self.image = PIL.Image.new(mode, size)
        self._draw = PIL.ImageDraw.Draw(self.image)
        (self._W, self._H) = size
        self._start()

    def _draw_image(self, image, coord):
        self.image.paste(image, coord)

    def draw_title(self):
        title = self._title()
        subtitle = self._subtitle()
        if title != NotImplemented:
            for x in [0, self._W - 1]:
                self._draw.line([x, 0, x, self._H], fill="white")
            for y in [0, self._H - 1]:
                self._draw.line([0, y, self._W, y], fill="white")
            self._draw.rectangle((0, 0, len(title)*FONT_W + 1, FONT_H), fill="white")
            self._draw.text((1, 0), title, fill=0)
        if subtitle != NotImplemented:
            self._draw.rectangle((0, self._H - FONT_H, len(subtitle)*FONT_W + 1, self._H), fill="white")
            self._draw.text((1, self._H - FONT_H - 1), subtitle, fill=0)

    @abc.abstractmethod
    def _start(self):
        return NotImplemented

    def _title(self):
        return NotImplemented

    def _subtitle(self):
        return NotImplemented

    @abc.abstractmethod
    def click(self, command):
        if command == Command.BACK:
            return (ScreenCommand.BACK, 0)
        if command == Command.LEFT:
            return (ScreenCommand.PREV, None)
        if command == Command.RIGHT:
            return (ScreenCommand.NEXT, None)
        return NotImplemented

class ScreenManager:
    def __init__(self, device, model, start_screens):
        self._model = model
        self._display = device
        self._screen = None
        self._screens = []
        self._indexes = []
        self._show(start_screens)

    def _show(self, screens):
        self._screens.append(screens)
        self._indexes.append(0)
        self._show_screen(0, 1)

    def _back(self, args):
        self._screens.pop()
        self._indexes.pop()
        if len(self._screens) == 0:
            self._exit(args)
        else:
            self._show_screen(0, -1) # thought: keep screen object, not only class? Both here and in left/right (needs new screen method for redraw)

    def _prev(self):
        self._move_screen(-1)

    def _next(self):
        self._move_screen(1)

    def _move_screen(self, delta):
        self._indexes[-1] = (self._indexes[-1] + delta) % len(self._screens[-1])
        self._show_screen(delta, 0)

    def _show_screen(self, xdir, ydir):
        screen = self._screens[-1][self._indexes[-1]]
        old_image = PIL.Image.new(self._display.mode, self._display.size) if self._screen is None else self._screen.image
        self._screen = screen(self._model, self._display.mode, self._display.size)
        self._refresh(old_image, xdir, ydir)

    def _refresh(self, old_image=None, xdir=0, ydir=0):
        self._screen.draw_title()
        if old_image is not None:
            xscale = 1 + abs(xdir)
            yscale = 1 + abs(ydir)
            viewport_w = xscale * self._display.width
            viewport_h = yscale * self._display.height
            merged = PIL.Image.new(self._display.mode, (viewport_w, viewport_h))
            old_pos = (
                int(xdir < 0) * self._display.width,
                int(ydir < 0) * self._display.height
            )
            new_pos = (
                int(xdir > 0) * self._display.width,
                int(ydir > 0) * self._display.height
            )
            merged.paste(old_image, old_pos)
            merged.paste(self._screen.image, new_pos)
            #TODO: persistent viewport
            virtual = viewport(self._display, width=viewport_w, height=viewport_h)
            virtual.set_position(old_pos)
            virtual.display(merged)
            (x, y) = old_pos
            (new_x, new_y) = new_pos
            dx = int((new_x - x) / 5)
            dy = int((new_y - y) / 5)
            while (x, y) != new_pos:
                with regulator:
                    virtual.set_position((x, y))
                x = max(0, min(x + dx, max(new_x, x)))
                y = max(0, min(y + dy, max(new_y, y)))
        self._display.display(self._screen.image)

    def click(self, action):
        click_result = self._screen.click(action)
        if click_result is not None:
            (command, args) = click_result
            if command == ScreenCommand.SHOW:
                return self._show(args)
            if command == ScreenCommand.BACK:
                return self._back(args)
            if command == ScreenCommand.PREV:
                return self._prev()
            if command == ScreenCommand.NEXT:
                return self._next()
        else:
            self._refresh()

    def _exit(self, code=0):
        suffix = " ({})".format(code) if code != 0 else ""
        image = self._screen.image
        draw = PIL.ImageDraw.Draw(image)
        draw.text((100, 50), "Bye!", fill="white")
        if code != 0:
            draw.text((64, 50), "({})".format(code), fill="white")
        self._display.display(image)
        self._display.show()
        sys.exit(code)
