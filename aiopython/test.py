import asynctest
import pytest

from server import create_app


@pytest.fixture
def cli(loop, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(create_app()))



async def test_main(cli):
    resp = await cli.get('/')
    assert resp.status == 200
    assert len(await resp.json()) == 5


@pytest.mark.asyncio
async def test_weather(cli):
    weather = {
        'city': 'Moscow',
        'precipitation': 'snow',
        'temperature': -12.5,
        'pressure': 1000,
        'humidity': 300,
    }
    with asynctest.mock.patch('server.get_weather', side_effect=lambda _: weather):
        resp = await cli.get('/weather/test name1')
    assert resp.status == 200
    assert await resp.json() == weather
