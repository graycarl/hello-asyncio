import concurrent.futures
import utils

MAX_THREADS = 10

def main():
    listen_socket = utils.listen()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        while True:
            client_connection, _ = listen_socket.accept()
            executor.submit(utils.handler, client_connection)


if __name__ == "__main__":
    main()
