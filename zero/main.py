import asyncio

import interface.buttons
from interface.buttons import Command
import interface.ui
import interface.logo_screen
import interface.debug_screen
import midi.connection
import midi.connections

async def main():
    loop = asyncio.get_event_loop()
    model = midi.connections.Connections()
    screen = interface.ui.ScreenManager(model, [interface.logo_screen.LogoScreen, interface.debug_screen.DebugScreen])
    buttons = interface.buttons.Buttons(
        {
            Command.LEFT: 13,
            Command.RIGHT: 6,
            Command.UP: 26,
            Command.DOWN: 19,
            Command.ENTER: 9,
            Command.BACK: 11,
            Command.OPTION: 5,
        },
        screen.click
    )

    while True:
        await asyncio.sleep(60)

#import logging
#logging.basicConfig(level=logging.DEBUG)
asyncio.run(main(), debug=True)
