import select
import utils

def loop(server_socket):
    inputs = [server_socket]
    outputs = []
    errors = []

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, errors)

        for s in readable:
            if s is server_socket:
                client_connection, _ = server_socket.accept()
                client_connection.setblocking(False)
                inputs.append(client_connection)
            else:
                utils.handler(s, close=False)
                if s not in outputs:
                    outputs.append(s)

        for s in writable:
            if s in inputs:
                inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()

        for s in exceptional:
            if s in outputs:
                outputs.remove(s)
            if s in inputs:
                inputs.remove(s)
            s.close()

def main():
    server_socket = utils.listen()
    server_socket.setblocking(False)

    try:
        loop(server_socket)
    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
