import random

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


def make_card(kind, value):
    """
    Return tuple containing card info with given values
    """

    return (
        kind,
        value
    )


def make_pool():
    """
    Generate a shuffled pool with all cards in UNO
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


def start_game(pool, stack, players):
    """
    Begins a new uno game by:

    1. Generating card pool
    2. Generating player card arrays
    3. Drawing 7 topmost cards for every player
    4. Moving remaining topmost element in pool to stack
    """

    pool = make_pool()
    players = []

    for i in range(PLAYERS):
        players.append([])
        draw_cards(pool, players[i], START_CARDS)

    stack = [pool.pop()]

    print('Started new game!')

    print('Pool:')
    for card in pool:
        print(card)

    print('Player decks:')
    for i in range(PLAYERS):
        print(f'Player {i}:')
        for card in players[i]:
            print(card)

    print('Stack:')
    for card in stack:
        print(card)


# --- main game ---

pool = None
stack = None
players = None

start_game(pool, stack, players)
