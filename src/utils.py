import sys
import os
import socket
import textwrap
from time import sleep
import random
import time


def get_port():
    """
    Get the port number from with "80" + file name prefix
    """
    return 8000 + int(os.path.basename(sys.argv[0]).split('-')[0])


def listen(port=None):
    if port is None:
        port = get_port()
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(('', port))
    listen_socket.listen(1)
    print(f'Serving HTTP on port {port} ...')
    return listen_socket


def handler(client_connection, cpu_time=0.05, io_time=0.05, piece=0.01):
    """
    模拟 Http 服务器处理请求
    """
    _ = client_connection.recv(1024)
    # print(request_data.decode('utf-8'))

    def cpu_task(duration):
        end_time = time.time() + duration
        while time.time() < end_time:
            pass

    tasks = []
    for _ in range(int(cpu_time / piece)):
        tasks.append(lambda: cpu_task(piece))
    for _ in range(int(io_time / piece)):
        tasks.append(lambda: sleep(piece))

    random.shuffle(tasks)
    for task in tasks:
        task()

    http_response = textwrap.dedent(f"""\
        HTTP/1.1 200 OK
        Content-Type: text/plain

        Server cmd: {sys.argv[0]}
        CPU Time: {cpu_time}
        IO Time: {io_time}
        TOTAL Time: {cpu_time + io_time}
    """)
    client_connection.sendall(http_response.encode())
    client_connection.close()
