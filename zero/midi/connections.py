import mido

import midi.connection

class Port:
    def __init__(self, name):
        self.name = name
        splitted = name.split(":")
        self.device = splitted[0]
        self.port = " ".join(splitted[1].split(" ")[0:-1])
        self.id = ":".join([splitted[1].split(" ")[-1], splitted[2]])

class Connections:
    def __init__(self):
        self._inputs = [Port(port) for port in sorted(mido.get_input_names())]
        self._outputs = [Port(port) for port in sorted(mido.get_output_names())]
        self.M = len(self._inputs)
        self.N = len(self._outputs)
        self._connections = {}

    def connected(self, coord):
        (i, j) = coord
        try:
            return self._connections[i].connected(self._outputs[j])
        except KeyError:
            return False

    def toggle(self, coord):
        (i, j) = coord
        if i not in self._connections:
            self._connections[i] = midi.connection.Connection(self._inputs[i])
        self._connections[i].toggle(self._outputs[j])

    def input_name(self, i):
        return self._inputs[i].port

    def output_name(self, j):
        return self._outputs[j].port
