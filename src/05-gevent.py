import gevent.monkey
gevent.monkey.patch_all()

import threading
import utils

def main():
    listen_socket = utils.listen()
    while True:
        client_connection, _ = listen_socket.accept()
        threading.Thread(target=utils.handler, args=(client_connection,)).start()

if __name__ == "__main__":
    main()
