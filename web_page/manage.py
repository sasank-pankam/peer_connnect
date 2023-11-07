import time
import threading
import webbrowser as wb
import resources.resources as re
import asyncio
import websockets


def send_message(ip, text):
    with re.locks['connected_sockets']:
        re.connected_sockets[ip.strip()].sendText(text)


def send_file(ip, path):
    with re.locks['connected_sockets']:
        re.connected_sockets[ip.strip()].sendFile(path)


def process_message(message):
    message = message.split('_/!_')
    if message[0] == 'thisisamessage':
        send_message(*reversed(message[1].split('~^~')))
    elif message[0] == 'thisisafile':
        send_file(*reversed(message[1].split('~^~')))


class WebSocketHandler:
    def __init__(self):
        self.websocket = None
        self.server = websockets.serve(self.handle_connection, 'localhost', 12346)
        print()
        server_thread = threading.Thread(target=asyncio.get_event_loop().run_until_complete, args=(self.server,))
        server_thread.start()
        time.sleep(3)
        url = 'web_page/html/index.html'
        wb.open(url)

    def handle_connection(self, websocket, path):
        self.websocket = websocket
        while True:
            message = websocket.recv()
            th = threading.Thread(target=process_message, args=[message])
            th.start()

    def send(self, header, ip, text):
        self.websocket.send(f'{header}_/!_{text}(^){ip}')
