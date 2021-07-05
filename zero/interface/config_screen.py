import interface.ui
import interface.icons
from interface.buttons import Command
from interface.ui import BKG
from midi.filter import NoteMode

class ConfigScreen(interface.ui.Screen):
    def _start(self):
        self._icons = interface.icons.Icons()
        self._cursor = 0
        self._N = self._len()
        self._draw_all()

    def _len(self):
        return NotImplemented

    def _icon(self, index):
        return NotImplemented

    def _change(self, index, delta):
        return NotImplemented

    def _desc(self):
        return NotImplemented

    def _inactive(self):
        return []

    def click(self, command):
        if command == Command.LEFT:
            cursor = self._prev_active()
            if cursor is not None:
                return self._move_cursor(cursor)
        if command == Command.RIGHT:
            cursor = self._next_active()
            if cursor is not None:
                return self._move_cursor(cursor)
        if command == Command.UP:
            self._change(self._cursor, 1)
            self._draw_all()
            return
        if command == Command.DOWN:
            self._change(self._cursor, -1)
            self._draw_all()
            return
        return super().click(command)

    def _next_active(self):
        cursor = self._cursor + 1
        while cursor < self._N and cursor in self._inactive():
            cursor += 1
        if cursor < self._N:
            return cursor

    def _prev_active(self):
        cursor = self._cursor - 1
        while cursor >= 0 and cursor in self._inactive():
            cursor -= 1
        if cursor >= 0:
            return cursor

    def _move_cursor(self, dst):
        self._cursor = dst
        self._draw_all()

    def _draw_all(self):
        self._draw.rectangle((0, 0, self._W, self._H), fill=BKG)
        for i in range(self._N):
            if not i in self._inactive():
                self._draw_icon(i)
        self._draw_icon_at("up", self._cursor, -1)
        self._draw_icon_at("down", self._cursor, 1)

    def _draw_icon(self, index):
        self._draw_icon_at(self._icon(index), index, 0)

    def _coords_for_icon(self, i, j):
        return (int(self._W/2 - 32*(self._N/2 - i)), int(self._H/2 + 32*j - 16))

    def _draw_icon_at(self, icon, i, j):
        self._draw_image(self._icons.icon(icon), self._coords_for_icon(i, j))

NOTES = ["C ", "C#", "D ", "D#", "E ", "F ", "F#", "G ", "G#", "A ", "A#", "B "]

class NoteFilterScreen(ConfigScreen):
    def __init__(self, connection, *args):
        self._connection = connection
        super().__init__(*args)

    def _start(self):
        filter = self._model.filter(self._connection)
        self._mode = filter.mode
        self._note = filter.note % 12
        self._octave = int(filter.note / 12)
        super()._start()

    def _title(self):
        return "Note filter"

    def _note_str(self):
        return "{}{}".format(NOTES[self._note], self._octave - 1)

    def _subtitle(self):
        if self._mode == NoteMode.ALL:
            return "Pass all notes"
        if self._mode == NoteMode.ABOVE:
            return "Pass from {} up".format(self._note_str())
        if self._mode == NoteMode.BELOW:
            return "Block from {} up".format(self._note_str())
        if self._mode == NoteMode.NONE:
            return "Block all notes"

    def _change(self, index, delta):
        if index == 0:
            self._mode = self._mode.succ() if delta ==1 else self._mode.pred()
        elif index == 1:
            self._note = (self._note + delta) % len(NOTES)
        elif index == 2:
            self._octave = (self._octave + delta) % 11
        self._model.set_filter(self._connection, self._mode, self._octave * 12 + self._note)

    def _len(self):
        return 3

    def _icon(self, index):
        if index == 0:
            return "note_mode_{}".format(self._mode.value)
        if index == 1:
            return "note_{}".format(self._note)
        if index == 2:
            return self._octave - 1

    def _inactive(self):
        if self._mode in [NoteMode.ALL, NoteMode.NONE]:
            return [1, 2]
        return super()._inactive()
