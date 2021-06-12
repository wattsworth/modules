from aiohttp import web

async def handle(request):
    print(request.query)
    return web.Response(text="OK")

app = web.Application()
app.add_routes([web.get('/endpoint', handle)])

if __name__ == '__main__':
    web.run_app(app, port=80)
