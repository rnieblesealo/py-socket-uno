import threading
import pickle
import server
import client


def await_input(msg, valid_entries):
    """
    Waits for user to enter valid option, re-prompting entry otherwise
    """

    while True:
        s = str(input(msg)).lower().strip()
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

    get_conns = threading.Thread(target=server.get_connections)
    get_conns.start()

    # join the host's client
    client.init()

    # start game once host decides so
    # FIXME: we may still receive new connections at this point!
    await_input(
        msg="Waiting for connections, enter 'start' to begin game: ",
        valid_entries=('start')
    )

    # when await_input finishes, we will reach this point

    print(f'Starting with {len(server.conns)} player(s)!')

    server.start_game()

    update_game = threading.Thread(target=server.update_game)
    update_game.start()

    # ask server to give the first turn
    client.send('give_first_turn')

# avoid re-initializing host client
if not is_host:
    client.init()

while True:
    match(client.recv()):
        case 'turn':
            # get valid plays
            client.send('give_plays')

            my_plays = client.recv_obj()
            my_plays = pickle.loads(my_plays)

            # feed card into deck, play it if possible, and move turn
            # play handled server-side
            if len(my_plays) == 0:
                print('No playable cards!')

                client.send('no_playables')

                continue

            # get updated play info
            client.send('give_plays')

            my_plays = client.recv_obj()
            my_plays = pickle.loads(my_plays)

            # get info about my deck
            # it will be updated if refeed happened
            client.send('give_deck')

            my_deck = client.recv_obj()
            my_deck = pickle.loads(my_deck)

            print("\nIt's your turn! Your deck: ")
            for i in range(len(my_deck)):
                print(f'{str(i)}: {my_deck[i]}')

            print('\nYou may play these card indices: ')

            # turn all entries into string format
            for i in range(len(my_plays)):
                my_plays[i] = str(my_plays[i])
                print(f'{my_plays[i]} ')

            # get played card and send it to server
            sel = await_input(
                msg='\nEnter index of card you wanna play: ',
                valid_entries=my_plays
            )

            client.send('card_play')
            client.send(sel)

            pass
        case 'not_turn':
            print('Awaiting other play...')
            pass
        case '_':
            print('Default')
            pass
