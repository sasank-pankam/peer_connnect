import _io
import socket as soc
import sys
import threading as td
import constants
import logs.log


class handleSocket:
    def __init__(self, handle: soc.socket):
        self.client = handle

        self.messages = []  # to store incoming messages

        self.toBeSent_text = []  # texts that are to be sent ( high priority )
        self.toBeSent_Files = []  # files that are to be sent ( low priority )

        self.sending_thread = td.Thread(target=self.sendToClient)
        self.sending_thread.start()

    @staticmethod
    def __getHeaderLength(text: str, *extras):

        length = (' '.join(extras) + ' ' + str(len(text))).encode('utf-8')
        length += b' ' * (64 - len(length))
        return length

    # t text_length - > header
    def sendText(self, text: str):
        self.toBeSent_text.append(('Text-Message', text))

    # f filename -> header
    def sendFile(self, bin_file: _io.BufferedReader):
        with bin_file as bi:
            self.toBeSent_Files.append((bi.readline(), bi.name))

    # a thread of this method is to be created and run at creation of this object
    def sendToClient(self):
        while True:
            # waiting until the text message or file lists are not empty -> to be written
            if self.toBeSent_text:
                self.sendSomething(self.toBeSent_text.pop(0), )
            if self.toBeSent_text:
                self.sendSomething(self.toBeSent_text.pop(0), )
            if self.toBeSent_Files:
                self.sendSomething(self.toBeSent_Files.pop(0), )

    def sendSomething(self, data: tuple):
        content, header = data
        sendlength = handleSocket.__getHeaderLength(content)
        header = (str(sendlength) + header).encode(constants.FORMAT)
        header += b' ' * (constants.HEADER - len(header))

        self.client.send(header)
        if type(content) is not bytes:
            content = content.encode(constants.FORMAT)
        self.client.send(content)

    def reciveSomething(self):
        while True:
            header = self.client.recv(64)
            if not header:
                continue
            header = header.decode(constants.FORMAT).split()

            actContent = self.client.recv(int(header[-1]))

            # # checking header of the message

            if header[0] == 'T':
                self.messages.append(actContent)

            # elif header[0] == 'F':
            #     initiateFileCreation(actContent)
            # elif header[0] == 'FC':
            #     appendFile(actContent)
            if actContent == constants.closing_message:
                break
        self.client.close()
