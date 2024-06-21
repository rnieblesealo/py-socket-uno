import socket

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = None


def init():
    """
    Initializes client socket
    """

    global client

    # socket behavior is undefined if connect() fails
    # we need to re-create it before retrying!

    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDRESS)
            break
        except socket.error:
            continue

    print('Connection successful!')


def send(msg):
    """
    Sends message to server
    """

    if client is None:
        return

    # encode msg, get len
    msg = msg.encode(FORMAT)
    msg_len = len(msg)

    # make len msg, pad to fit header
    len_msg = str(msg_len).encode(FORMAT)
    len_msg += b' ' * (HEADER - len(len_msg))

    # send server len; then msg of that len
    client.send(len_msg)
    client.send(msg)


def recv() -> str:
    """
    Receive utf-8 string from server
    """

    if client is None:
        return ''

    msg_len = None
    while msg_len is None:
        msg_len = client.recv(HEADER).decode(FORMAT)

    msg_len = int(msg_len)
    msg = client.recv(msg_len).decode(FORMAT)

    return msg


def recv_obj():
    """
    Receive object from server
    """

    if client is None:
        return None

    obj_size = None
    while obj_size is None:
        obj_size = client.recv(HEADER).decode(FORMAT)

    obj_size = int(obj_size)
    obj = client.recv(obj_size)

    return obj
