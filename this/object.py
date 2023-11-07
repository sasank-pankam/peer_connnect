import socket as soc
from web_page import manage as wm
import threading
import time
import asyncio
import constants
import resources.resources as re


class handleSocket:
    sender_name = None

    def process(self, header: list, content) -> bool:

        try:
            if header[0] == 'TEXT':
                wm.send('thisisamessage', self.ip, content.decode(constants.FORMAT))
            elif header[0] == 'FILE':
                with open(f'{re.directory}/{header[1]}', 'ab') as fp:
                    fp.write(content)
            elif header[0] == 'FILE-COMPLETED':
                wm.send('compleatedafiletransfer', self.ip, header[1])
            elif header[0] == 'CLOSE':
                wm.send('thisisacommand', self.ip, constants.closing_message)
                self.bool_var = False

        except Exception as e:
            print('Unable to process a message due to', e)
        return True

    def __init__(self, handle: soc.socket, ip: str, name: str):
        self.sender_name = name
        self.client = handle
        self.ip = ip
        self.client_lock = threading.Lock()
        self.bool_var = True

        if not (h := self.client.recv(64)):
            self.name = self.client.recv(64).decode(constants.FORMAT).strip()
        else:
            self.name = h.decode(constants.FORMAT).strip()

        # -------------------------------------------------------------------
        asyncio.get_event_loop().run_until_complete(wm.send('thisisausername', self.ip, self.name))
        # -------------------------------------------------------------------

    @staticmethod
    def __getHeader(text: str | bytes, *extras):

        header = (' '.join(extras) + ' ' + str(len(text))).encode('utf-8')
        header += b' ' * (64 - len(header))
        return header

    # t text_length - > header
    def sendText(self, text: str):
        with self.client_lock:
            self.client.send(handleSocket.__getHeader(text, 'TEXT'))
            self.client.send(text)

    def _sendFile(self, file_path: str):
        with open(file_path, 'rb') as fp:
            name = fp.name
            while content := fp.readline():
                with self.client_lock:
                    self.client.send(handleSocket.__getHeader(content, f'FILE {name}'))
                    self.client.send(content)
                    time.sleep(0.01)

    def sendFile(self, file_path: str):
        threading.Thread(target=self._sendFile, args=(file_path,)).start()

    def receiveSomething(self):
        while self.bool_var:
            header = self.client.recv(64)
            if not header:
                continue
            header = header.decode(constants.FORMAT).split()

            actContent = self.client.recv(int(header[-1]))

            # processing and exiting the loop
            self.process(header, actContent)
            time.sleep(0.01)
        self.client.send(constants.closing_message.encode(constants.FORMAT))
        self.client.close()
