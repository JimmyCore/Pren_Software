import json

import aiohttp_cors
import socketio
from aiohttp import web
# DEPRECATED
# # create a Socket.IO server
# sio = socketio.AsyncServer(cors_allowed_origins="*")
#
# app = web.Application()
# sio.attach(app)
#
# cors = aiohttp_cors.setup(app, defaults={
#     "*": aiohttp_cors.ResourceOptions(
#         allow_credentials=True,
#         expose_headers="*",
#         allow_headers="*",
#     )
# })
#
#
# @sio.on('*')
# async def catch_all(event, sid, data):
#     pass
#
#
# @sio.event
# async def connect(sid, environ, auth):
#     print('connect ', sid)
#
#
# @sio.event
# async def disconnect(sid):
#     print('disconnect ', sid)
#
#
# async def handleRun(request):
#     data = {
#         "name": "StatusInfo",
#         "status": "online"
#     }
#     return web.Response(text=json.dumps(data))
#
#
# def startServer():
#     web.AppRunner(app)
#     # web.run_app(app)
#     return sio
#
#
# run = cors.add(app.router.add_resource("/run"))
# cors.add(run.add_route("GET", handleRun))



