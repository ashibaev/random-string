from aiohttp import web

from app.settings import Config
from app.string_generator import StringGenerator


def get_config(app: web.Application) -> Config:
    return app['config']


def get_string_generator(app: web.Application) -> StringGenerator:
    return app['string_generator']
