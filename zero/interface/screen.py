import adafruit_ssd1306
import board
import busio
import PIL.Image
import PIL.ImageDraw

from interface import icons

WIDTH  = 128
HEIGHT = 64

# assumption: WIDTH >= HEIGHT
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

class Screen:
    def __init__(self, model):
        self._model = model
        self._cursor = (0, 0)
        self._cursor_visible = False
        self._icons = icons.Icons(HEIGHT / max(self._model.M, self._model.N))
        self._i2c = busio.I2C(board.SCL, board.SDA)
        self._display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, self._i2c)
        self._image = PIL.Image.new("1", (self._display.width, self._display.height))
        self._draw_desc()
        self._draw_all_tiles()
        self._refresh()

    def move_cursor(self, delta):
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
        self._refresh()

    def click_cursor(self):
        if not self._cursor_visible:
            self._show_cursor()
            return

        self._model.toggle(self._cursor)
        self._draw_desc()
        self._draw_affected_tiles(self._cursor)
        self._refresh()

    def back_cursor(self):
        self._hide_cursor()

    def _show_cursor(self):
        self._cursor_visible = True
        self._draw_desc()
        self._draw_cursor(self._cursor)
        self._refresh()

    def _hide_cursor(self):
        self._cursor_visible = False
        self._draw_desc()
        self._draw_cursor(self._cursor)
        self._refresh()

    def _draw_desc(self):
        (i, j) = self._cursor
        draw = PIL.ImageDraw.Draw(self._image)
        draw.rectangle((0, 0, WIDTH - HEIGHT, HEIGHT), fill=0)
        if not self._cursor_visible:
            return
        input_name = self._model.input_name(i)
        output_name = self._model.output_name(j)
        draw.text((0, 0), input_name[0:10], fill=1)
        draw.text((0, 10), input_name[-10:], fill=1)
        draw.text((0, 43), output_name[0:10], fill=1)
        draw.text((0, 53), output_name[-10:], fill=1)
        if self._model.connected(self._cursor):
            self._draw_icon("connnected", (0, 24))

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
        self._draw_image(self._icons.tile(self._tile(coord)), (WIDTH - HEIGHT + i*self._icons.size, j*self._icons.size))

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

    def _draw_image(self, image, coord):
        self._image.paste(image, coord)

    def _refresh(self):
        self._display.image(self._image)
        self._display.show()

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
