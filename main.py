import socket as soc
import constants
import resources.resources as re
import threading as td
from logs import log
import this.server as this_server


def get_peer_list(ip, subnet):
    """
    return list of all ip addresses of that ip address
    then checking that the same application is running on the other side
    -- i think it's not a good idea but for now let it be
    """
    pass

def initialize():
    re.server_given_list.extend(get_peer_list())
    this_server.managePeers()
    this_server.makeServer()


if __name__ == '__main__':
    initialize()
