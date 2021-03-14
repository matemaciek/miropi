import PIL.Image

import interface.ui
import interface.patch_screen
import interface.list_screen
import interface.tools
from interface.buttons import Command
from interface.ui import ScreenCommand

class LogoScreen(interface.ui.Screen):
    def _start(self):
        logo = interface.tools.resize_keep_ar(PIL.Image.open("miropi.png").convert(self.image.mode), self.image.size)
        self._draw_image(logo, (0, 0))

    def click(self, command):
        if command == Command.ENTER:
            return (ScreenCommand.SHOW, [
                interface.patch_screen.PatchScreen,
                interface.list_screen.ConnectionScreen,
                interface.list_screen.InputListScreen,
                interface.list_screen.OutputListScreen
            ])
        return super().click(command)
