import interface.ui
from interface.buttons import Command
from interface.ui import ScreenCommand, BKG, FNT, FNT_BASE, D

class DebugScreen(interface.ui.Screen):
    def _start(self):
        self._draw.rectangle((0, 0, self._W, self._H), fill=BKG)
        text = "Up:  shutdown\nEnter: reboot\nDown: restart"
        (box_x, box_y) = self._draw.textsize(text, **FNT_BASE)
        self._draw.text(((self._W - box_x)//2, (self._H - box_y)//2), text, **FNT)

    def click(self, command):
        if command == Command.UP:
            return (ScreenCommand.BACK, 0)
        if command == Command.ENTER:
            return (ScreenCommand.BACK, 21)
        if command == Command.DOWN:
            return (ScreenCommand.BACK, 42)
        return super().click(command)

    def _title(self):
        return "Power"
