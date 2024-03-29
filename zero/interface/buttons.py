import asyncio
import time
from gpiozero import Button
from enum import Enum

class Command(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    ENTER = 4
    BACK = 5

class Buttons:
    def __init__(self, mapping, action):
        self._buttons = []
        for key in mapping.keys():
            self._connect(key, mapping[key], action)
            time.sleep(0.1)

    def _connect(self, pin, command, action):
        button = Button(pin)
        self._buttons.append(button)
        loop = asyncio.get_event_loop()
        button.when_pressed = lambda: _handle_button(command, action, loop)

def _handle_button(command, action, loop):
    print("Button press:", command)
    loop.call_soon_threadsafe(asyncio.ensure_future, _run_action(action, command))

async def _run_action(action, command):
    action(command)
