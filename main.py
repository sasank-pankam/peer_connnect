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
    return []
    pass


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


async def run(web_socket):
    await web_socket.connect()

    while True:
        message = await web_socket.receive()
        await process_message(message)


def get_credentials():
    with open('credetials.txt', 'r') as fp:
        name = fp.readline()
        return name


def initialize():
    name = get_credentials()

    with re.locks['threads_of_connected_peers']:
        re.threads_of_connected_peers.update(get_peer_list())

    web_socket = wm.WebSocketHandler()
    run(web_socket)

    this_server.managePeers(web_socket, name)
    this_server.makeServer(web_socket, name)


if __name__ == '__main__':
    initialize()

