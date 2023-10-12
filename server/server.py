import socket as soc
import resources.resources as re
import connect_to_server


def updatePeersList(server_connect: soc.socket):
    re.server_connect = server_connect  # updating the connected socket in resources file
    re.server_given_list = connect_to_server.getUsersInNetwork(server_connect)  # updating the list of server given list of ip's

