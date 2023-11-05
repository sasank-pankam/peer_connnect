import threading as td

server_connect = []  # socket connected to main server

server_given_list = []  # list of ip's given by main server

connected_sockets = {}  # dictionary with ip as key sockets that the current device is connected to

threads_of_connected_peers = set()  # threads that are listening to the sockets


def get_locks():
    lis = [
        'threads_of_connected_peers',
        'connected_sockets',
        'server_given_list',
        'server_connect',
    ]
    dic = {}
    for i in lis:
        dic[i] = td.Lock()
    return dic


locks = get_locks()
