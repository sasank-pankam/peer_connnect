import asyncio
import os
import webbrowser
import websockets
from resources import resources as re
#hello
_websocket = None
_name = None


def send(header, ip, text):
    global _websocket
    asyncio.run(_websocket.send(f'{header}_/!_{text}(^){ip}'))
    print(f'send  ---- {header}_/!_{text}(^){ip}')


async def process_message(_message):
    print('process_message --- ',_message)
    _message = _message.split('_/!_')
    if _message[0] == 'thisisamessage':
        send_message(*reversed(_message[1].split('~^~')))
    elif _message[0] == 'thisisafile':
        send_file(*reversed(_message[1].split('~^~')))


def send_message(ip, text):
    print('send_message --- ',ip, text)
    with re.locks['connected_sockets']:
        re.connected_sockets[ip.strip()].sendText(text)


async def handler(websocket, path):

    global _websocket
    _websocket = websocket
    try:
        await websocket.send(f'thisismyusername_/!_{_name}')
        while True:
            data = await websocket.recv()
            reply = f"Data received as: {data}!"
            print(data)
            await process_message(data)
    except Exception as e:
        print('webpage closed!!')


def send_file(ip, _path):
    print('send_file --- ', ip, _path)
    with re.locks['connected_sockets']:
        print(re.connected_sockets)
        re.connected_sockets[ip.strip()].sendFile(_path)


def start_server():
    _start_server = websockets.serve(handler, "localhost", 12346)
    asyncio.get_event_loop().run_until_complete(_start_server)
    asyncio.get_event_loop().run_forever()


def create_server():
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    start_server()


def make_server(name):
    global _name
    _name = name
    webbrowser.open(os.getcwd() + '/web_page/html/index.html')
    create_server()
