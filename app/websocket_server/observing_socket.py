from utils import Observer


class ObservingSocket(Observer):
    def __init__(self, socket):
        self.socket = socket
        self.updated = None

    def update(self, new_value):
        self.updated = new_value

    @property
    def closed(self):
        return self.socket.closed

    async def send(self):
        data = self.updated
        self.updated = None
        await self.socket.send_str(data)

    async def close(self, *args, **kwargs):
        await self.socket.close(*args, **kwargs)
