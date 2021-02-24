import PIL.Image

def _compile(data, size, invert):
    if type(data) is dict:
        return {k:_compile(v, size, invert) for (k, v) in data.items()}
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
        self._icons = _compile(_raw_icons, 16, False)

    def icon(self, name):
        return self._icons[name]

    def tile(self, tile):
        return self._tiles[tile.invert][tile.state][tile.state_h][tile.state_v]

_raw_icons = {
    "connected":
        b"\xC0\x00"+
        b"\xE0\x00"+
        b"\x70\x00"+
        b"\x3F\x80"+
        b"\x1F\xC0"+
        b"\x18\xE0"+
        b"\x1B\x70"+
        b"\x1B\xB0"+
        b"\x1D\xC0"+
        b"\x0E\xF0"+
        b"\x07\x78"+
        b"\x03\x78"+
        b"\x00\x3C"+
        b"\x00\x0E"+
        b"\x00\x07"+
        b"\x00\x03",
    "disconnected":
        b"\xC0\x00"+
        b"\xE0\x00"+
        b"\x7F\x00"+
        b"\x3F\x80"+
        b"\x31\xC0"+
        b"\x30\xE0"+
        b"\x30\x70"+
        b"\x38\x00"+
        b"\x1C\xC0"+
        b"\x0E\xE0"+
        b"\x06\x70"+
        b"\x00\x3C"+
        b"\x00\x1E"+
        b"\x00\x1E"+
        b"\x00\x0F"+
        b"\x00\x03",
    "checked":
        b"\xFF\xFF"+
        b"\xFF\xFF"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x0B"+
        b"\xC0\x1B"+
        b"\xC0\x3B"+
        b"\xC0\x73"+
        b"\xD0\xE3"+
        b"\xD9\xC3"+
        b"\xDF\x83"+
        b"\xCF\x03"+
        b"\xC6\x03"+
        b"\xC0\x03"+
        b"\xFF\xFF"+
        b"\xFF\xFF",
    "unchecked":
        b"\xFF\xFF"+
        b"\xFF\xFF"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xC0\x03"+
        b"\xFF\xFF"+
        b"\xFF\xFF"
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
                "v": b"\x00\x00\x00\x00\x00\x00\x00\x00",
                "V": b"\x18\x18\x18\x18\x18\x18\x18\x18"
            },
            "H": {
                "v": b"\x00\x00\x00\xFF\xFF\x00\x00\x00",
                "V": b"\x18\x00\x00\xFF\xFF\x00\x00\x18"
            }
        },
        "on": {
            "h": {
                "v": b"\x18\x18\x18\x1F\x1F\x00\x00\x00",
                "V": b"\x18\x18\x18\x1F\x1F\x18\x18\x18"
            },
            "H": {
                "v": b"\x18\x18\x18\xFF\xFF\x00\x00\x00",
                "V": b"\x18\x18\x18\xFF\xFF\x18\x18\x18"
            }
        }
    },
    16: {
        "off": {
            "h": {
                "v":
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00",
                "V":
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"
            },
            "H": {
                "v":
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\xFF\xFF"+
                    b"\xFF\xFF"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00",
                "V":
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\xFF\xFF"+
                    b"\xFF\xFF"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"
            }
        },
        "on": {
            "h": {
                "v":
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\xFF"+
                    b"\x01\xFF"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00",
                "V":
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\xFF"+
                    b"\x01\xFF"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"
            },
            "H": {
                "v":
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\xFF\xFF"+
                    b"\xFF\xFF"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00"+
                    b"\x00\x00",
                "V":
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\xFF\xFF"+
                    b"\xFF\xFF"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"+
                    b"\x01\x80"
            }
        }
    }
}
