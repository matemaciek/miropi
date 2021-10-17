import yaml

CONF_FILE = 'config.yaml'

class Config:
    @staticmethod
    def _load_file():
        open(CONF_FILE, 'a').close() # create if not exists
        with open(CONF_FILE) as file:
            config = yaml.load(file, Loader=yaml.Loader)
            if config is None:
                config = {'connections': {}, 'input': {}, 'output': {}}
            return config

    def _save(self):
        with open(CONF_FILE, 'w') as file:
            yaml.dump(self._content, file, Dumper=yaml.Dumper)

    def __init__(self):
        self._content = self._load_file()

    def _register_ports(self, ports, destination):
        for port in ports:
            if port.full_id in destination:
                setup = destination[port.full_id]
                port.setup(
                    'hidden' in setup and setup['hidden'],
                    setup['alias'] if 'alias' in setup else None,
                    lambda port: self._update_port(port, destination[port.full_id])
                )
            else:
                destination[port.full_id] = {}
        self._save()

    def register_inputs(self, ports):
        self._register_ports(ports, self._content['input'])

    def register_outputs(self, ports):
        self._register_ports(ports, self._content['output'])

    def connections(self):
        return [(src, dst) for src, dsts in self._content['connections'].items() for dst in dsts]

    def update(self, coord, connected):
        (src, dst) = coord
        connections = self._content['connections']
        if connected:
            try:
                key = next(name for name in src.names() if name in connections)
            except StopIteration:
                key = src.name()
                connections[key] = []
            connections[key].append(dst.name())
        else:
            key = next(name for name in src.names() if name in connections)
            value = next(name for name in dst.names() if name in connections[key])
            connections[key].remove(value)
            if len(connections[key]) == 0:
                del connections[key]
        self._save()

    def _update_port(self, port, destination):
        destination['hidden'] = port.hidden
        self._save()
