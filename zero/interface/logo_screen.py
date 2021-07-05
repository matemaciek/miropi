import interface.ui
import interface.patch_screen
import interface.list_screen
import interface.tools
from interface.buttons import Command
from interface.ui import ScreenCommand

class LogoScreen(interface.ui.Screen):
    def _start(self):
        self._icons = interface.icons.Icons()
        logo = interface.tools.resize_keep_ar(self._icons.icon("logo"), self.image.size)
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
