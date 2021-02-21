import board
import asyncio
from gpiozero import Button

class All:
    def __init__(self):
        self._buttons = []

    def connect(self, pin, label, action):
        button = Button(pin)
        self._buttons.append(button)
        loop = asyncio.get_event_loop()
        button.when_pressed = lambda: _handle_button(label, action, loop)

def _handle_button(label, action, loop):
    asyncio.run_coroutine_threadsafe(_run_action(action), loop)
    print("Button press:", label)

async def _run_action(action):
    action()
