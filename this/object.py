import _io
import socket as soc
import sys

import constants
import logs.log


def handleText(actContent):
    pass


def initiateFileCreation(actContent):
    pass


def appendFile(actContent):
    pass


class handleSocket:
    def __init__(self, handle: soc.socket):
        self.client = handle
        self.fp = open(f'../logs/test/{self.client.getpeername()}.txt', 'a')

    @staticmethod
    def __getHeaderLength(text: str, *extras):

        lenght = (' '.join(extras) + ' ' + str(len(text))).encode('utf-8')
        lenght += b' ' * (64 - len(lenght))
        return lenght

    # t text_length - > header
    def sendText(self, text: str) -> bool:
        try:
            self.client.send(handleSocket.__getHeaderLength(text, 't'))
            self.client.send(text.encode('utf-8'))
        except Exception as e:
            logs.log.writeLogTextTransferErrors(str(e))
            return False
        return True

    # f filename -> header
    def sendFile(self, bin_file: _io.BufferedReader, start=None, end=None) -> bool:
        name = bin_file.name
        lines = []
        if start is None:
            start = 0
        if end is None:
            end = sys.maxsize
        try:
            while start <= end:
                line = bin_file.readline()
                if line is None:
                    break
                lines.append(line)
                start += 1

            content = b''.join(lines)
            header = f'f~{bin_file.name}'

            self.client.send(handleSocket.__getHeaderLength(header))
            self.client.send(header.encode('utf-8'))
            self.client.send(handleSocket.__getHeaderLength(content.decode('utf-8')))
            self.client.send(content)
        except Exception as e:
            logs.log.writeLogFileSharingErrors(str(e))
            return False
        return True

    def wirte(self, string: str):
        self.fp.write(string)

    def reciveSomething(self):
        while True:
            header = self.client.recv(64)
            if not header:
                continue
            header = header.decode(constants.FORMAT).split()

            actContent = self.client.recv(int(header[-1]))
            # # checking header of the message
            # if header[0] == 'T':
            #     handleText(actContent)
            # elif header[0] == 'F':
            #     initiateFileCreation(actContent)
            # elif header[0] == 'FC':
            #     appendFile(actContent)
            if actContent == 'exit':
                break
            self.wirte(actContent.decode(constants.FORMAT))
