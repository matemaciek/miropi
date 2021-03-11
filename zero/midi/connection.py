import asyncio
import time
import mido

import midi.filter

async def _send(port, msg):
    port.send(msg)

class Writer:
    def __init__(self, output):
        self.output = output
        self._output_port = mido.open_output(output.name)
        self.queue = asyncio.Queue()
        self.filter = midi.filter.NoteFilter()
        self._worker_task = asyncio.create_task(self._worker())

    async def _worker(self):
        while True:
            msg = await self.queue.get()
            filtered = self.filter.process(msg)
            if filtered is not None:
                print("Out:", self.output.id, filtered)
                asyncio.create_task(_send(self._output_port, filtered))
            else:
                print("Filtered:", self.output.id, msg)

    def __del__(self):
        self._worker_task.cancel()
        self._output_port.close()

class Connection:
    def __init__(self, input):
        self._input = input
        self._outputs = {}

    def connected(self, output):
        return output.id in self._outputs

    def to(self, dst):
        return self._outputs[dst]

    def toggle(self, output):
        if self.connected(output):
            self.disconnect(output)
        else:
            self.connect(output)

    def sinks(self):
        return len(self._outputs)

    def dump(self):
        return [k for k in self._outputs.keys()]

    def connect(self, output):
        if self.sinks() == 0:
            self._start_reader()
        self._outputs[output.id] = Writer(output)

    def disconnect(self, output):
        del self._outputs[output.id]
        if self.sinks() == 0:
            self._stop_reader()

    def _start_reader(self):
        loop = asyncio.get_event_loop()
        def callback(msg):
            msg.time = time.monotonic()
            #print("In:", self._input.id, msg)
            for output in self._outputs.values():
                loop.call_soon_threadsafe(output.queue.put_nowait, msg)
        
        self._input_port = mido.open_input(self._input.name, callback=callback)

    def _stop_reader(self):
        self._input_port.close()

    def __del__(self):
        for output in list(self._outputs.values()):
            self.disconnect(output.output)

    def outputs(self):
        return self._outputs.keys()
