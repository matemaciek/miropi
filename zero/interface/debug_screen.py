import interface.ui
from interface.buttons import Command
from interface.ui import ScreenCommand

class DebugScreen(interface.ui.Screen):
    def _start(self):
        self._draw.text((10, 10), "Up:  shutdown", fill=1)
        self._draw.text((10, 20), "Enter: reboot", fill=1)
        self._draw.text((10, 30), "Down: restart", fill=1)

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
