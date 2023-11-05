import socket
import sys
import threading

import resources.resources as re
import web_page.manage as wm
import this.server as this_server
import signal


def get_peer_list(ip) -> list[tuple[str, str]]:
    initial_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    initial_server_socket.connect((ip, 8095))
    if not (k := initial_server_socket.recv(64)):
        what_is_size = initial_server_socket.recv(64)
        str_ip = initial_server_socket.recv(int(what_is_size.decode()))
    else:
        print(k)
        str_ip = initial_server_socket.recv(int(k.decode()))
    lis_ip = eval(str_ip)
    initial_server_socket.close()
    return lis_ip


def validate_arguments(arguments: list):
    pass
    

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

    with re.locks['server_given_list']:
        re.server_given_list.extend(get_peer_list(ip))
        print(re.server_given_list)
    web_socket = wm.WebSocketHandler()

    this_server.managePeers(web_socket, name)
    current_server, acceptor_thread = this_server.makeServer(web_socket, name, exit_event)


def signal_handler():
    global current_server, exit_event, acceptor_thread
    print('Exiting the programme')
    for ip, obj in re.connected_sockets.items():
        obj.bool_var = False
    if not (current_server and exit_event and acceptor_thread):
        exit_event.set()
        acceptor_thread.join()
        current_server.close()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    validate_arguments(sys.argv)
    initialize()
