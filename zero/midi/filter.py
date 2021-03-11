import abc
from enum import Enum

class Filter(abc.ABC):
    def process(self, msg):
        if msg.type not in self.types():
            return msg
        return self._process(msg)

    @abc.abstractmethod
    def _process(self, msg):
        return NotImplemented

    @abc.abstractmethod
    def types(self):
        return NotImplemented

# TODO: AllFilter

class NoteMode(Enum):
    ALL = 0
    ABOVE = 1
    BELOW = 2
    NONE = 3
    
    def succ(self):
        return NoteMode((self.value + 1) % len(NoteMode))

    def pred(self):
        return NoteMode((self.value - 1) % len(NoteMode))

class NoteFilter(Filter):
    def __init__(self, mode=NoteMode.ALL, note=60):
        self.mode = mode
        self.note = note

    def types(self):
        return ['note_off', 'note_on', 'polytouch']

    def _process(self, msg):
        if self.mode == NoteMode.ALL:
            return msg
        if self.mode == NoteMode.ABOVE:
            return msg if msg.note >= self.note else None
        if self.mode == NoteMode.BELOW:
            return msg if msg.note < self.note else None
        if self.mode == NoteMode.NONE:
            return None
