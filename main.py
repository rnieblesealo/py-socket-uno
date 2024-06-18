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

    # start game once host decides so
    # WARNING: we may still receive new connections at this point, sort this out
    await_input(
        msg="Waiting for connections, enter 'start' to begin game: ",
        valid_entries=('start')
    )

    # when await_input finishes, we will reach this point

    print(f'Starting with {threading.active_count() - 1} player(s)!')

    server.start_game()

    while True:
        # tell the current player that it's their turn
        server.send(server.player_turn, 'turn')

        # send player their deck
        server.send_obj(
            server.player_turn,
            server.player_decks[server.player_turn]
        )

        # send player a list of cards they can play too
        server.send_obj(
            server.player_turn,
            server.get_playable_cards(
                server.card_stack[-1],
                server.player_decks[server.player_turn]
            )
        )


else:
    client.init()

    while True:
        match(client.recv()):
            case 'turn':
                # get info about my deck
                my_deck = client.recv_obj()

                if my_deck is None:
                    # this shouldn't happen, but TODO add error handing for this
                    continue

                my_deck = pickle.loads(my_deck)

                print("\nIt's your turn! Your deck: ")
                for i in range(len(my_deck)):
                    print(f'{str(i)}: {my_deck[i]}')

                # also get indices of valid card plays
                my_plays = client.recv_obj()

                if my_plays is None:
                    continue

                my_plays = pickle.loads(my_plays)

                # if no allowed plays, ask server to draw cards into this deck until a valid one's found
                if len(my_plays) == 0:
                    client.send('out')

                    # RESUME@: implement a server queue system

                # turn all entries into string format
                for index in my_plays:
                    index = str(index)

                print('\nYou may play these card indices: ')
                print(str(my_plays))

                sel = await_input(
                    msg='\nEnter index of card you wanna play: ',
                    valid_entries=(my_plays)
                )

                pass
            case '_':
                pass
