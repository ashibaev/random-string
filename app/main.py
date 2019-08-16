import argparse
import logging
import logging.config
import sys
import weakref

from typing import List

from aiohttp import web
from aiohttp import WSCloseCode

from app.routes import setup_routes
from app.middlewares import setup_middlewares
from app.settings import load_config, Config, DEFAULT_CONFIG_PATH
from app.string_generator import StringGenerator

__all__ = [
    'main',
    'init_app'
]


def get_config_path(args: List[str]) -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=str(DEFAULT_CONFIG_PATH))
    return parser.parse_args(args).config


async def close_sockets(app: web.Application) -> None:
    logger = logging.getLogger()
    logger.info(f'Need to close {len(app["websockets"])} sockets. Closing...')
    websocket: web.WebSocketResponse
    for websocket in set(app['websockets']):
        await websocket.close(code=WSCloseCode.GOING_AWAY,
                              message=b'Server shutdown')
    logger.info('All sockets are closed.')


def init_app(config: Config, logger: logging.Logger) -> web.Application:
    app = web.Application(logger=logger)

    app['config'] = config
    app['string_generator'] = StringGenerator(
        config.string_generator.length,
        config.string_generator.symbols
    )
    app['websockets'] = weakref.WeakSet()

    app.on_shutdown.append(close_sockets)

    setup_routes(app)
    setup_middlewares(app)

    return app


def main(argv):
    config = load_config(get_config_path(argv))
    logging.config.dictConfig(config.logging)
    logger = logging.getLogger()
    logging.debug(f'Initialize app with config: {config}')
    app = init_app(config, logger)
    logger.info('Starting app...')
    web.run_app(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main(sys.argv[1:])
