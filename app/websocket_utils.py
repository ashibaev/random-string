import asyncio
import logging

from contextlib import asynccontextmanager
from typing import NoReturn

from aiohttp import web

from app.app_utils import get_config, get_string_generator
from app.string_generator import StringGenerator


@asynccontextmanager
async def prepare_socket(websocket: web.WebSocketResponse, request: web.Request):
    await websocket.prepare(request)
    request.app['websockets'].add(websocket)
    loop = asyncio.get_running_loop()
    request['updating_task'] = loop.create_task(
        update_socket_data(
            websocket,
            get_string_generator(request.app),
            get_config(request.app).update_interval,
            request.app.logger,
            request["request_id"]
        )
    )
    request.app.logger.info(f"Websocket for [id={request['request_id']}] is initialized")
    try:
        yield
    finally:
        request.app['websockets'].discard(websocket)
        request['updating_task'].cancel()
        await websocket.close()
        request.app.logger.info(f"Websocket for [id={request['request_id']}] is closed")


async def update_socket_data(websocket: web.WebSocketResponse,
                             string_generator: StringGenerator,
                             interval: float,
                             logger: logging.Logger,
                             request_id: str) -> NoReturn:
    while True:
        logger.debug(f"Try update data for [id={request_id}]")
        if not websocket.closed:
            data = string_generator.generate_string()
            await websocket.send_str(data)
            logger.debug(f"Updated: [id={request_id}]. New data: {data}")
        else:
            logger.debug(f"Can't update [id={request_id}]")
        await asyncio.sleep(interval)
