import pytest

import logging
import logging.config

from aiohttp import web

from app.settings import load_config, Config, PROJECT_ROOT
from app.main import init_app

TEST_CONFIG_PATH = PROJECT_ROOT.parent / 'config' / 'app.test.yml'


@pytest.fixture
def config() -> Config:
    return load_config(TEST_CONFIG_PATH)


@pytest.fixture
def logger(config) -> logging.Logger:
    logging.config.dictConfig(config.logging)
    return logging.getLogger()


@pytest.fixture
def handler():
    async def ok_handler(request: web.Request) -> web.HTTPOk:
        return web.HTTPOk()
    return ok_handler


@pytest.fixture
def app(config: Config, logger: logging.Logger) -> web.Application:
    return init_app(config, logger)


@pytest.fixture
def app_server(loop, aiohttp_client, app: web.Application):
    return loop.run_until_complete(aiohttp_client(app))
