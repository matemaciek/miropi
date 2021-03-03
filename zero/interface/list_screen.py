import interface.ui
import interface.icons
from interface.buttons import Command
from interface.ui import ScreenCommand

FONT_W = 6
FONT_H = 9

class ListScreen(interface.ui.Screen):
    def _start(self):
        self._icons = interface.icons.Icons()
        self._cursor = 0
        self._items = self._fill()
        self._N = len(self._items)
        self._draw_all()

    def _fill(self):
        return NotImplemented

    def _icon(self, index):
        return NotImplemented

    def click(self, command):
        if command == Command.UP:
            return self._move_cursor(-1)
        if command == Command.DOWN:
            return self._move_cursor(1)
        return super().click(command)

    def _move_cursor(self, delta):
        self._cursor = (self._cursor + delta) % self._N
        self._draw_all()

    def _draw_all(self):
        self._draw.rectangle((0, 0, self._W, self._H), fill=0)
        dy = int(self._H/3)
        for y in [dy, 2*dy]:
            self._draw.line([0, y, self._W, y], fill=1)

        text_offset = 19
        n = int((self._W - text_offset)/FONT_W)
        for i in [-1, 0, 1]:
            index = self._cursor + i
            if 0 <= index < self._N:
                self._draw.text((text_offset, (i + 1)*dy), self._items[index][:n], fill=1)
                self._draw.text((text_offset, (i + 1)*dy + FONT_H), self._items[index][n:], fill=1)

        self._draw_icon()

    def _subtitle(self):
        return "{}/{}".format(self._cursor + 1, self._N)

    def _draw_icon(self):
        self._draw_image(self._icons.icon(self._icon()), (2, int(self._H/2) - 8))


class IOListScreen(ListScreen):
    def _list_model(self):
        return NotImplemented

    def _fill(self):
        return [input.port for input in self._list_model()]

    def click(self, command):
        if command == Command.ENTER:
            self._list_model()[self._cursor].toggle()
            self._model.save()
            self._draw_icon()
            return
        return super().click(command)

    def _icon(self):
        return "checked" if self._list_model()[self._cursor].enabled else "unchecked"


class InputListScreen(IOListScreen):
    def _list_model(self):
        return self._model.inputs

    def _title(self):
        return "Inputs"


class OutputListScreen(IOListScreen):
    def _list_model(self):
        return self._model.outputs

    def _title(self):
        return "Outputs"
