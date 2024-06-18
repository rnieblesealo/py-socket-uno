import socket

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def init():
    # start client
    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)

def send(msg):
    # encode msg, get len
    msg = msg.encode(FORMAT)
    msg_len = len(msg)

    # make len msg, pad to fit header
    len_msg = str(msg_len).encode(FORMAT)
    len_msg += b' ' * (HEADER - len(len_msg))

    # send server len; then msg of that len
    client.send(len_msg)
    client.send(msg)
