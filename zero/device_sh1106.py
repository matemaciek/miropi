import luma.oled.device
import luma.core.interface.serial
from interface.buttons import Command

display = luma.oled.device.sh1106(luma.core.interface.serial.spi())
buttons = {
    26: Command.LEFT,
    5: Command.RIGHT,
    19: Command.UP,
    6: Command.DOWN,
    13: Command.ENTER,
    20: Command.ENTER,
    16: Command.BACK,
    21: Command.BACK,
}
