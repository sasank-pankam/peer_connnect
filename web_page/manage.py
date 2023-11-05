import time
import threading
import webbrowser as wb
import resources.resources as re
import asyncio
import websockets


def send_message(ip, text):
    with re.locks['connected_sockets']:
        re.connected_sockets[ip.strip()].sendText(text)


async def process_message(message):
    message = message.split()
    if message[0] == 'TEXT':
        ip = message[1]
        send_message(ip, message[-1])
    if message[0] == 'CMD':
        pass


class WebSocketHandler:
    def __init__(self, url='web_page/html/index.html'):
        self.websocket = None
        self.server = websockets.serve(self.handle_connection, 'localhost', 12345)
        server_thread = threading.Thread(target=asyncio.get_event_loop().run_until_complete, args=(self.server,))
        server_thread.start()
        wb.open(url)
        time.sleep(3)

    def handle_connection(self, websocket, path):
        self.websocket = websocket
        while True:
            message = websocket.recv()
            th = threading.Thread(target=process_message, args=[message])
            th.start()

    def send(self, ip, text):
        self.websocket.send(f'TEXT {ip} {text}')
