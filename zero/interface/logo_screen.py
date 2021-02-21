import interface.ui
import interface.patch_screen
import PIL.Image

class LogoScreen(interface.ui.Screen):
    def _start(self):
        self._draw_image(PIL.Image.open("miropi.png").convert("1"), (0, 0))

    def click(self, command):
        return interface.patch_screen.PatchScreen
