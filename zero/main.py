import asyncio
import luma.lcd.device
import luma.core.interface.serial

import interface.buttons
import interface.ui
import interface.logo_screen
import interface.debug_screen
import midi.connection
import midi.connections
import device_st7789 as device
#import device_sh1106 as device

def load():
    model = midi.connections.Connections()
    screen = interface.ui.ScreenManager(device.display, model, [interface.logo_screen.LogoScreen, interface.debug_screen.DebugScreen])
    buttons = interface.buttons.Buttons(device.buttons, screen.click)
    return (model, screen, buttons)

async def main():
    (model, screen, buttons) = (None, None, None)

    while True:
        if model is None or model.outdated():
            print("Model outdated, reloading")
            del (model, screen, buttons)
            (model, screen, buttons) = load()
        await asyncio.sleep(5)

#import logging
#logging.basicConfig(level=logging.DEBUG)
asyncio.run(main(), debug=False)
