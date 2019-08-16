import uuid

from aiohttp import web


@web.middleware
async def add_request_id(request: web.Request, handler) -> web.Response:
    request['request_id'] = uuid.uuid4().hex
    request.app.logger.info(
        f"New connection [id={request['request_id']}]"
    )
    try:
        response = await handler(request)
    except Exception as e:
        request.app.logger.error(f"Error occur in [id={request['request_id']}]: {repr(e)}")
        raise
    return response


def setup_middlewares(app: web.Application) -> None:
    app.middlewares.append(add_request_id)
