import socket
import random
import threading

# -- connectivity --

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # get ipv4 from hostname
ADDRESS = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = None
conns = []

def init():
    """
    Initialize host server
    """

    global r

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)

def handle_client(conn):
    """
    Listen for messages from a given connection
    """

    connected = True
    while connected:
        # discard null messages
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if not msg_len:
            continue

        # receive message
        msg_len = int(msg_len)
        msg = conn.recv(msg_len).decode(FORMAT)

        if (msg == DISCONNECT_MESSAGE):
            connected = False
            break

    conn.close()

def get_connections():
    """
    Listen for connections and store their info in conns
    """

    if server is None:
        return

    server.listen()
    while True:
        # store conn in arr
        conn, addr = server.accept()
        conns.append((conn, addr))

        # begin new thread for this conn
        thread = threading.Thread(
            target=handle_client, args=(conn, addr))

        thread.start()

# -- game --

PLAYERS = 4
START_CARDS = 7

VALUES = (
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'draw',
    'reverse',
    'skip',
    'wild'
)

KINDS = (
    'red',
    'green',
    'blue',
    'yellow',
    'wild',
)

card_pool = None
card_stack = None
player_turn = 0
player_decks = []

def make_card(kind, value) -> tuple[str, str]:
    return (
        kind,
        value
    )

def make_pool() -> list:
    """
    Generate every possible card into a list, shuffle, and return it
    """

    pool = []

    for kind in KINDS:
        if kind == 'wild':
            # there's only 2 wildcards, compensate for this case
            pool.append(make_card(kind, 'draw'))
            pool.append(make_card(kind, 'wild'))
            pass
        else:
            for value in VALUES:
                pool.append(make_card(kind, value))

    random.shuffle(pool)

    return pool

def move_card(src, dest, index=-1):
    """
    Move a card from a source to a destination
    May specifiy index, otherwise topmost is used
    """

    taken = src.pop() if index == -1 else src.pop(index)
    dest.append(taken)

def draw_cards(src, dest, amt):
    """
    Moves @amt cards from the top of the source to the dest
    """

    for i in range(amt):
        dest.append(src.pop())

def start_game():
    """
    Initializes all game data
    """

    global card_pool
    global card_stack
    global player_decks

    card_pool = make_pool()

    for i in range(len(conns)):
        player_decks.append([])
        draw_cards(card_pool, player_decks[i], START_CARDS)

    card_stack = [card_pool.pop()]

    print('\nCard pool:\n')
    for card in card_pool:
        print(card)

    print('\nPlayer decks:')
    for i in range(len(player_decks)):
        print(f'\nPlayer {i}:\n')
        for card in player_decks[i]:
            print(card)

    print('\nStack:\n')
    for card in card_stack:
        print(card)

    print('\n---')

def is_valid_play(top, card):
    """
    Evaluates a top card against selected card
    Return True if card can be placed after top following UNO rules

    """

    conditions = [
        top[0] == card[0],  # top kinds match
        top[1] == card[1]   # top values match
    ]

    return True in conditions
