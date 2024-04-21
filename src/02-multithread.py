import threading
import utils

MAX_THREADS = 10
semaphore = threading.Semaphore(MAX_THREADS)


def handler(client_connection):
    try:
        utils.handler(client_connection)
    finally:
        semaphore.release()


def main():
    listen_socket = utils.listen()
    while True:
        client_connection, _ = listen_socket.accept()
        semaphore.acquire()
        threading.Thread(target=handler, args=(client_connection,)).start()

if __name__ == "__main__":
    main()
