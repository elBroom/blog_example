from aiohttp import web

from server import create_app

web.run_app(create_app())
