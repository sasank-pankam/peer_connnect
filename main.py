import asyncio

import resources.resources as re
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


def get_credentials():
    with open('credentials.txt', 'r') as fp:
        name = fp.readline()
        return name


def initialize():
    name = get_credentials()

    with re.locks['threads_of_connected_peers']:
        re.threads_of_connected_peers.update(get_peer_list())

    web_socket = wm.WebSocketHandler()

    this_server.managePeers(web_socket, name)
    this_server.makeServer(web_socket, name)


if __name__ == '__main__':
    initialize()

