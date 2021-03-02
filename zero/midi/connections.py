import mido
import itertools
import yaml

import midi.connection

CONF_FILE = 'config.yaml'

class Port:
    def __init__(self, name):
        self.name = name
        self.enabled = True
        splitted = name.split(":")
        self.device = splitted[0]
        self.port = " ".join(splitted[1].split(" ")[0:-1])
        self.id = ":".join([splitted[1].split(" ")[-1], splitted[2]])

    def persistent_id(self):
        return self.device + " / " + self.port

    def toggle(self):
        self.enabled = not self.enabled

def _unpersist_id(id, ports):
    return next(p for p in ports if p.persistent_id() == id)

def _save_hidden_ports(config, ports):
    for p in ports:
        if p.enabled: # remove if necessary
            if p.device in config:
                if p.port in config[p.device]:
                    config[p.device].remove(p.port)
                if len(config[p.device]) == 0:
                    del config[p.device]
        else: # add if necessary
            if p.device not in config:
                config[p.device] = []
            if p.port not in config[p.device]:
                config[p.device].append(p.port)


def _load_hidden_ports(config, ports):
    for p in ports:
        try:
            if p.port in config[p.device]:
                p.toggle()
        except KeyError:
            next

class Connections:
    def __init__(self):
        self.inputs = [Port(port) for port in sorted(mido.get_input_names())]
        self.outputs = [Port(port) for port in sorted(mido.get_output_names())]
        self._connections = {}
        self.load()

    def save(self):
        _save_hidden_ports(self._config['hidden inputs'], self.inputs)
        _save_hidden_ports(self._config['hidden outputs'], self.outputs)
        with open(CONF_FILE, 'w') as file:
            yaml.dump(self._config, file, Dumper=yaml.Dumper)

    def load(self):
        open(CONF_FILE, 'a').close() # create if not exists
        with open(CONF_FILE) as file:
            config = yaml.load(file, Loader=yaml.Loader)
            self._config = {'hidden inputs': {}, 'hidden outputs': {}, 'connections': {}} if config is None else config
            _load_hidden_ports(self._config['hidden inputs'], self.inputs)
            _load_hidden_ports(self._config['hidden outputs'], self.outputs)
            for src, dsts in self._config['connections'].items():
                for dst in dsts:
                    try:
                        self._toggle((_unpersist_id(src, self.inputs), _unpersist_id(dst, self.outputs)))
                    except StopIteration:
                        next

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

        # update config
        connections = self._config['connections']
        if self.connected(coord):
            if src.persistent_id() not in connections:
                connections[src.persistent_id()] = []
            connections[src.persistent_id()].append(dst.persistent_id())
        else:
            connections[src.persistent_id()].remove(dst.persistent_id())
            if len(connections[src.persistent_id()]) == 0:
                del connections[src.persistent_id()]

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
        return self._enabled_inputs()[i].port

    def output_name(self, j):
        return self._enabled_outputs()[j].port
