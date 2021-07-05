import PIL.Image
import PIL.ImageOps

def _compile(data, size, invert):
    if type(data) is dict:
        return {k:_compile(v, size, invert) for (k, v) in data.items()}
    if data[-4:] == ".png":
        im = PIL.Image.open("icons/" + data)
        if not invert:
            return PIL.Image.open("icons/" + data)
        return PIL.ImageOps.invert(im.convert('RGB'))
    if invert:
        byte_array = bytearray(data)
        for index in range(len(byte_array)):
            byte_array[index] ^= 0xFF
        data = bytes(byte_array)
    return PIL.Image.frombytes("1", (size, size), data)

class Icons:
    def __init__(self, max_size=None):
        if max_size is not None:
            self.size = sorted([s for s in _raw_tiles.keys() if s <= max_size])[-1]
            self._tiles = {
                False: _compile(_raw_tiles[self.size], self.size, False),
                True: _compile(_raw_tiles[self.size], self.size, True)
            }
        self._icons = {
            False: _compile(_raw_icons, 16, False),
            True: _compile(_raw_icons, 16, True)
        }

    def icon(self, name, invert=False):
        return self._icons[invert][name]

    def tile(self, tile):
        return self._tiles[tile.invert][tile.state][tile.state_h][tile.state_v]

_raw_icons = {
    "logo": "miropi.png",
    -1: "-1.png",
    0: "0.png",
    1: "1.png",
    2: "2.png",
    3: "3.png",
    4: "4.png",
    5: "5.png",
    6: "6.png",
    7: "7.png",
    8: "8.png",
    9: "9.png",
    "note_0": "note-0.png",
    "note_1": "note-1.png",
    "note_2": "note-2.png",
    "note_3": "note-3.png",
    "note_4": "note-4.png",
    "note_5": "note-5.png",
    "note_6": "note-6.png",
    "note_7": "note-7.png",
    "note_8": "note-8.png",
    "note_9": "note-9.png",
    "note_10": "note-10.png",
    "note_11": "note-11.png",
    "note_mode_0": "note-all.png",
    "note_mode_1": "note-above.png",
    "note_mode_2": "note-below.png",
    "note_mode_3": "note-none.png",
    "up": "up.png",
    "down": "down.png",
    "connected": "connected.png",
    "disconnected": "disconnected.png",
    "checked": "checked.png",
    "unchecked": "unchecked.png"
}

_raw_tiles = {
    3: {
        "off": {
            "h": {
                "v": b"\x00\x00\x00",
                "V": b"\x40\x40\x40"
            },
            "H": {
                "v": b"\x00\xE0\x00",
                "V": b"\x00\xE0\x00"
            }
        },
        "on": {
            "h": {
                "v": b"\x40\x60\x00",
                "V": b"\x40\x60\x40"
            },
            "H": {
                "v": b"\x40\xE0\x00",
                "V": b"\x40\xE0\x40"
            }
        }
    },
    5: {
        "off": {
            "h": {
                "v": b"\x00\x00\x00\x00\x00",
                "V": b"\x20\x20\x20\x20\x20"
            },
            "H": {
                "v": b"\x00\x00\xF8\x00\x00",
                "V": b"\x20\x00\xF8\x00\x20"
            }
        },
        "on": {
            "h": {
                "v": b"\x20\x20\x38\x00\x00",
                "V": b"\x20\x20\x38\x20\x20"
            },
            "H": {
                "v": b"\x20\x20\xF8\x00\x00",
                "V": b"\x20\x20\xF8\x20\x20"
            }
        }
    },
    7: {
        "off": {
            "h": {
                "v": b"\x00\x00\x00\x00\x00\x00\x00",
                "V": b"\x10\x10\x10\x10\x10\x10\x10"
            },
            "H": {
                "v": b"\x00\x00\x00\xFE\x00\x00\x00",
                "V": b"\x10\x00\x00\xFE\x00\x00\x10"
            }
        },
        "on": {
            "h": {
                "v": b"\x10\x10\x10\x1E\x00\x00\x00",
                "V": b"\x10\x10\x10\x1E\x10\x10\x10"
            },
            "H": {
                "v": b"\x10\x10\x10\xFE\x00\x00\x00",
                "V": b"\x10\x10\x10\xFE\x10\x10\x10"
            }
        }
    },
    8: {
        "off": {
            "h": {
                "v": "8-off-h-v.png",
                "V": "8-off-h-V.png"
            },
            "H": {
                "v": "8-off-H-v.png",
                "V": "8-off-H-V.png"
            }
        },
        "on": {
            "h": {
                "v": "8-on-h-v.png",
                "V": "8-on-h-V.png"
            },
            "H": {
                "v": "8-on-H-v.png",
                "V": "8-on-H-V.png"
            }
        }
    },
    16: {
        "off": {
            "h": {
                "v": "16-off-h-v.png",
                "V": "16-off-h-V.png"
            },
            "H": {
                "v": "16-off-H-v.png",
                "V": "16-off-H-V.png"
            }
        },
        "on": {
            "h": {
                "v": "16-on-h-v.png",
                "V": "16-on-h-V.png"
            },
            "H": {
                "v": "16-on-H-v.png",
                "V": "16-on-H-V.png"
            }
        }
    },
    32: {
        "off": {
            "h": {
                "v": "32-off-h-v.png",
                "V": "32-off-h-V.png"
            },
            "H": {
                "v": "32-off-H-v.png",
                "V": "32-off-H-V.png"
            }
        },
        "on": {
            "h": {
                "v": "32-on-h-v.png",
                "V": "32-on-h-V.png"
            },
            "H": {
                "v": "32-on-H-v.png",
                "V": "32-on-H-V.png"
            }
        }
    }
}
