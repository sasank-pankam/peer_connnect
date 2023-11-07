import threading as td

server_connect = []  # socket connected to main server

server_given_list = []  # list of ip's given by main server

connected_sockets = {}  # dictionary with ip as key sockets that the current device is connected to

threads_of_connected_peers = []  # threads that are listening to the sockets

directory = ''


def get_locks():
    global directory
    lis = [
        'threads_of_connected_peers',
        'connected_sockets',
        'server_given_list',
        'server_connect',
        'directory'
    ]
    dic = {}
    for i in lis:
        dic[i] = td.Lock()
    with open('./credentials.txt', 'r') as fp:
        _, _, directory = fp.readline(), fp.readline(), fp.readline()
    return dic


locks = get_locks()
