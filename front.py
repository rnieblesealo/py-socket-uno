# todo: fix player cards dest set incorrectly due to same card object in diff decks
# work on: animations

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

INTERPOLATION_TIME = 0.5


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

        # used for interpolation
        self.target_dest = self.dest.copy()

        # is this card allowed to move by itself?
        self.override_pos = False

    def update(self, dt=1):
        # constantly move towards target dest
        self.dest.x = lerp(
            self.dest.x,
            self.target_dest.x,
            INTERPOLATION_TIME
        )

        self.dest.y = lerp(
            self.dest.y,
            self.target_dest.y,
            INTERPOLATION_TIME
        )

        # print(f"{self.dest.x}, {self.dest.y}")


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
        deck.append((pool[random.randint(0, len(pool) - 1)]))
    return deck


def render_turned_deck(display, deck, ctr, orient):
    """
    Renders a deck of turned cards
    Used to render other player decks
    Can orient to accomodate to screen corners
    """

    if not deck:
        return

    offset = [
        50 if orient == 0 or orient == 2 else 0,
        50 if orient == 1 or orient == 3 else 0
    ]

    oriented_card = turned[orient]

    total_width = oriented_card.get_width() + ((len(deck) - 1) * offset[0])
    total_height = oriented_card.get_height() + ((len(deck) - 1) * offset[1])

    deck_draw_rect = pygame.Rect(
        0,
        0,
        total_width,
        total_height
    )

    deck_draw_rect.center = ctr

    for i in range(len(deck)):
        # if card allowed to move by itself, skip positioning it
        # if deck[i].override_pos:
        deck[i].dest.size = oriented_card.get_size()        # stick to using the target dest ONLY this isn't ok 
        deck[i].dest.topleft = (
            deck_draw_rect.topleft[0] + (i * offset[0]),
            deck_draw_rect.topleft[1] + (i * offset[1])
        )

        display.blit(oriented_card, deck[i].dest)
        pygame.draw.rect(display, (255, 0, 0), deck[i].dest, 2)

    pygame.draw.rect(display, (0, 0, 255), deck_draw_rect, 2)
    pygame.draw.circle(display, (0, 0, 255), ctr, 5)


def render_deck(display, deck, ctr):
    """
    Renders the given set of cards to the display, centered at ctr.
    Can also apply rotation to accomodate for left + right edges and such.
    """

    # ignore empty deck
    if not deck:
        return

    # offset between cards drawn
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

        pygame.draw.rect(display, (0, 255, 0), deck[i].dest, 2)

    pygame.draw.rect(display, (0, 255, 0), deck_draw_rect, 2)
    pygame.draw.circle(display, (0, 255, 0), ctr, 5)


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


def lerp(a, b, t):
    return a * (1 - t) + (b * t)


display = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()
dt = 0

table = import_image('Table_0')

# we have 4 rotated versions of the turned deck card in
# order to draw enemy player decks at diff positions of the screen
# enemy decks should be drawn clockwise
turned = [
    import_image('Deck'),
    pygame.transform.rotate(import_image('Deck', 0.3), 90),     # to left
    pygame.transform.rotate(import_image('Deck', 0.3), 180),    # to top
    pygame.transform.rotate(import_image('Deck', 0.3), 270),    # to right
]

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

print(lerp(0, 1, 0.5))

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

    # update display
    display.fill((0, 0, 0))
    display.blit(table, (0, 0))

    # update clock, get dt in ms
    dt = clock.tick(60) / 1000

    # draw stack
    render_deck(display, stack, display.get_rect().center)

    # THIS IS UNFINISHED!
    # make the game auto-pick draw location of other players

    # draw my deck
    render_deck(
        display,
        player_decks[my_player_number],
        display.get_rect().midbottom
    )

    # animate any cards i hover over
    hovered_card = get_clicked_deck_card(my_deck)
    if my_deck[hovered_card]:
        my_deck[hovered_card].target_dest.y -= 20

    # draw other decks
    render_turned_deck(display, player_decks[1], display.get_rect().midleft, 1)
    render_turned_deck(display, player_decks[2], display.get_rect().midtop, 2)
    render_turned_deck(
        display, player_decks[3], display.get_rect().midright, 3)

    # update all deck cards
    for deck in player_decks:
        for card in deck:
            card.update(dt)

    pygame.display.update()
