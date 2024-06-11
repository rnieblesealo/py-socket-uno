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

    # --- main game ---


pool = make_pool()
players = []

for i in range(PLAYERS):
    players.append([])
    draw_cards(pool, players[i], START_CARDS)

stack = [pool.pop()]

print('\nSTARTED NEW GAME!')

print('\nPOOL:\n')
for card in pool:
    print(card)

print('\nPLAYER DECKS:')
for i in range(PLAYERS):
    print(f'\nPlayer {i}:\n')
    for card in players[i]:
        print(card)

print('\nSTACK:\n')
for card in stack:
    print(card)

turn = 0

print('\n---')

while True:
    print(f'\nSTACK TOP: {stack[-1]}')

    print('\nYOUR CARDS:\n')
    for card in players[turn]:
        print(card)

    sel = int(input(f'\n[Player {turn}]: Enter index of card to play: '))

    try:
        if is_valid_play(stack[-1], players[turn][sel]):
            move_card(players[turn], stack, sel)

            print(f'\nMoved {stack[-1]} from player {turn} deck!')
        else:
            print('\nInvalid play! Try again')

    except IndexError:
        print("\nYou can't pick that card! Try again")
