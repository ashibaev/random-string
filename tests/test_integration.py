from aiohttp import web

from app.settings import Config


async def test_websocket_can_prepare(app_server):
    response = await app_server.get('/ws')
    assert response.status == web.HTTPUpgradeRequired.status_code


async def test_websocket_receive_data(app_server, config: Config):
    response: web.WebSocketResponse = await app_server.ws_connect('/ws')
    data = await response.receive_str()
    assert len(data) == config.string_generator.length
    assert set(data).issubset(set(config.string_generator.symbols))
    await response.send_str('')
