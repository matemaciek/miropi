from interface.buttons import Command
import interface.patch_screen
import interface.ui
import interface.icons

FONT_W = 6
FONT_H = 9

class ListScreen(interface.ui.Screen):
    def _start(self):
        self._icons = interface.icons.Icons()
        self._title = "Inputs"
        self._cursor = 0
        self._items = [input.port for input in self._model.inputs]
        self._N = len(self._items)
        self._draw_all()

    def click(self, command):
        if command == Command.UP:
            return self._move_cursor(-1)
        if command == Command.DOWN:
            return self._move_cursor(1)
        return interface.patch_screen.PatchScreen

    def _move_cursor(self, delta):
        self._cursor = (self._cursor + delta) % self._N
        self._draw_all()

    def _draw_all(self):
        self._draw.rectangle((0, 0, self._W, self._H), fill=0)
        for x in [0, self._W - 1]:
            self._draw.line([x, 0, x, self._H], fill=1)
        dy = int(self._H/3)
        for y in [0, dy, 2*dy, self._H - 1]:
            self._draw.line([0, y, self._W, y], fill=1)

        text_offset = 19
        n = int((self._W - text_offset)/FONT_W)
        for i in [-1, 0, 1]:
            index = self._cursor + i
            if 0 <= index < self._N:
                self._draw.text((text_offset, (i + 1)*dy), self._items[index][:n], fill=1)
                self._draw.text((text_offset, (i + 1)*dy + FONT_H), self._items[index][n:], fill=1)

        self._draw_image(self._icons.icon("disconnnected"), (2, int(self._H/2) - 8))
        
        self._draw.rectangle((0, 0, len(self._title)*FONT_W, FONT_H), fill=1)
        self._draw.text((1, 0), self._title, fill=0)
        
        index_str = "{}/{}".format(self._cursor + 1, self._N)
        self._draw.rectangle((0, self._H - FONT_H, len(index_str)*FONT_W, self._H), fill=1)
        self._draw.text((1, self._H - FONT_H - 1), index_str, fill=0)

