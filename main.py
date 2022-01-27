import asyncio

from config import Config
from handlers import process_request


async def main():
    if Config.DEBUG:
        server = await asyncio.start_server(process_request, '0.0.0.0', 443)
    else:
        server = await asyncio.start_server(process_request, '127.0.0.1', 443)

    async with server:
        await server.serve_forever()


asyncio.run(main())
