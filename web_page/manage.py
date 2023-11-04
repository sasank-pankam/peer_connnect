import webbrowser as wb
import constants

import asyncio
import websockets


class WebSocketHandler:
    def __init__(self, url='html/index.html'):
        self.websocket = None
        self.url = url
        wb.open(url)

    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def send(self, text):
        await self.websocket.send(text)

    async def receive(self):
        message = await self.websocket.recv()
        return message
