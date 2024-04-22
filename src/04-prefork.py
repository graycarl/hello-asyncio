from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
import utils

NUM_WORKERS = 4
NUM_THREADS_PER_WORKER = 5


def run(server_socket):
    processes = []
    for _ in range(NUM_WORKERS):
        p = Process(target=handle_request, args=(server_socket,))
        p.daemon = True
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


def handle_request(server_socket):
    with ThreadPoolExecutor(max_workers=NUM_THREADS_PER_WORKER) as executor:
        while True:
            client_socket, _ = server_socket.accept()
            executor.submit(utils.handler, client_socket)


if __name__ == "__main__":
    server_socket = utils.listen()
    run(server_socket)
