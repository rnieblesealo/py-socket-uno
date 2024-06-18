import threading
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
        server.send(server.player_turn, 'turn')

else:
    client.init()

    print('[Client] Connected to server!')

    while True:
        match(client.recv()):
            case 'turn':
                sel = await_input(
                    msg='Enter your play: ',
                    valid_entries=('')
                )
                pass
            case '_':
                pass
