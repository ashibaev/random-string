from typing import Union

from aiohttp import web

from app.websocket_utils import prepare_socket


async def handle_websocket(request: web.Request) -> Union[web.Response, web.WebSocketResponse]:
    websocket = web.WebSocketResponse()
    if not websocket.can_prepare(request):
        return web.HTTPUpgradeRequired()
    async with prepare_socket(websocket, request):
        await websocket.receive()
        return websocket
