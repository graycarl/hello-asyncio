import utils


def main():
    listen_socket = utils.listen()
    while True:
        client_connection, _ = listen_socket.accept()
        utils.handler(client_connection)


if __name__ == '__main__':
    main()
