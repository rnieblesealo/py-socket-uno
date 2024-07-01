import threading
import random
import pickle
import server
import client
import sys


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
    # try to start the server until OK
    print('Attempting to start host server...')

    s_state = server.init()
    while s_state != 0:
        s_state = server.init()

        if s_state == 2:
            print('Cannot start host server; another host likely exists. Exiting...')
            sys.exit()

    print('Started host server!')

    get_conns = threading.Thread(target=server.get_connections)
    get_conns.start()

    # also initialize host client
    # keep trying until successful
    print('Attempting to start host client...')

    connected = client.init()
    while not connected:
        connected = client.init()

    print('Started host client!')

    # start game once host decides so, as long as we have more than 1 connection
    while True:
        sel = await_input(
            msg="Waiting for connections, enter 'start' to begin game: ",
            valid_entries=('start')
        )

        if len(server.conns) > 1:
            print(f'Starting with {len(server.conns)} player(s)!')
            break
        else:
            print(f'Not enough players! Need {str(server.MIN_PLAYERS)}')
            print(f'Have {str(len(server.conns))}')

    server.start_game()

    update_game = threading.Thread(target=server.update_game)
    update_game.start()

    # ask server to give the first turn
    client.send('give_first_turn')

# avoid re-initializing host client
if not is_host:
    print('OK, looking for game to join instead...')

    connected = client.init()
    while not connected:
        connected = client.init()

    print('Joined game! Waiting for host to start game...')

in_game = True
autoplay = True

while in_game:
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
            # or generate it if autoplay on
            sel = None
            if autoplay:
                sel = random.choice(my_plays)

            else:
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
        case 'win':
            print('YOU WIN !!!')
            client.send(client.DISCONNECT_MESSAGE)
            break
        case 'lose':
            print('YOU LOSE !!!')
            client.send(client.DISCONNECT_MESSAGE)
            break
        case '_':
            print('Default')
            pass
