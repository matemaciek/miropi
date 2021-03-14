import asyncio
import luma.lcd.device
import luma.core.interface.serial

import interface.buttons
import interface.ui
import interface.logo_screen
import interface.debug_screen
import midi.connection
import midi.connections
import device_sh1106 as device

async def main():
    model = midi.connections.Connections()
    screen = interface.ui.ScreenManager(device.display, model, [interface.logo_screen.LogoScreen, interface.debug_screen.DebugScreen])
    buttons = interface.buttons.Buttons(device.buttons, screen.click)

    while True:
        await asyncio.sleep(60)

#import logging
#logging.basicConfig(level=logging.DEBUG)
asyncio.run(main(), debug=True)
