import mido

import midi.connection

class Port:
    def __init__(self, name):
        self.name = name
        self.enabled = True
        splitted = name.split(":")
        self.device = splitted[0]
        self.port = " ".join(splitted[1].split(" ")[0:-1])
        self.id = ":".join([splitted[1].split(" ")[-1], splitted[2]])

    def toggle(self):
        self.enabled = not self.enabled

class Connections:
    def __init__(self):
        self.inputs = [Port(port) for port in sorted(mido.get_input_names())]
        self.outputs = [Port(port) for port in sorted(mido.get_output_names())]
        self._connections = {}

    #def reload(self):

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
        return self._enabled_inputs()[i].port

    def output_name(self, j):
        return self._enabled_outputs()[j].port
