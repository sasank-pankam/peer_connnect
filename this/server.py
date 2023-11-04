import socket as soc
from . import object as obj
import resources.resources
import threading as td
import resources.resources as re
import logs.log as log


def get_local_ip_address():
    try:
        s = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))

        local_ip_address = s.getsockname()[0]
        s.close()

        return local_ip_address
    except Exception as e:
        return str(e)


def connectPeers(web_socket) -> dict[obj.handleSocket]:
    lis = {}  # list of peer sockets
    if re.server_given_list:
        for addr in re.server_given_list:
            peer = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
            try:
                peer.connect(addr)
                lis[addr] = obj.handleSocket(peer, addr, web_socket)
            except OSError as oe:
                log.writeLogPeerConnectionErrors(str(oe))
    return lis


def managePeers(web_socket):
    peers = connectPeers(web_socket)

    threds = [td.Thread(target=peers[x].receiveSomething) for x in peers]

    for i in threds:
        i.start()

    re.connected_sockets.update(peers)
    re.threds_of_connected_peers.update(threds)


def makeServer(web_socket) -> tuple[soc.socket, td.Thread]:
    server_ip = get_local_ip_address()
    server_port = 7070

    this_server_socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
    this_server_socket.bind((server_ip, server_port))

    t1 = td.Thread(target=acceptPeers, args=[this_server_socket, web_socket])
    t1.start()
    return this_server_socket, t1


def acceptPeers(server: soc.socket, web_socket):
    server.listen()
    print(f'Listening for connections at {server.getsockname()} ')
    while True:
        new_client, new_client_address = server.accept()
        resources.resources.connected_sockets[new_client_address] = (
            peer := obj.handleSocket(new_client, new_client_address, web_socket))
        re.threds_of_connected_peers.add(peer := td.Thread(target=peer.receiveSomething))
        peer.start()
