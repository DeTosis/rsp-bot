import aiohttp_cors
from aiohttp import web
import asyncio

from bot.modules.core_modules.telegram_bot import TelegramBot
import bot.modules.aiohttp_endpoint.endpoint_commands as ec

class ServerEndpoint:

    def __init__(self, port: int, bot: TelegramBot):
        self.port = port
        self.bot = bot

    async def handle(self, request):
        req = await request.text()

        if req == 'stopBot':
            await ec.shutdown()

        if req == 'startBot':
            await ec.start(self.bot)

        if req == 'isAlive':
            isValid = await ec.validate()
            return web.Response(text=f'{isValid}', status=200)

        if req == 'get-recent':
            data = await ec.retriveRecent(self.bot)
            return web.json_response(data, status=200)
        
        if req == 'get-schedules-parsed':
            data = await ec.retriveSchedules()
            return web.json_response(data, status=200)

        return web.Response()

    async def bot_server(self):
        app = web.Application()
        app.router.add_post('/', self.handle)

        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*"
            )
        })

        for route in list(app.router.routes()):
            cors.add(route)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        await site.start()
        print(f'[ INFO ] Server started at port {self.port}')
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            print('[ INFO ] Server task cancelled')
            return