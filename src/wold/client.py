
import subprocess
import asyncio
import websockets


class Client():
    def __init__(self, config):
        self.config = config


    def start(self):
        asyncio.get_event_loop().run_until_complete(self._connect())
        asyncio.get_event_loop().run_forever()

    async def _connect(self):
        uri = f'ws://{self.config.host}:{self.config.port}'
        async with websockets.connect(uri) as websocket:
            # For crash see here: https://stackoverflow.com/questions/49878953/issues-listening-incoming-messages-in-websocket-client-on-python-3-6
            while True:
                target = await websocket.recv()
                if target:
                    self._wake(target)
            
    def _wake(self, label):
        if label in self.config.inventory:
            subprocess.run(['wakeonlan', self.config.inventory[label]])
            print(f'magic packet sent to: {label}')
        else:
            print(f'device not recognized: {label}')
