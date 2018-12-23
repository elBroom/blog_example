from aiohttp import ClientSession, web
from aiomysql.sa import create_engine
import sqlalchemy as sa
from marshmallow import Schema, fields


API_KEY = 'd2bfda841c26acc2637199b2a7b03086'


# models
metadata = sa.MetaData()

users = sa.Table('users', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(255)),
    sa.Column('city', sa.String(255)),
    sa.Column('email', sa.String(255)),
)


# schemas
class UserSchema(Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    city = fields.String(required=True)
    email = fields.Email(required=True)

user_schema = UserSchema()


# middleware
@web.middleware
async def db_middleware(request, handler):
    if 'db' not in request.app:
        request.app['db'] = await create_engine(
            user='root',
            db='highloadCup',
            host='0.0.0.0',
            password='1234',
        )

    return await handler(request)



# service
async def get_weather(city):
    async with ClientSession() as client:
        async with client.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={API_KEY}'
        ) as resp:
            if resp.status != 200:
                raise ValueError

            data = await resp.json()
            return {
                'city': city,
                'precipitation': data['weather'][0]['main'],
                'temperature': data['main']['temp'],
                'pressure': data['main']['humidity'],
                'humidity': data['main']['pressure'],
            }
    raise ValueError

# views
async def handle_weather(request):
    async with request.app['db'].acquire() as conn:
        rv = await conn.execute(users.select().where(users.c.name==request.match_info['name']))
        row = await rv.fetchone()
        if not row:
            raise web.HTTPNotFound

    try:
        answer = await get_weather(row.city)
    except ValueError:
        raise web.HTTPServiceUnavailable(text='Ooops!')
    return web.json_response(answer)


async def handle_hello(request):
    async with request.app['db'].acquire() as conn:
        rv = await conn.execute(users.select().where(users.c.name==request.match_info['name']))
        row = await rv.fetchone()
        if not row:
            raise web.HTTPNotFound

    return web.json_response(user_schema.dump(row).data)

async def handle_all(request):
    async with request.app['db'].acquire() as conn:
        rv = await conn.execute(users.select())
        res = await rv.fetchall()

    return web.json_response([user_schema.dump(row).data for row in res])

async def handle_create(request):
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError as e:
        return web.json_response({'status': 400, 'errors': 'invalid JSON'}, status=400)

    user, errors = user_schema.load(data)
    if errors:
        return web.json_response({'status': 400, 'errors': errors}, status=400)

    user_id = 0
    async with request.app['db'].acquire() as conn:
        rv = await conn.execute(users.insert().values(**data))
        await conn.execute('commit;')
        user_id = rv.lastrowid

    if user_id:
        return web.json_response({"id": user_id}, status=204)
    raise web.HTTPServiceUnavailable(text='Ooops!')



# app
def create_app():
    app = web.Application(middlewares=[db_middleware])
    app.add_routes([
        web.post('/', handle_create),
        web.get('/', handle_all),
        web.get('/weather/{name}', handle_weather),
        web.get('/{name}', handle_hello),
    ])
    return app
