import asyncio

import interface.buttons
from interface.buttons import Command
import interface.ui
import interface.logo_screen
import midi.connection
import midi.connections

async def main():
    loop = asyncio.get_event_loop()
    model = midi.connections.Connections()
    screen = interface.ui.ScreenManager(model, interface.logo_screen.LogoScreen)
    buttons = interface.buttons.Buttons(
        {
            Command.LEFT: 27,
            Command.RIGHT: 11,
            Command.UP: 9,
            Command.DOWN: 22,
            Command.ENTER: 10,
            Command.BACK: 17,
        },
        screen.click
    )

    while True:
        await asyncio.sleep(60)

asyncio.run(main(), debug=True)
