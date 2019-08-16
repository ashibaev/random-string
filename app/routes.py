from aiohttp import web

from app.views import handle_websocket


def setup_routes(app: web.Application) -> None:
    app.router.add_get('/ws', handle_websocket)
