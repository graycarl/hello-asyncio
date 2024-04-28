import select
import socket
import utils

def loop(server_socket):
    epoll = select.epoll()
    epoll.register(server_socket.fileno(), select.EPOLLIN)

    connections = {}
    try:
        while True:
            events = epoll.poll(1)
            for fileno, event in events:
                if fileno == server_socket.fileno():
                    client_connection, _ = server_socket.accept()
                    client_connection.setblocking(False)
                    epoll.register(client_connection.fileno(), select.EPOLLIN)
                    connections[client_connection.fileno()] = client_connection
                elif event & select.EPOLLIN:
                    client_connection = connections[fileno]
                    data = client_connection.recv(1024)
                    if data:
                        response = utils.gen_response(data)
                        client_connection.sendall(response)
                        client_connection.shutdown(socket.SHUT_RDWR)
                    else:
                        epoll.unregister(fileno)
                        client_connection.close()
                        del connections[fileno]

                else:
                    raise Exception('Unknown event')
    finally:
        epoll.unregister(server_socket.fileno())
        epoll.close()
        server_socket.close()

def main():
    server_socket = utils.listen()
    server_socket.setblocking(False)

    try:
        loop(server_socket)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
