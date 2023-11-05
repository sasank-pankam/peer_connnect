import socket
import sys
import resources.resources as re
import web_page.manage as wm
import this.server as this_server


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


def initialize():
    name, ip = get_credentials()

    with re.locks['server_given_list']:
        re.server_given_list.extend(get_peer_list(ip))
        print(re.server_given_list)
    web_socket = wm.WebSocketHandler()

    this_server.managePeers(web_socket, name)
    this_server.makeServer(web_socket, name)


if __name__ == '__main__':
    validate_arguments(sys.argv)
    initialize()
