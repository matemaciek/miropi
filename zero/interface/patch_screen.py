import PIL.Image

import interface.icons
import interface.ui
from interface.buttons import Command
from interface.ui import ScreenCommand

# assumption: W >= H
#
# /---------------|------------\
# |               |            |
# | desc(W-H x H) |tiles(H x H)|
# |               |            |
# \---------------|------------/

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
        self._icons = interface.icons.Icons(self._H / max(self._model.M, self._model.N))
        self.R_W = self._model.M * self._icons.size
        self.L_W = self._W - self.R_W
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
            (self._cursor[0] + dx) % self._model.M,
            (self._cursor[1] + dy) % self._model.N
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
        self._draw.rectangle((0, 0, self.L_W - 1, self._H), fill=0)
        #draw.line((self.L_W - 1, 0, self.L_W - 1, self.R_W), fill=1)
        #draw.line((self.L_W - 1, self.R_W, self.L_W + self.R_W, self.R_W), fill=1)
        if not self._cursor_visible:
            self._draw_image(PIL.Image.open("miropi.png").convert("1").resize((int(self._W/2), int(self._H/2))), (0, int(self._H/4)))
            return
        max_l = int(self.L_W/6)
        input_name = self._model.input_name(i)
        output_name = self._model.output_name(j)
        self._draw.text((0, 0), input_name[0:max_l-2]+"..", fill=1)
        self._draw.text((0, 10), ".."+input_name[-max_l+2:], fill=1)
        self._draw.text((0, 43), output_name[0:max_l-2]+"..", fill=1)
        self._draw.text((0, 53), ".."+output_name[-max_l+2:], fill=1)
        icon = "connected" if self._model.connected(self._cursor) else "disconnected"
        self._draw_icon(icon, (int(self.L_W/2) - 8, int(self._H/2) - 8))

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
        self._draw_image(self._icons.tile(self._tile(coord)), (self.L_W + i*self._icons.size, j*self._icons.size))

    def _draw_all_tiles(self):
        for x in range(0, self._model.M):
            for y in range(0, self._model.N):
                self._draw_tile((x, y))

    def _draw_affected_tiles(self, coord):
        (i, j) = coord
        for x in range(i, self._model.M):
            self._draw_tile((x, j))
        for y in range(0, self._model.N):
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
        for y in range(j+1, self._model.N):
            if self._model.connected((i, y)):
                return 'V'
        return 'v'
