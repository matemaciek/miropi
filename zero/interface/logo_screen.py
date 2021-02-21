import PIL.Image

import interface.ui
import interface.patch_screen
from interface.buttons import Command

class LogoScreen(interface.ui.Screen):
    def _start(self):
        self._draw_image(PIL.Image.open("miropi.png").convert("1"), (0, 0))

    def click(self, command):
        if command == Command.BACK:
            return -1
        return interface.patch_screen.PatchScreen
