import socket as soc
import constants


def changeToIP(raw_str: str) -> tuple:
    raw_str = raw_str.split(':')
    return raw_str[0], int(raw_str[1])


# FORMAT ==> ip_address:port number1,ip_address:port number2,....ip_address:port number n
# converted to list[ tuple( ip , port) ]
def getUsersInNetwork(server_connecting_socket: soc.socket) -> list[tuple]:

    length = server_connecting_socket.recv(constants.HEADER)
    length = int(length.decode(constants.FORMAT))
    devices_list = server_connecting_socket.recv(length).decode(constants.FORMAT)
    devices_list = devices_list.split(',')

    return list(map(changeToIP, devices_list))
