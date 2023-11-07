import socket
import sys
import threading
import resources.resources as re
import web_page.manage as wm
import this.server as this_server
import signal


def get_peer_list(ip) -> list[tuple[str, str]]:

    try:
        initial_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('Getting peers in the network')
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
        lis_ip = eval(str_ip)

        initial_server_socket.close()
    except Exception as e:
        print('Error in connecting to server for peers in the network')
        return False

    return lis_ip


def validate_arguments(arguments: list[str]):
    for ind in range(1, len(arguments)):
        t = arguments[ind].split('=')
        if t[0] == '--name':
            with open('credentials.txt', 'r') as fp:
                lis = fp.readlines()
                lis[0] = t[1]
            with open('credentials.txt', 'w') as fp:
                fp.writelines(lis)


def get_credentials():
    with open('credentials.txt', 'r') as fp:
        name, ip = fp.readline(), fp.readline()
        return name, ip


current_server = None
acceptor_thread = None
exit_event = threading.Event()
server_ip = None


def sodi(name, exit_event):
    global current_server, acceptor_thread
    current_server, acceptor_thread = this_server.makeServer(name, exit_event)


def initialize():
    global current_server, acceptor_thread, exit_event, server_ip
    name, ip = get_credentials()
    ip = ip.strip()
    server_ip = ip
    if not (peer_list := get_peer_list(ip)) and type(peer_list) is bool:
        return

    with re.locks['server_given_list']:
        re.server_given_list.extend(peer_list)
        print(re.server_given_list)
    td1 = threading.Thread(target=this_server.managePeers, args=[name])
    td2 = threading.Thread(target=sodi, args=[name, exit_event])
    td1.start()
    td2.start()

    wm.make_server(name)


def signal_handler(signum, frame):
    global current_server, exit_event, acceptor_thread
    print('Exiting the programme')

    for ip, obj in re.connected_sockets.items():
        obj.bool_var = False
    if not (current_server is None or exit_event is None or acceptor_thread is None):
        exit_event.set()
        acceptor_thread.join()
        current_server.close()

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((server_ip, 12345))

        msg = b'exit'
        msg = msg + b' ' * (64 - len(msg))
        server.send(msg)
    except Exception:
        pass


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    validate_arguments(sys.argv)
    initialize()
