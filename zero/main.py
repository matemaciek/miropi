import asyncio

import interface.buttons
import interface.screen
import midi.connection
import midi.connections

async def main():
    loop = asyncio.get_event_loop()
    model = midi.connections.Connections()
    screen = interface.screen.Screen(model)
    buttons = interface.buttons.All()

    buttons.connect(9, "Up", lambda: screen.move_cursor((0,-1)))
    buttons.connect(10, "Enter", screen.click_cursor)
    buttons.connect(11, "Right", lambda: screen.move_cursor((1,0)))
    buttons.connect(17, "Back", screen.back_cursor)
    buttons.connect(22, "Down", lambda: screen.move_cursor((0,1)))
    buttons.connect(27, "Left", lambda: screen.move_cursor((-1,0)))

    while True:
        await asyncio.sleep(60)

asyncio.run(main())
