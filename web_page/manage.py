import asyncio
import webbrowser
import websockets
from resources import resources as re

_websocket = None
_name = None


async def send(header, ip, text):
    global _websocket
    await _websocket.send(f'{header}_/!_{text}(^){ip}')


async def process_message(_message):
    _message = _message.split('_/!_')
    if _message[0] == 'thisisamessage':
        await send_message(*reversed(_message[1].split('~^~')))
    elif _message[0] == 'thisisafile':
        await send_file(*reversed(_message[1].split('~^~')))


async def send_message(ip, text):
    async with re.locks['connected_sockets']:
        await re.connected_sockets[ip.strip()].sendText(text)


async def handler(websocket, path):
    global _websocket
    _websocket = websocket
    await websocket.send(f'thisismyusername_/!_{_name}')
    while True:
        data = await websocket.recv()
        reply = f"Data received as: {data}!"
        print(data)
        await websocket.send(reply)


async def send_file(ip, _path):
    async with re.locks['connected_sockets']:
        await re.connected_sockets[ip.strip()].sendFile(_path)


def start_server():
    _start_server = websockets.serve(handler, "localhost", 12345)
    asyncio.get_event_loop().run_until_complete(_start_server)
    asyncio.get_event_loop().run_forever()


def create_server():
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    start_server()


def make_server(name):
    global _name
    _name = name
    webbrowser.open('web_page/html/index.html')
    create_server()
