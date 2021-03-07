import asyncio
import luma.oled.device
import luma.core.interface.serial

import interface.buttons
from interface.buttons import Command
import interface.ui
import interface.logo_screen
import interface.debug_screen
import midi.connection
import midi.connections

async def main():
    loop = asyncio.get_event_loop()
    device = luma.oled.device.sh1106(luma.core.interface.serial.spi())
    model = midi.connections.Connections()
    screen = interface.ui.ScreenManager(device, model, [interface.logo_screen.LogoScreen, interface.debug_screen.DebugScreen])
    buttons = interface.buttons.Buttons(
        {
            26: Command.LEFT,
            5: Command.RIGHT,
            19: Command.UP,
            6: Command.DOWN,
            13: Command.ENTER,
            20: Command.ENTER,
            16: Command.BACK,
            21: Command.BACK,
        },
        screen.click
    )

    while True:
        await asyncio.sleep(60)

#import logging
#logging.basicConfig(level=logging.DEBUG)
asyncio.run(main(), debug=True)
