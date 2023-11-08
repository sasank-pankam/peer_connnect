import asyncio
import os
import webbrowser
import websockets
from resources import resources as re


_websocket = None
_name = None


def send(header, ip, text):
    """forwards a message with required format to webpage"""
    global _websocket
    asyncio.run(_websocket.send(f'{header}_/!_{text}(^){ip}'))
    print(f'send  ---- {header}_/!_{text}(^){ip}')


async def process_message(_message):
    """process the message received from webpage"""
    print('process_message --- ', _message)
    _message = _message.split('_/!_')
    if _message[0] == 'thisisamessage':
        send_message(*reversed(_message[1].split('~^~')))
    elif _message[0] == 'thisisafile':
        send_file(*reversed(_message[1].split('~^~')))


async def handler(websocket, path):
    """function that handles websocket server object"""
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


def send_message(ip, text):
    """calls a sendText method of handleSocket object to send message content as text"""
    print('send_message --- ', ip, text)
    with re.locks['connected_sockets']:
        re.connected_sockets[ip.strip()].sendText(text)


def send_file(ip, _path):
    """calls a sendFIle method of handleSocket object to send a file of path _path"""
    print('send_file --- ', ip, _path)
    with re.locks['connected_sockets']:
        print(re.connected_sockets)
        re.connected_sockets[ip.strip()].sendFile(_path)


def start_server():
    """starts a websocket server to communicate with webpage"""
    _start_server = websockets.serve(handler, "localhost", 12346)
    asyncio.get_event_loop().run_until_complete(_start_server)
    asyncio.get_event_loop().run_forever()


def create_server():
    """Creates a prerequisites for starting server"""
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    start_server()


def make_server(name):
    """loads webpage and calls create_server function """
    global _name
    _name = name
    webbrowser.open(os.getcwd() + '/web_page/html/index.html')
    create_server()
