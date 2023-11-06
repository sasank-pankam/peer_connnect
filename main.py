import socket
import sys
import threading

import resources.resources as re
import web_page.manage as wm
import this.server as this_server
import signal

server_socket = None

async def getMessagesFromScript(websocket, path):
    
    await websocket.send("2ef7bde608ce5404e97d5f042f95f89f1c232871")
    async for message in websocket:
        temp = message.split('_/!_')
        if temp[0] == "thisisausername":
            global user_name
            user_name = temp[1]
            print("user name: " + user_name)
        elif temp[0] == "thisisamessage":
            temp = temp[1].split("~^~")
            print("from "+user_name+" message: " + temp[0] + " to " + temp[1])

def get_peer_list(ip) -> list[tuple[str, str]]:

    initial_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(ip)
    initial_server_socket.connect((ip, 12345))
    msg = b'list'
    msg = msg + b' ' * (64 - len(msg))
    initial_server_socket.send(msg) #changed
   
    else:
        print(k)
        str_ip = initial_server_socket.recv(int(k.decode()))
    lis_ip = eval(str_ip)
    server_socket = initial_server_socket
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


def initialize():
    global current_server, acceptor_thread, exit_event
    name, ip = get_credentials()
    ip = ip.strip()
    with re.locks['server_given_list']:
        re.server_given_list.extend(get_peer_list(ip))
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
