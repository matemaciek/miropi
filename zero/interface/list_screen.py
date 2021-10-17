import interface.ui
import interface.icons
import interface.config_screen

from interface.buttons import Command
from interface.ui import BKG_D, BKG_L, FNT, FNT_BKG, ScreenCommand, BKG, D

VISIBLE = 5

class ListScreen(interface.ui.Screen):
    def _start(self):
        self._icons = interface.icons.Icons()
        self._cursor = 0
        self._items = self._fill()
        self._N = len(self._items)
        self._draw_all()

    def _fill(self):
        return NotImplemented

    def _icon(self):
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
        self._draw.rectangle((0, 0, self._W, self._H), fill=BKG)
        dy = self._H//VISIBLE
        for (dir, c) in [(-1, BKG_L), (1, BKG_D)]:
            h = (self._H + dir*(dy + D))//2
            self._draw.line([D, h, self._W - D, h], fill=c)

        for i in range(VISIBLE):
            offset = i - VISIBLE//2
            index = self._cursor + offset
            if 0 <= index < self._N:
                self._draw.text((2*D, i*dy + D), self._items[index], **(FNT if offset == 0 else FNT_BKG))

        self._draw_icon()

    def _subtitle(self):
        return "{}/{}".format(self._cursor + 1, self._N)

    def _draw_icon(self):
        self._draw_image(self._icons.icon(self._icon()), (self._W - 32 - 2*D, self._H//2 - 16))


class IOListScreen(ListScreen):
    def _list_model(self):
        return NotImplemented

    def _fill(self):
        return [input.short_name for input in self._list_model()]

    def click(self, command):
        if command == Command.ENTER:
            self._list_model()[self._cursor].toggle()
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


class ConnectionScreen(ListScreen):
    def _fill(self):
        self._connections = self._model.connections()
        return ["{}\n{}".format(self._model.input_name_for_id(src), self._model.output_name_for_id(dst)) for (src, dst) in self._connections]

    def click(self, command):
        if command == Command.ENTER:
            return (ScreenCommand.SHOW, [
                lambda *args: interface.config_screen.NoteFilterScreen(self._connections[self._cursor], *args)
            ])
        return super().click(command)

    def _icon(self):
        return "note_mode_{}".format(self._model.filter(self._connections[self._cursor]).mode.value)

    def _title(self):
        return "Connections"
