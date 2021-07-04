import luma.lcd.device
import luma.core.interface.serial
from interface.buttons import Command

display = luma.lcd.device.st7789(luma.core.interface.serial.spi(gpio_DC=25, gpio_RST=27, bus_speed_hz=52000000), gpio_LIGHT=24, active_low=False, rotate=1)
buttons = {
    5: Command.LEFT,
    26: Command.RIGHT,
    6: Command.UP,
    19: Command.DOWN,
    13: Command.ENTER,
    20: Command.ENTER,
    16: Command.BACK,
    21: Command.BACK,
}
