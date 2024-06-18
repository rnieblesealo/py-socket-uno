import threading
import pickle
import server
import client

def await_input(msg, valid_entries):
    """
    Waits for user to enter valid option, re-prompting entry otherwise
    """

    while True:
        s = input(msg).lower()
        if s in valid_entries:
            return s
        print("Try again!")

# decide if we want to host or join
is_host = False
game_started = False

sel = await_input(
    msg='Would you like to host game? (y/n): ',
    valid_entries=('y', 'n')
)

is_host = True if sel == 'y' else False

if is_host:
    # start server and begin scanning for new connections
    server.init()

    thread = threading.Thread(target=server.get_connections)
    thread.start()

    # start game once host decides so; WARNING: we may still receive new connections at this point, sort this out
    await_input(
        msg="[Host] Waiting for connections, enter 'start' to begin game: ",
        valid_entries=('start')
    )

    # when await_input finishes, we will reach this point

    print(f'[Host] Starting with {threading.active_count() - 1} player(s)!')

    server.start_game()

    while True:
        # tell the current player that it's their turn and send them deck info
        server.send(server.player_turn, 'turn')
        server.send_obj(server.player_turn, server.player_decks[server.player_turn])

else:
    client.init()

    print('[Client] Connected to server!')

    while True:
        match(client.recv()):
            case 'turn':
                # get info about my deck
                my_deck = client.recv_obj()

                if my_deck is None:
                    # this shouldn't happen, but TODO add error handing for this
                    continue

                print("\nDeck: ")
                for card in pickle.loads(my_deck):
                    print(card)

                sel = await_input(
                    msg='Enter your play: ',
                    valid_entries=('')
                )
                pass
            case '_':
                pass
