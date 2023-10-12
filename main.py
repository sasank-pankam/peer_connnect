# import socket as soc
# import constants
# import resources.resources as re
# import threading as td
# from logs import log
# import server.server as server
import this.server as this_server


def initialize():
    # main_server_ip = constants.SERVER_IP
    # main_server_port = constants.SERVER_PORT
    #
    # mian_server_socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
    # mian_server_socket.connect((main_server_ip, main_server_port))
    #
    # log.writeLogMainServer(
    #     f'Connected to the server with server.ip = {main_server_ip}:{main_server_port} and client.ip = {soc.gethostbyname(soc.gethostname())}')
    #
    # server.updatePeersList(mian_server_socket)
    this_server.managePeers()
    this_server.makeServer()


if __name__ == '__main__':
    initialize()
