import pygame
import random

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

display = pygame.display.set_mode(DISPLAY_SIZE)


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
            # assemble card data
            info = (
                color,
                kind,
                import_image(
                    f"{color.capitalize()}_{kind.capitalize()}",
                    scale
                )
            )

            # append card data
            cards.append(info)

    # wildcards need special treatment since they don't share same kinds
    for kind in WILDS:
        info = (
            'wild',
            kind,
            import_image(
                f"Wild_{kind.capitalize()}",
                scale
            )
        )

        cards.append(info)

    return cards


def draw_cards(pool, n):
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

    # position difference between drawing of current card and the next
    offset = (50, 0)

    # assume first card in deck has the dimensions of the rest
    card_dimensions = (
        deck[0][2].get_width(),
        deck[0][2].get_height()
    )

    # width required to draw entire deck
    total_width = card_dimensions[0] + ((len(deck) - 1) * offset[0])

    # make dest draw rect for easy draw pos manipulation
    draw_rect = pygame.Rect(
        0,
        0,
        total_width,
        card_dimensions[1]
    )

    # move draw rect to center
    draw_rect.center = ctr

    # debug draw
    # pygame.draw.circle(display, (255, 255, 255), ctr, 5)
    # pygame.draw.rect(display, (255, 255, 255), draw_rect)

    # draw every card's image component
    # it is stored at the third element of its info tuple
    for i in range(len(deck)):
        display.blit(
            deck[i][2],
            (
                draw_rect.topleft[0] + (i * offset[0]),
                draw_rect.topleft[1] + (i * offset[1])
            )
        )


table = import_image('Table_0.png')
cards = import_cards()
deck = draw_cards(cards, 7)

while True:
    display.fill((0, 0, 0))
    display.blit(table, (0, 0))

    render_deck(display, deck, display.get_rect().midbottom)

    pygame.display.update()
