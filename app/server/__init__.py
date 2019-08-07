import asyncio
import os
import weakref

from os.path import dirname, join

from aiohttp import web
from aiohttp import WSCloseCode


PATH = join(dirname(__file__), 'client.html')
PORT = int(os.environ.get('PORT', '8080'))


async def handle(request):
    return web.FileResponse(PATH)


def main():
    app = web.Application()
    app.add_routes([web.get('/', handle)])

    web.run_app(app, host='0.0.0.0', port=PORT)


if __name__ == '__main__':
    main()
