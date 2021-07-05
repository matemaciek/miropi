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
    -1:
        b"\x00\x00"+
        b"\x00\xC0"+
        b"\x01\xC0"+
        b"\x03\xC0"+
        b"\x03\xC0"+
        b"\x00\xC0"+
        b"\x78\xC0"+
        b"\x78\xC0"+
        b"\x00\xC0"+
        b"\x00\xC0"+
        b"\x00\xC0"+
        b"\x00\xC0"+
        b"\x00\xC0"+
        b"\x03\xF0"+
        b"\x03\xF0"+
        b"\x00\x00",
    0:
        b"\x00\x00"+
        b"\x1E\x00"+
        b"\x3F\x00"+
        b"\x73\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x73\x80"+
        b"\x3F\x00"+
        b"\x1E\x00"+
        b"\x00\x00",
    1:
        b"\x00\x00"+
        b"\x0C\x00"+
        b"\x1C\x00"+
        b"\x3C\x00"+
        b"\x3C\x00"+
        b"\x0C\x00"+
        b"\x0C\x00"+
        b"\x0C\x00"+
        b"\x0C\x00"+
        b"\x0C\x00"+
        b"\x0C\x00"+
        b"\x0C\x00"+
        b"\x0C\x00"+
        b"\x3F\x00"+
        b"\x3F\x00"+
        b"\x00\x00",
    2:
        b"\x00\x00"+
        b"\x1E\x00"+
        b"\x3F\x00"+
        b"\x73\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x03\x80"+
        b"\x07\x00"+
        b"\x0E\x00"+
        b"\x1C\x00"+
        b"\x38\x00"+
        b"\x70\x00"+
        b"\x61\x80"+
        b"\x7F\x80"+
        b"\x7F\x80"+
        b"\x00\x00",
    3:
        b"\x00\x00"+
        b"\x1E\x00"+
        b"\x3F\x00"+
        b"\x73\x80"+
        b"\x61\x80"+
        b"\x63\x80"+
        b"\x0F\x00"+
        b"\x0F\x00"+
        b"\x03\x80"+
        b"\x01\x80"+
        b"\x01\x80"+
        b"\x61\x80"+
        b"\x73\x80"+
        b"\x3F\x00"+
        b"\x1E\x00"+
        b"\x00\x00",
    4:
        b"\x00\x00"+
        b"\x03\x00"+
        b"\x07\x00"+
        b"\x0F\x00"+
        b"\x1F\x00"+
        b"\x3B\x00"+
        b"\x73\x00"+
        b"\x7F\x80"+
        b"\x7F\x80"+
        b"\x03\x00"+
        b"\x03\x00"+
        b"\x03\x00"+
        b"\x03\x00"+
        b"\x03\x00"+
        b"\x03\x00"+
        b"\x00\x00",
    5:
        b"\x00\x00"+
        b"\x7F\x80"+
        b"\x7F\x80"+
        b"\x61\x80"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x7E\x00"+
        b"\x7F\x00"+
        b"\x03\x80"+
        b"\x01\x80"+
        b"\x01\x80"+
        b"\x61\x80"+
        b"\x73\x80"+
        b"\x3F\x00"+
        b"\x1E\x00"+
        b"\x00\x00",
    6:
        b"\x00\x00"+
        b"\x1E\x00"+
        b"\x3F\x00"+
        b"\x73\x80"+
        b"\x61\x80"+
        b"\x60\x00"+
        b"\x7E\x00"+
        b"\x7F\x00"+
        b"\x73\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x73\x80"+
        b"\x3F\x00"+
        b"\x1E\x00"+
        b"\x00\x00",
    7:
        b"\x00\x00"+
        b"\x7F\x80"+
        b"\x7F\x80"+
        b"\x63\x00"+
        b"\x03\x00"+
        b"\x06\x00"+
        b"\x06\x00"+
        b"\x0C\x00"+
        b"\x0C\x00"+
        b"\x18\x00"+
        b"\x18\x00"+
        b"\x30\x00"+
        b"\x30\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x00\x00",
    8:
        b"\x00\x00"+
        b"\x1E\x00"+
        b"\x3F\x00"+
        b"\x73\x80"+
        b"\x61\x80"+
        b"\x73\x80"+
        b"\x3F\x00"+
        b"\x3F\x00"+
        b"\x73\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x73\x80"+
        b"\x3F\x00"+
        b"\x1E\x00"+
        b"\x00\x00",
    9:
        b"\x00\x00"+
        b"\x1E\x00"+
        b"\x3F\x00"+
        b"\x73\x80"+
        b"\x61\x80"+
        b"\x73\x80"+
        b"\x3F\x80"+
        b"\x1F\x80"+
        b"\x01\x80"+
        b"\x01\x80"+
        b"\x01\x80"+
        b"\x61\x80"+
        b"\x73\x80"+
        b"\x3F\x00"+
        b"\x1E\x00"+
        b"\x00\x00",
    "note_0":
        b"\x00\x00"+
        b"\x1F\x80"+
        b"\x3F\x80"+
        b"\x71\x80"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x71\x80"+
        b"\x3F\x80"+
        b"\x1F\x80"+
        b"\x00\x00",
    "note_1":
        b"\x00\x00"+
        b"\x1F\x82"+
        b"\x3F\x92"+
        b"\x71\x93"+
        b"\x60\x17"+
        b"\x60\x1E"+
        b"\x60\x3A"+
        b"\x60\x32"+
        b"\x60\x13"+
        b"\x60\x17"+
        b"\x60\x1E"+
        b"\x60\x3A"+
        b"\x71\xB2"+
        b"\x3F\x92"+
        b"\x1F\x90"+
        b"\x00\x00",
    "note_2":
        b"\x00\x00"+
        b"\x7E\x00"+
        b"\x7F\x00"+
        b"\x63\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x63\x80"+
        b"\x7F\x00"+
        b"\x7E\x00"+
        b"\x00\x00",
    "note_3":
        b"\x00\x00"+
        b"\x7E\x02"+
        b"\x7F\x12"+
        b"\x63\x93"+
        b"\x61\x97"+
        b"\x61\x9E"+
        b"\x61\xBA"+
        b"\x61\xB2"+
        b"\x61\x93"+
        b"\x61\x97"+
        b"\x61\x9E"+
        b"\x61\xBA"+
        b"\x63\xB2"+
        b"\x7F\x12"+
        b"\x7E\x10"+
        b"\x00\x00",
    "note_4":
        b"\x00\x00"+
        b"\x7F\x80"+
        b"\x7F\x80"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x7F\x00"+
        b"\x7F\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x7F\x80"+
        b"\x7F\x80"+
        b"\x00\x00",
    "note_5":
        b"\x00\x00"+
        b"\x7F\x80"+
        b"\x7F\x80"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x7F\x00"+
        b"\x7F\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x00\x00",
    "note_6":
        b"\x00\x00"+
        b"\x7F\x82"+
        b"\x7F\x92"+
        b"\x60\x13"+
        b"\x60\x17"+
        b"\x60\x1E"+
        b"\x7F\x3A"+
        b"\x7F\x32"+
        b"\x60\x13"+
        b"\x60\x17"+
        b"\x60\x1E"+
        b"\x60\x3A"+
        b"\x60\x32"+
        b"\x60\x12"+
        b"\x60\x10"+
        b"\x00\x00",
    "note_7":
        b"\x00\x00"+
        b"\x1F\x80"+
        b"\x3F\x80"+
        b"\x71\x80"+
        b"\x60\x00"+
        b"\x60\x00"+
        b"\x67\x80"+
        b"\x67\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x71\x80"+
        b"\x3F\x80"+
        b"\x1F\x80"+
        b"\x00\x00",
    "note_8":
        b"\x00\x00"+
        b"\x1F\x82"+
        b"\x3F\x92"+
        b"\x71\x93"+
        b"\x60\x17"+
        b"\x60\x1E"+
        b"\x67\xBA"+
        b"\x67\xB2"+
        b"\x61\x93"+
        b"\x61\x97"+
        b"\x61\x9E"+
        b"\x61\xBA"+
        b"\x71\xB2"+
        b"\x3F\x92"+
        b"\x1F\x90"+
        b"\x00\x00",
    "note_9":
        b"\x00\x00"+
        b"\x1E\x00"+
        b"\x3F\x00"+
        b"\x73\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x7F\x80"+
        b"\x7F\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x00\x00",
    "note_10":
        b"\x00\x00"+
        b"\x1E\x02"+
        b"\x3F\x12"+
        b"\x73\x93"+
        b"\x61\x97"+
        b"\x61\x9E"+
        b"\x7F\xBA"+
        b"\x7F\xB2"+
        b"\x61\x93"+
        b"\x61\x97"+
        b"\x61\x9E"+
        b"\x61\xBA"+
        b"\x61\xB2"+
        b"\x61\x92"+
        b"\x61\x90"+
        b"\x00\x00",
    "note_11":
        b"\x00\x00"+
        b"\x7E\x00"+
        b"\x7F\x00"+
        b"\x63\x80"+
        b"\x61\x80"+
        b"\x63\x80"+
        b"\x7F\x00"+
        b"\x7F\x00"+
        b"\x63\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x61\x80"+
        b"\x63\x80"+
        b"\x7F\x00"+
        b"\x7E\x00"+
        b"\x00\x00",
    "note_mode_0":
        b"\x00\x00"+
        b"\x08\x08"+
        b"\x0C\x0C"+
        b"\xFF\xFE"+
        b"\xFF\xFE"+
        b"\x0C\x0C"+
        b"\x08\x08"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x08\x08"+
        b"\x0C\x0C"+
        b"\xFF\xFE"+
        b"\xFF\xFE"+
        b"\x0C\x0C"+
        b"\x08\x08"+
        b"\x00\x00",
    "note_mode_1":
        b"\x00\x00"+
        b"\x08\x08"+
        b"\x0C\x0C"+
        b"\xFF\xFE"+
        b"\xFF\xFE"+
        b"\x0C\x0C"+
        b"\x08\x08"+
        b"\x00\x00"+
        b"\x00\xC0"+
        b"\x08\xC0"+
        b"\x0C\xC0"+
        b"\xFE\xC0"+
        b"\xFE\xC0"+
        b"\x0C\xC0"+
        b"\x08\xC0"+
        b"\x00\xC0",
    "note_mode_2":
        b"\x00\xC0"+
        b"\x08\xC0"+
        b"\x0C\xC0"+
        b"\xFE\xC0"+
        b"\xFE\xC0"+
        b"\x0C\xC0"+
        b"\x08\xC0"+
        b"\x00\xC0"+
        b"\x00\x00"+
        b"\x08\x08"+
        b"\x0C\x0C"+
        b"\xFF\xFE"+
        b"\xFF\xFE"+
        b"\x0C\x0C"+
        b"\x08\x08"+
        b"\x00\x00",
    "note_mode_3":
        b"\x00\xC0"+
        b"\x08\xC0"+
        b"\x0C\xC0"+
        b"\xFE\xC0"+
        b"\xFE\xC0"+
        b"\x0C\xC0"+
        b"\x08\xC0"+
        b"\x00\xC0"+
        b"\x00\xC0"+
        b"\x08\xC0"+
        b"\x0C\xC0"+
        b"\xFE\xC0"+
        b"\xFE\xC0"+
        b"\x0C\xC0"+
        b"\x08\xC0"+
        b"\x00\xC0",
    "up":
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x01\x80"+
        b"\x03\xC0"+
        b"\x07\xE0"+
        b"\x0F\xF0"+
        b"\x1F\xF8"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00",
    "down":
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x1F\xF8"+
        b"\x0F\xF0"+
        b"\x07\xE0"+
        b"\x03\xC0"+
        b"\x01\x80"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00"+
        b"\x00\x00",
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
