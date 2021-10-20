import mido

import config
import midi.connection

class Port:
    def __init__(self, name):
        self.enabled = True
        self.alias = None
        self.port_name = name
        splitted = name.split(":")
        self.device = splitted[0]
        self.port = " ".join(splitted[1].split(" ")[0:-1])
        self.id = ":".join([splitted[1].split(" ")[-1], splitted[2]])
        self.full_id = self.device + " / " + self.port

    @property
    def hidden(self):
        return not self.enabled

    def toggle(self):
        self.enabled = not self.enabled
        (self._after_change)(self)

    def setup(self, hidden, alias, after_change):
        self.config = config
        self.enabled = not hidden
        self.alias = alias
        self._after_change = after_change

    def name(self):
        """unique name for config"""
        if self.alias is not None:
            return self.alias
        return self.full_id

    @property
    def short_name(self):
        if self.alias is not None:
            return self.alias
        return self.port

    def names(self):
        return [self.alias, self.full_id]

    def named(self, name):
        return name in self.names()

def _get_by_name(name, ports):
    return next(p for p in ports if p.named(name))

def _valid_inputs():
    return sorted([dev for dev in mido.get_input_names() if dev[0:6] != 'RtMidi'])

def _valid_outputs():
    return sorted([dev for dev in mido.get_output_names() if dev[0:6] != 'RtMidi'])

class Connections:
    def __init__(self):
        self._config = config.Config()
        inputs = _valid_inputs()
        outputs = _valid_outputs()
        self._devices = str(inputs + outputs)
        self.inputs = [Port(port) for port in inputs]
        self.outputs = [Port(port) for port in outputs]
        self._config.register_inputs(self.inputs)
        self._config.register_outputs(self.outputs)
        self._connections = {}
        for src, dst in self._config.connections():
            try:
                self._toggle((_get_by_name(src, self.inputs), _get_by_name(dst, self.outputs)))
            except StopIteration:
                next

    def outdated(self):
        return self._devices != str(_valid_inputs() + _valid_outputs())

    def M(self):
        return len(self._enabled_inputs())

    def N(self):
        return len(self._enabled_outputs())

    def connected(self, coord):
        (src, dst) = self._coord_to_ports(coord)
        try:
            return self._connections[src.id].connected(dst)
        except KeyError:
            return False

    def toggle(self, coord):
        (src, dst) = self._coord_to_ports(coord)
        self._toggle((src, dst))
        self._config.update((src, dst), self.connected(coord))

    def _toggle(self, coord):
        (src, dst) = coord
        if src.id not in self._connections:
            self._connections[src.id] = midi.connection.Connection(src)
        self._connections[src.id].toggle(dst)

    def _enabled_inputs(self):
        return [input for input in self.inputs if input.enabled]

    def _enabled_outputs(self):
        return [output for output in self.outputs if output.enabled]

    def _coord_to_ports(self, coord):
        (i, j) = coord
        return (self._enabled_inputs()[i], self._enabled_outputs()[j])

    def input_name(self, i):
        return self._enabled_inputs()[i].short_name

    def output_name(self, j):
        return self._enabled_outputs()[j].short_name

    def input_name_for_id(self, id):
        return next(p for p in self.inputs if p.id == id).short_name

    def output_name_for_id(self, id):
        return next(p for p in self.outputs if p.id == id).short_name

    def connections(self):
        result = []
        for src in self._connections.keys():
            result += [(src, dst) for dst in self._connections[src].outputs()]
        return result

    def filter(self, connection):
        (src, dst) = connection
        return self._connections[src].to(dst).filter

    def set_filter(self, connection, mode, note):
        (src, dst) = connection
        self._connections[src].to(dst).filter = midi.filter.NoteFilter(mode, note)

    def drop_ports(self):
        print( "Cleaning connections" )
        for key in list( self._connections.keys() ):
            self._connections[key].cleanup()

