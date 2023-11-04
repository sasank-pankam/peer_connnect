import socket as soc
import constants
import resources.resources as re
import threading as td
from logs import log
import web_page.manage as wm
import this.server as this_server


def get_peer_list():
    """
    return list of all ip addresses of that ip address
    then checking that the same application is running on the other side
    -- i think it's not a good idea but for now let it be
    """
    pass


def send_message(ip, text):
    re.connected_sockets[ip].sendText(text)


async def process_message(message):
    message = message.split()
    if message[0] == 'TEXT':
        ip = message[1]
        send_message(ip, message[-1])
    if message[0] == 'CMD':
        pass


async def run(web_socket):
    await web_socket.connect()

    while True:
        message = await web_socket.receive()
        await process_message(message)


def initialize():
    re.server_given_list.extend(get_peer_list())

    web_socket = wm.WebSocketHandler()
    run(web_socket)

    this_server.managePeers(web_socket)
    this_server.makeServer(web_socket)


if __name__ == '__main__':
    initialize()

