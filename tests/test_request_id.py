import pytest
from aiohttp import web

from app.middlewares import add_request_id


def make_request(app: web.Application):
    class Request(dict):
        pass
    request = Request()
    request.app = app
    return request


async def test_request_id(app, handler):
    request = make_request(app)
    await add_request_id(request, handler)
    request_id = request.get('request_id', None)
    assert isinstance(request_id, str)


@pytest.mark.parametrize('count', [10000])
async def test_unique_request_id(app, handler, count: int):
    ids = set()
    for _ in range(count):
        request = make_request(app)
        await add_request_id(request, handler)
        ids.add(request.get('request_id', None))
    assert len(ids) == count
