import socket
import sys
import threading

import resources.resources as re
import web_page.manage as wm
import this.server as this_server
import signal

server_socket = None


def get_peer_list(ip) -> list[tuple[str, str]]:

    initial_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    initial_server_socket.connect((ip, 12345))
    msg = b'list'

    msg = msg + b' ' * (64 - len(msg))
    initial_server_socket.send(msg)

    if not (k := initial_server_socket.recv(64)):
        size = initial_server_socket.recv(64)
        str_ip = initial_server_socket.recv(int(size.decode()))
    else:
        print(k)
        str_ip = initial_server_socket.recv(int(k.decode()))
    print(str_ip)
    lis_ip = eval(str_ip)
    server_socket = initial_server_socket

    return lis_ip


def validate_arguments(arguments: list[str]):
    with open('credentials.txt', 'r') as fp:
        lis = fp.readlines()

    for ind in range(1, len(arguments)):
        t = arguments[ind].split('=')
        if t[0] == '--name':
            lis[0] = t[1]
        elif t[0] == '--dir':
            lis[2] = t[1]
        elif t[0] == '--ip':
            lis[1] = t[1]

    with open('credentials.txt', 'w') as fp:
        fp.writelines(lis)


def get_credentials():
    with open('credentials.txt', 'r') as fp:
        name, ip = fp.readline(), fp.readline()
        return name, ip


current_server = None
acceptor_thread = None
exit_event = threading.Event()


def initialize():
    global current_server, acceptor_thread, exit_event
    name, ip = get_credentials()
    ip = ip.strip()
    list_peers = get_peer_list(ip)

    with re.locks['server_given_list']:
        re.server_given_list.extend(list_peers)
        print(re.server_given_list)
    web_socket = wm.WebSocketHandler()

    this_server.managePeers(web_socket, name)
    current_server, acceptor_thread = this_server.makeServer(web_socket, name, exit_event)


def signal_handler(signum, frame):
    global current_server, exit_event, acceptor_thread
    print('Exiting the programme')
    for ip, obj in re.connected_sockets.items():
        obj.bool_var = False
    if not (current_server is None or exit_event is None or acceptor_thread is None):
        exit_event.set()
        acceptor_thread.join()
        current_server.close()
    msg = b'exit'
    msg = msg + b' ' * (64 - len(msg))
    server_socket.send(msg)
    exit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    validate_arguments(sys.argv)
    initialize()
