import asyncio
import contextlib
import os
import threading
import weakref

from string_generator import StringGenerator

from aiohttp import web
from aiohttp import WSCloseCode

from websocket_server.observing_socket import ObservingSocket


PORT = int(os.environ.get('PORT', '8080'))
STRING_LENGTH = int(os.environ.get('STRING_LENGTH', '16'))
UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL', '5'))

__all__ = [
    'main'
]


@contextlib.asynccontextmanager
async def prepare_socket(request):
    app = request.app
    string = app['string']
    socket = web.WebSocketResponse()
    await socket.prepare(request)
    wrapper = ObservingSocket(socket)
    string.register(wrapper)
    app['websockets'].add(wrapper)
    try:
        yield wrapper
    finally:
        string.delete_observer(wrapper)
        request.app['websockets'].discard(wrapper)
        wrapper.close()


async def handle_request(request):
    async with prepare_socket(request) as websocket:
        while not websocket.closed:
            await asyncio.sleep(0.05)
            if websocket.updated:
                await websocket.send()


async def on_shutdown(app):
    for ws in set(app['websockets']):
        await ws.close(code=WSCloseCode.GOING_AWAY,
                       message='Server shutdown')


def init_app():
    app = web.Application()

    app['websockets'] = weakref.WeakSet()
    app.on_shutdown.append(on_shutdown)
    app.add_routes([web.get('/', handle_request)])

    string = StringGenerator()
    app['string'] = string

    return app


def main():
    app = init_app()

    updating = threading.Thread(
        target=StringGenerator.update_string,
        args=(app['string'], STRING_LENGTH, UPDATE_INTERVAL)
    )
    updating.start()
    web.run_app(app, host='0.0.0.0', port=PORT)


if __name__ == '__main__':
    main()
