import webbrowser as wb
import constants

import asyncio
import websockets


class WebSocketHandler:
    def __init__(self, url='web_page/html/index.html'):
        self.websocket = None
        self.url = url
        wb.open(url)

    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def send(self, ip, text):
        string = f'TEXT {ip} {text}'
        await self.websocket.send(string)

    async def receive(self):
        message = await self.websocket.recv()
        return message
