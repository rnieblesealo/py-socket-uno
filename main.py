# next activity is to draw other player stacks in diff positions on the screen
# also include a check for a violation of max players

import pygame
import random
import sys

ASSETS_PATH = 'assets'
DISPLAY_SIZE = (1280, 720)

KINDS = (
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
    'skip'
)

COLORS = (
    'red',
    'green',
    'blue',
    'yellow',
)

WILDS = {
    'wild',
    'draw'
}


INVALID_START_KINDS = [
    'draw',
    'reverse',
    'skip',
    'wild'
]

MAX_PLAYERS = 4

display = pygame.display.set_mode(DISPLAY_SIZE)


class Card:
    def __init__(self, image, color, kind):
        self.image = image
        self.color = color
        self.kind = kind

        # store position and everything within this dest rect
        self.dest = pygame.Rect(
            0,
            0,
            image.get_width(),
            image.get_height()
        )


def import_image(name, scale=1):
    """
    Shorthand for importing alpha-converted png image in ASSET_PATH.
    """

    return pygame.transform.scale_by(
        pygame.image.load(f"{ASSETS_PATH}/{name}.png").convert_alpha(),
        scale
    )


def import_cards():
    """
    Loads all cards according to info in KINDS, COLORS, and WILDS.
    Format is (color, kind, image).
    """

    cards = []
    scale = 0.3
    for color in COLORS:
        for kind in KINDS:
            # assemble card from data
            card = Card(
                import_image(
                    f"{color.capitalize()}_{kind.capitalize()}",
                    scale
                ),
                color,
                kind,
            )

            # append card data
            cards.append(card)

    # wildcards need special treatment since they don't share same kinds
    for kind in WILDS:
        card = Card(
            import_image(
                f"Wild_{kind.capitalize()}",
                scale
            ),
            'wild',
            kind,
        )

        cards.append(card)

    return cards


def generate_deck(pool, n):
    """
    Draws n cards from given pool.
    """

    deck = []
    for i in range(n):
        deck.append(pool[random.randint(0, len(pool) - 1)])
    return deck


def render_deck(display, deck, ctr):
    """
    Renders the given set of cards to the display, centered at ctr.
    """

    # ignore empty deck
    if not deck:
        return

    # position difference between drawing of current card and the next
    offset = (50, 0)

    # assume first card in deck has the dimensions of the rest
    card_dimensions = (
        deck[0].image.get_width(),
        deck[0].image.get_height()
    )

    # get width required to draw entire deck
    total_width = card_dimensions[0] + ((len(deck) - 1) * offset[0])

    # make dest draw rect for easy draw pos manipulation
    deck_draw_rect = pygame.Rect(
        0,
        0,
        total_width,
        card_dimensions[1]
    )

    # move draw rect to desired center
    deck_draw_rect.center = ctr

    # position each card over where it needs to go in the deck
    # draw every card's image component
    for i in range(len(deck)):
        deck[i].dest.topleft = (
            deck_draw_rect.topleft[0] + (i * offset[0]),
            deck_draw_rect.topleft[1] + (i * offset[1])
        )

        display.blit(deck[i].image, deck[i].dest)

        pygame.draw.rect(display, (0, 0, 0), deck[i].dest, 2)


def get_clicked_deck_card(deck) -> Card:
    """
    Check if mouse position is within the dest rect of any card in our deck
    Returns card index in deck if match found, otherwise -1
    """

    # loop goes in reverse to prioritize upper cards in deck stack
    # this is reflected visually! makes more sense if u look at it

    mouse_pos = pygame.mouse.get_pos()
    i = len(deck) - 1
    for card in reversed(deck):
        if card.dest.collidepoint(mouse_pos):
            return i
        i -= 1
    return -1


def pick_start_card(cards):
    """
    Get valid start card from within given list
    Returns the index
    """

    # return -1 for empty card list
    if not cards:
        return -1

    # pick a random start card
    i = random.randint(0, len(cards) - 1)

    # keep picking if invalid kind
    if cards[i].kind in INVALID_START_KINDS:
        return pick_start_card(cards)
    return i


def move(i, a, b):
    """
    Moves item at a's i-th index to the top of b
    Ideally used to move cards between stacks
    """

    taken = a.pop(i)
    b.append(taken)


table = import_image('Table_0')
cards = import_cards()

player_decks = [
    generate_deck(cards, 7),
    generate_deck(cards, 7),
    generate_deck(cards, 7),
    generate_deck(cards, 7),
]

my_player_number = 0
my_deck = player_decks[my_player_number]

stack = [
    cards[pick_start_card(cards)]
]


while True:
    # we need pygame.event.get() for anything event-related to be processed
    # anywhere
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # move clicked card to stack
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_idx = get_clicked_deck_card(my_deck)

            # disallow action if no valid click
            if clicked_idx == -1:
                continue

            # compare clicked card and latest in deck
            clicked = my_deck[clicked_idx]
            latest = stack[-1]

            conditions = [
                len(stack) == 0,                    # stack empty
                (clicked.kind == latest.kind),      # kinds match
                (clicked.color == latest.color),    # colors match
            ]

            # if any conditions are true, allow play
            if True in conditions:
                move(clicked_idx, my_deck, stack)

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()

    display.fill((0, 0, 0))
    display.blit(table, (0, 0))

    # draw stack
    render_deck(display, stack, display.get_rect().center)

    # draw player decks
    for deck in player_decks:
        render_deck(display, deck, display.get_rect().midbottom)

    pygame.display.update()
