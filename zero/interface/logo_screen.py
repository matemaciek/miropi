import PIL.Image

import interface.ui
import interface.patch_screen
import interface.list_screen
from interface.buttons import Command
from interface.ui import ScreenCommand

class LogoScreen(interface.ui.Screen):
    def _start(self):
        self._draw_image(PIL.Image.open("miropi.png").convert("1"), (0, 0))

    def click(self, command):
        if command == Command.ENTER:
            return (ScreenCommand.SHOW, [
                interface.patch_screen.PatchScreen,
                interface.list_screen.ConnectionScreen,
                interface.list_screen.InputListScreen,
                interface.list_screen.OutputListScreen
            ])
        return super().click(command)
