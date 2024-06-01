import pygame
import random

ASSETS_PATH = 'assets/'
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
    return pygame.transform.scale_by(
        pygame.image.load(ASSETS_PATH + name).convert_alpha(),
        scale
    )


def import_cards():
    cards = []
    scale = 0.3
    for color in COLORS:
        for kind in KINDS:
            info = (
                color,
                kind,
                import_image(
                    f"{color.capitalize()}_{kind.capitalize()}.png",
                    scale
                )
            )

            cards.append(info)

    for kind in WILDS:
        info = (
            'wild',
            kind,
            import_image(
                f"Wild_{kind.capitalize()}.png",
                scale
            )
        )

        cards.append(info)

    return cards


def create_deck(pool, n):
    deck = []
    for i in range(n):
        deck.append(pool[random.randint(0, len(pool) - 1)])
    return deck


def draw_deck(display, deck, ctr):
    offset = (50, 0)

    card_dimensions = (
        deck[0][2].get_width(),
        deck[0][2].get_height()
    )

    total_width = card_dimensions[0] + ((len(deck) - 1) * offset[0])

    draw_rect = pygame.Rect(
        0,
        0,
        total_width,
        card_dimensions[1]
    )

    draw_rect.center = ctr

    # pygame.draw.circle(display, (255, 255, 255), ctr, 5)
    # pygame.draw.rect(display, (255, 255, 255), draw_rect)

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
deck = create_deck(cards, 7)

while True:
    display.fill((0, 0, 0))
    display.blit(table, (0, 0))

    draw_deck(display, deck, display.get_rect().midbottom)

    pygame.display.update()
