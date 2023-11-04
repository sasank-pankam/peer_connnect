server_connect = []  # socket connected to main server

server_given_list = []  # list of ip's given by main server

connected_sockets = {}  # dictonary with ip as key sockets that the current device is connected to

threds_of_connected_peers = set()  # threads that are listening to the sockets

alive_connections = []  #

this_server_accept = None  # thread that will accept new clients

