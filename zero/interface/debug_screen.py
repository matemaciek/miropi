import interface.ui
from interface.buttons import Command
from interface.ui import ScreenCommand

class DebugScreen(interface.ui.Screen):
    def _start(self):
        self._draw.text((0, 0), "Up: shutdown", fill=1)
        self._draw.text((0, 20), "Middle: reboot", fill=1)
        self._draw.text((0, 40), "Down: restart", fill=1)

    def click(self, command):
        if command == Command.UP:
            return (ScreenCommand.BACK, 0)
        if command == Command.ENTER:
            return (ScreenCommand.BACK, 21)
        if command == Command.DOWN:
            return (ScreenCommand.BACK, 42)
        return super().click(command)
