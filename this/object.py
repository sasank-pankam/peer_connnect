import os.path
import socket as soc
import threading as td
import constants
import web_page.manage as wb


class handleSocket:
    sender_name = None

    def process(self, header: list, content) -> bool:

        try:
            if header[0] == 'TEXT':
                self.web_page.send(self.ip, content)
            elif header[0] == 'FILE':
                with open(header[1], 'ab') as fp:
                    fp.write(content)
        except Exception as e:
            return False
        return True

    def __init__(self, handle: soc.socket, ip: str, web_page: wb.WebSocketHandler, name: str):
        self.sender_name = name
        self.client = handle
        self.web_page = web_page

        # -------------------------------------------------------------------
        if not (h := self.client.recv(64)):
            self.name = self.client.recv(64).decode(constants.FORMAT).split()[-1]
        else:
            self.name = h.decode(constants.FORMAT).split()[-1]

        # -------------------------------------------------------------------

        self.ip = ip

    @staticmethod
    def __getHeader(text: str | bytes, *extras):

        header = (' '.join(extras) + ' ' + str(len(text))).encode('utf-8')
        header += b' ' * (64 - len(header))
        return header

    # t text_length - > header
    def sendText(self, text: str):
        self.client.send(handleSocket.__getHeader(text, 'TEXT'))
        self.client.send(text)

    def sendFile(self, file_path: str):
        name = os.path.basename(file_path)
        with open(file_path, 'rb') as fp:
            content = fp.readline()
            self.client.send(handleSocket.__getHeader(content, f'FILE {name}'))
            self.client.send(content)

    def receiveSomething(self):
        while True:
            header = self.client.recv(64)
            if not header:
                continue
            header = header.decode(constants.FORMAT).split()

            actContent = self.client.recv(int(header[-1]))

            # processing and exiting the loop
            if not self.process(header, actContent):
                break
        self.client.close()
