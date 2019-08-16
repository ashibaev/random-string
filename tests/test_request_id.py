import pytest
from aiohttp import web

from app.middlewares import add_request_id


def make_request(app: web.Application):
    class Request(dict):
        pass
    request = Request()
    request.app = app
    return request


async def test_request_id(app: web.Application, handler):
    request = make_request(app)
    await add_request_id(request, handler)
    request_id = request.get('request_id', None)
    assert isinstance(request_id, str)


@pytest.mark.parametrize('iterations', [10000])
async def test_unique_request_id(app: web.Application, handler, iterations: int):
    unique_ids = set()
    for _ in range(iterations):
        request = make_request(app)
        await add_request_id(request, handler)
        unique_ids.add(request.get('request_id', None))
    assert len(unique_ids) == iterations
