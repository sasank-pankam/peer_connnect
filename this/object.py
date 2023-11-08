import os.path
import socket as soc
from web_page import manage as wm
import threading
import time
import constants
import resources.resources as re
import select


def process(obj, header: list, content) -> bool:
    print(header, content)
    try:
        if header[0] == 'TEXT':
            wm.send('thisisamessage', obj.ip, content.decode(constants.FORMAT))
        elif header[0] == 'FILE':
            with open(f'{re.directory}/{header[1]}', 'ab') as fp:
                fp.write(content)

        elif header[0] == 'FILE-COMPLETED':
            wm.send('thisisafile', obj.ip, header[1])

        elif header[0] == 'CLOSE-CONNECTION':
            wm.send('thisisacommand', obj.ip, constants.closing_message)
            with re.locks['connected_sockets']:
                re.connected_sockets.pop(obj.ip)
            obj.bool_var = False

    except Exception as e:
        print('Unable to process a message due to', e)
    return True


class handleSocket:
    sender_name = None

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
        print(self.name)
        wm.send('thisisausername', self.ip, self.name)
        # try:
        # # -------------------------------------------------------------------
        # except:
        #     pass
        # -------------------------------------------------------------------
        print('wejl')

    @staticmethod
    def __getHeader(text: str | bytes, *extras):

        header = (' '.join(extras) + ' ' + str(len(text))).encode('utf-8')
        header += b' ' * (64 - len(header))
        return header

    # t text_length - > header
    def sendText(self, text: str):
        with self.client_lock:
            self.client.send(handleSocket.__getHeader(text, 'TEXT'))
            self.client.send(text.encode(constants.FORMAT))

    def _sendFile(self, file_path: str):
        print('sendFile', file_path)
        with open(file_path.strip(), 'rb') as fp:
            name = os.path.basename(file_path)
            while content := fp.readline():
                with self.client_lock:
                    self.client.send(handleSocket.__getHeader(content, f'FILE {name}'))
                    self.client.send(content)
                    time.sleep(0.01)
            with self.client_lock:
                self.client.send(handleSocket.__getHeader(b'', f'FILE-COMPLETED {name}'))

    def sendFile(self, file_path: str):
        threading.Thread(target=self._sendFile, args=(file_path,)).start()

    def receiveSomething(self):
        try:
            while self.bool_var:
                print(f'{self.ip}\'s bool_var : ---->> {self.bool_var}')
                readable, _, _ = select.select([self.client], [], [], 0.001)

                if self.client in readable:
                    header = self.client.recv(64)
                    if not header:
                        continue
                    header = header.decode(constants.FORMAT).split()

                    actContent = self.client.recv(int(header[-1]))

                    # processing and exiting the loop
                    process(self, header, actContent)
                    time.sleep(0.01)

            self.client.send(constants.closing_message.encode(constants.FORMAT))
            self.client.close()
        except Exception as e:
            print('ERROR IN RECIVING FILE from', self.ip)
            wm.send('thisisacommand', self.ip, constants.closing_message)
