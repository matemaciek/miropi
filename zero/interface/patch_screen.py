import interface.icons
import interface.tools
import interface.ui
from interface.ui import BKG, FNT, FNT_BASE, D
from interface.buttons import Command

D_H_MIN = 96

# /--------------------\
# |                    |
# | tiles(W x (H-D_H)) |
# |                    |
# |--------------------|
# |                    |
# |    desc(W x D_H)   |
# |                    |
# \--------------------/

class Tile:
    def __init__(self, state, state_h, state_v, invert):
        self.state = state
        self.state_h = state_h
        self.state_v = state_v
        self.invert = invert

class PatchScreen(interface.ui.Screen):
    def _start(self):
        self._cursor = (0, 0)
        self._cursor_visible = False
        self._icons = interface.icons.Icons(min(self._W//self._model.M(), (self._H-D_H_MIN)//self._model.N()))
        self._tiles_start = ((self._W - self._model.M() * self._icons.size)//2, 0)
        self._desc_start = (0, self._model.N() * self._icons.size)
        self._draw_desc()
        self._draw_all_tiles()

    def click(self, command):
        if command == Command.ENTER:
            return self._click_cursor()
        if not self._cursor_visible:
            return super().click(command)
        if command == Command.LEFT:
            return self._move_cursor((-1, 0))
        if command == Command.RIGHT:
            return self._move_cursor((1, 0))
        if command == Command.UP:
            return self._move_cursor((0, -1))
        if command == Command.DOWN:
            return self._move_cursor((0, 1))
        if command == Command.BACK:
            return self._back_cursor()

    def _move_cursor(self, delta):
        if not self._cursor_visible:
            self._show_cursor()
            return
        
        (dx, dy) = delta
        old_cursor = self._cursor
        self._cursor = (
            (self._cursor[0] + dx) % self._model.M(),
            (self._cursor[1] + dy) % self._model.N()
        )
        self._draw_desc()
        self._draw_cursor(old_cursor)
        self._draw_cursor(self._cursor)

    def _click_cursor(self):
        if not self._cursor_visible:
            self._show_cursor()
            return

        self._model.toggle(self._cursor)
        self._draw_desc()
        self._draw_affected_tiles(self._cursor)

    def _back_cursor(self):
        self._hide_cursor()

    def _show_cursor(self):
        self._cursor_visible = True
        self._draw_desc()
        self._draw_cursor(self._cursor)

    def _hide_cursor(self):
        self._cursor_visible = False
        self._draw_desc()
        self._draw_cursor(self._cursor)

    def _draw_desc(self):
        (i, j) = self._cursor
        self._draw.rectangle((self._desc_start, (self._W, self._H)), fill=BKG)
        desc_h = self._H - self._desc_start[1]
        if not self._cursor_visible:
            self._draw_image(interface.tools.resize_keep_ar(self._icons.icon("logo"), (self._W, desc_h)), self._desc_start)
            return
        input_name = self._model.input_name(i)
        output_name = self._model.output_name(j)
        self._draw.text((self._desc_start[0] + D, self._desc_start[1] + D), input_name, **FNT)
        (_, box_h) = self._draw.textsize(output_name, **FNT_BASE)
        self._draw.text((D, self._H - box_h - D), output_name, **FNT)
        icon = "connected" if self._model.connected(self._cursor) else "disconnected"
        self._draw_icon(icon, (self._W//2 - 16, self._desc_start[1] + desc_h//2 - 16))

    def _draw_cursor(self, cursor):
        self._draw_tile(cursor)

    def _tile(self, coord):
        return Tile(
            self._state(coord),
            self._state_h(coord),
            self._state_v(coord),
            self._cursor == coord and self._cursor_visible
        )

    def _draw_tile(self, coord):
        (i, j) = coord
        self._draw_image(self._icons.tile(self._tile(coord)), (self._tiles_start[0] + i*self._icons.size, self._tiles_start[1] + j*self._icons.size))

    def _draw_all_tiles(self):
        for x in range(0, self._model.M()):
            for y in range(0, self._model.N()):
                self._draw_tile((x, y))

    def _draw_affected_tiles(self, coord):
        (i, j) = coord
        for x in range(i, self._model.M()):
            self._draw_tile((x, j))
        for y in range(0, j):
            self._draw_tile((i, y))

    def _draw_icon(self, name, coord):
        self._draw_image(self._icons.icon(name), coord)

    def _state(self, coord):
        return "on" if self._model.connected(coord) else "off"

    def _state_h(self, coord):
        (i, j) = coord
        for x in range(0, i):
            if self._model.connected((x, j)):
                return 'H'
        return 'h'

    def _state_v(self, coord):
        (i, j) = coord
        for y in range(j+1, self._model.N()):
            if self._model.connected((i, y)):
                return 'V'
        return 'v'
